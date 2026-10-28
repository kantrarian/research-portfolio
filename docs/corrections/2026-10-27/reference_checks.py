"""Small mathematical oracles, not production solvers or empirical benchmarks."""

import numpy as np
from scipy.linalg import expm


def hencky(fe):
    c = fe.T @ fe
    values, vectors = np.linalg.eigh(c)
    if np.any(values <= 0):
        raise ValueError("elastic metric must be positive definite")
    return (vectors * (0.5 * np.log(values))) @ vectors.T


def frozen_plastic_step(f_new, fp_old, lp, dt):
    if not np.isfinite(dt) or dt < 0:
        raise ValueError("dt must be finite and nonnegative")
    if np.linalg.det(f_new) <= 0 or np.linalg.det(fp_old) <= 0:
        raise ValueError("deformation maps must have positive determinant")
    fe_trial = np.linalg.solve(fp_old.T, f_new.T).T
    fp_new = expm(dt * lp) @ fp_old
    fe_new = fe_trial @ expm(-dt * lp)
    return fe_new, fp_new, hencky(fe_new)


def hencky_rate(e, lp):
    """First variation of the SPD sandwich in a fixed intermediate frame."""
    values, basis = np.linalg.eigh(e)
    flow = basis.T @ lp @ basis
    d = (flow + flow.T) / 2
    w = (flow - flow.T) / 2
    gaps = values[:, None] - values[None, :]
    factor = np.ones_like(gaps)
    small = np.abs(gaps) < 1e-5
    factor[small] += gaps[small] ** 2 / 3 - gaps[small] ** 4 / 45
    factor[~small] = gaps[~small] / np.tanh(gaps[~small])
    return basis @ (-factor * d - gaps * w) @ basis.T


def dispersion_qubo(weights, distances, alpha, penalty, k):
    weights = np.asarray(weights, dtype=float)
    distances = np.asarray(distances, dtype=float)
    n = len(weights)
    if not isinstance(k, (int, np.integer)) or isinstance(k, bool) or not 0 <= k <= n:
        raise ValueError("k must be an integer in [0,n]")
    if distances.shape != (n, n) or not np.allclose(distances, distances.T):
        raise ValueError("distances must be square and symmetric")
    if not (np.isfinite(weights).all() and np.isfinite(distances).all()
            and np.isfinite(alpha) and np.isfinite(penalty) and penalty >= 0):
        raise ValueError("finite coefficients and nonnegative penalty required")
    q = np.triu(2 * penalty - alpha * distances, 1)
    q += np.diag(-weights + penalty * (1 - 2 * k))
    return q, float(penalty * k * k)


def ising_from_upper(q, constant):
    if not np.allclose(q, np.triu(q)):
        raise ValueError("each pair must be stored once in the upper triangle")
    pairs = np.triu(q, 1)
    h = -np.diag(q) / 2 - (pairs.sum(axis=0) + pairs.sum(axis=1)) / 4
    return h, pairs / 4, constant + np.trace(q) / 2 + pairs.sum() / 4


def gaussian_information(sigma, h, noise):
    """I(z; H z + epsilon), including degenerate Gaussian latent fields."""
    sigma, h, noise = (np.asarray(a, dtype=float) for a in (sigma, h, noise))
    if not np.isfinite(sigma).all() or not np.allclose(sigma, sigma.T):
        raise ValueError("symmetric finite latent covariance required")
    if np.linalg.eigvalsh(sigma).min() < -1e-12:
        raise ValueError("latent covariance must be positive semidefinite")
    if not np.isfinite(noise).all() or not np.allclose(noise, noise.T):
        raise ValueError("symmetric finite noise covariance required")
    values, vectors = np.linalg.eigh(noise)
    if np.any(values <= 0):
        raise ValueError("strictly positive observation noise required")
    whiten = (vectors * (values ** -0.5)) @ vectors.T
    info_matrix = np.eye(len(noise)) + whiten @ h @ sigma @ h.T @ whiten
    sign, logdet = np.linalg.slogdet(info_matrix)
    if sign <= 0:
        raise ValueError("invalid information matrix")
    return float(0.5 * logdet)


def group_commutator(a, b, t):
    if not np.allclose(a, a.conj().T) or not np.allclose(b, b.conj().T):
        raise ValueError("unitary construction requires Hermitian generators")
    return expm(-1j * a * t) @ expm(-1j * b * t) @ expm(1j * a * t) @ expm(1j * b * t)
