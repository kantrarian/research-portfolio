import itertools
import unittest

import numpy as np
from numpy.testing import assert_allclose
from scipy.linalg import expm, logm

from reference_checks import (dispersion_qubo, frozen_plastic_step,
                              gaussian_information, group_commutator,
                              hencky, hencky_rate, ising_from_upper)


class BCHChecks(unittest.TestCase):
    def test_state_metric_volume_and_rotation(self):
        rotation = expm(np.array([[0., -.4, 0.], [.4, 0., 0.], [0., 0., 0.]]))
        f = rotation @ np.diag([1.3, .8, 1.1])
        fp = np.diag([1.2, 1 / 1.2, 1.])
        lp = np.array([[.2, .7, .1], [-.3, -.1, .2], [0., 0., -.1]])
        fe_new, fp_new, e = frozen_plastic_step(f, fp, lp, .1)
        assert_allclose(fe_new @ fp_new, f, atol=2e-14)
        assert_allclose(e, e.T, atol=2e-14)
        self.assertGreater(np.linalg.eigvalsh(fe_new.T @ fe_new).min(), 0)
        self.assertAlmostEqual(np.linalg.det(fp_new), np.linalg.det(fp), places=13)
        fe_zero, _, _ = frozen_plastic_step(f, np.eye(3), np.zeros((3, 3)), .1)
        assert_allclose(fe_zero, f)
        self.assertGreater(np.linalg.norm(fe_zero - expm(hencky(fe_zero))), .1)

    def test_symmetric_commuting_branch(self):
        e = np.diag([.3, -.2, .1])
        d = np.diag([.1, -.05, -.05])
        _, _, updated = frozen_plastic_step(expm(e), np.eye(3), d, .2)
        assert_allclose(updated, e - .2 * d, atol=1e-14)

    def test_zero_commutator_does_not_certify_nonsymmetric_update(self):
        lp = np.zeros((3, 3))
        lp[0, 1] = 1.
        e = np.zeros((3, 3))
        self.assertEqual(np.linalg.norm(e @ lp - lp @ e), 0.)
        _, _, exact = frozen_plastic_step(np.eye(3), np.eye(3), lp, .1)
        fast = e - .1 * lp
        self.assertAlmostEqual(np.linalg.norm(fast - fast.T), .14142135623730953)
        self.assertAlmostEqual(np.linalg.norm(fast - exact), .07079881555915817)

    def test_symmetric_trial_does_not_make_product_log_a_strain(self):
        e = np.diag([.3, -.2, 0.])
        lp = np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., 0.]])
        fe = expm(e)
        updated = fe @ expm(-.1 * lp)
        product_log = logm(updated)
        strain = hencky(updated)
        self.assertGreater(np.linalg.norm(product_log - product_log.T), .07)
        self.assertGreater(np.linalg.norm(product_log - strain), .036)
        assert_allclose(strain, strain.T, atol=1e-14)

    def test_pure_spin_is_conjugation(self):
        e = np.diag([.3, -.2, .1])
        w = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 0.]])
        _, _, updated = frozen_plastic_step(expm(e), np.eye(3), w, .1)
        assert_allclose(updated, expm(.1 * w) @ e @ expm(-.1 * w), atol=1e-14)

    def test_first_variation_including_degeneracy(self):
        lp = np.array([[.2, .7, .1], [-.3, -.1, .2], [.4, -.2, -.1]])
        for e in (np.diag([.3, -.2, .1]), np.eye(3) * .2):
            fe = expm(e)
            h = 1e-6
            rate = (hencky(fe @ expm(-h * lp)) - hencky(fe @ expm(h * lp))) / (2*h)
            assert_allclose(hencky_rate(e, lp), rate, atol=3e-10)


class QUBOChecks(unittest.TestCase):
    def setUp(self):
        self.weights = np.array([.2, 1.1, .7, .4])
        self.dist = np.abs(np.arange(4)[:, None] - np.arange(4)[None, :]) / 3
        self.alpha = .6
        self.states = np.array(list(itertools.product([0, 1], repeat=4)))

    def test_all_bitstrings_polynomial_upper_symmetric_and_ising(self):
        q, c = dispersion_qubo(self.weights, self.dist, self.alpha, 4., 2)
        h, j, ci = ising_from_upper(q, c)
        symmetric = (q + q.T) / 2
        for x in self.states:
            direct = (-self.weights @ x - self.alpha * x @ np.triu(self.dist, 1) @ x
                      + 4. * (sum(x) - 2)**2)
            z = 1 - 2 * x
            assert_allclose([x @ q @ x + c, x @ symmetric @ x + c,
                             h @ z + z @ j @ z + ci], direct, atol=1e-13)

    def test_bound_covers_infeasible_states_for_every_budget(self):
        bound = np.abs(self.weights).sum() + abs(self.alpha) * np.abs(np.triu(self.dist, 1)).sum()
        for k in range(5):
            q, c = dispersion_qubo(self.weights, self.dist, self.alpha, bound + .1, k)
            energies = np.array([x @ q @ x + c for x in self.states])
            feasible = self.states.sum(axis=1) == k
            self.assertGreater(energies[~feasible].min(), energies[feasible].min())

    def test_feasible_enumeration_cannot_detect_insufficient_penalty(self):
        q, c = dispersion_qubo(self.weights, self.dist, self.alpha, 0., 2)
        energies = np.array([x @ q @ x + c for x in self.states])
        self.assertNotEqual(self.states[energies.argmin()].sum(), 2)

    def test_reject_invalid_budget_and_matrix_convention(self):
        for k in (-1, 5, 1.5, True):
            with self.assertRaises(ValueError):
                dispersion_qubo(self.weights, self.dist, .6, 4., k)
        with self.assertRaises(ValueError):
            ising_from_upper(np.ones((2, 2)), 0)


class InformationAndUnitaryChecks(unittest.TestCase):
    def test_singular_latent_covariance_finite_with_noise(self):
        sigma = np.array([[1., -1.], [-1., 1.]])
        self.assertEqual(np.linalg.det(sigma), 0)
        info = gaussian_information(sigma, np.eye(2), np.eye(2) * .5)
        self.assertAlmostEqual(info, .5 * np.log(5.))
        with self.assertRaises(ValueError):
            gaussian_information(sigma, np.eye(2), np.zeros((2, 2)))

    def test_unit_conversion_preserves_information(self):
        sigma = np.array([[1., .3], [.3, 2.]])
        h, noise = np.eye(2), np.diag([.2, .5])
        units = np.diag([10., .1])
        self.assertAlmostEqual(gaussian_information(sigma, h, noise),
                               gaussian_information(sigma, units @ h, units @ noise @ units.T))

    def test_fourth_order_real_deficit_and_coefficient(self):
        a = np.array([[0., 1.], [1., 0.]]) / 2
        b = np.diag([1., -1.]) / 2
        psi = np.array([1., 0.], dtype=complex)
        comm = a @ b - b @ a
        expected = .5 * np.linalg.norm(comm @ psi)**2
        ratios = []
        for t in (.1, .05, .025):
            u = group_commutator(a, b, t)
            assert_allclose(u.conj().T @ u, np.eye(2), atol=1e-14)
            deficit = .5 * np.linalg.norm((u - np.eye(2)) @ psi)**2
            self.assertAlmostEqual(deficit, 1 - np.vdot(psi, u @ psi).real, places=14)
            ratios.append(deficit / t**4)
        self.assertLess(abs(ratios[-1] - expected), 2e-5)
        self.assertLess(abs(ratios[-1] - expected), abs(ratios[0] - expected))

    def test_nonhermitian_generator_refused(self):
        with self.assertRaises(ValueError):
            group_commutator(np.array([[0., 1.], [0., 0.]]), np.eye(2), .1)


if __name__ == "__main__":
    unittest.main()
