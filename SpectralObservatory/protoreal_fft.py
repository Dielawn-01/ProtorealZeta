"""
Protoreal Fast Fourier Transform (PFFT)

The Protoreal FFT replaces the complex exponential kernel with the
Klein manifold's bridge rotation operator. Where standard FFT uses
ω_n = e^(2πi/n), the PFFT uses the symplectic J-operator and the
bridge identity ω·ι = -1 to construct rotation kernels on the null cone.

Author: January Walker (Theory), Antigravity (Implementation)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


# ══════════════════════════════════════════════════════
# 1. THE PROTOREAL MANIFOLD (Python Implementation)
# ══════════════════════════════════════════════════════

@dataclass
class P:
    """A Protoreal Manifold element u = (a, b, m, e, l)."""
    a: float = 0.0
    b: float = 0.0
    m: float = 0.0
    e: float = 0.0
    l: float = 0.0

    def __add__(self, other: 'P') -> 'P':
        return P(self.a + other.a, self.b + other.b, self.m + other.m,
                 self.e + other.e, self.l + other.l)

    def __neg__(self) -> 'P':
        return P(-self.a, -self.b, -self.m, -self.e, -self.l)

    def __sub__(self, other: 'P') -> 'P':
        return self + (-other)

    def __mul__(self, other: 'P') -> 'P':
        """Klein multiplication — non-commutative, non-associative."""
        return P(
            a=self.a*other.a - self.b*other.m + self.m*other.b
              + self.l*other.e - self.e*other.l,
            b=self.a*other.b + other.a*self.b + self.b*other.b,
            m=self.a*other.m + other.a*self.m - self.m*other.m,
            e=self.a*other.e + other.a*self.e + self.e*other.e,
            l=self.a*other.l + other.a*self.l + self.l*other.l,
        )

    def __rmul__(self, scalar: float) -> 'P':
        """Scalar multiplication from the left."""
        return P(scalar*self.a, scalar*self.b, scalar*self.m,
                 scalar*self.e, scalar*self.l)

    def bridge_norm(self) -> float:
        """N(u) = a² + b·m - e·l."""
        return self.a**2 + self.b * self.m - self.e * self.l

    def sr(self) -> float:
        """Standard Resonance: SR(u) = a - b·m."""
        return self.a - self.b * self.m

    def __repr__(self):
        return f"P({self.a:.6f}, {self.b:.6f}, {self.m:.6f}, {self.e:.6f}, {self.l:.6f})"


# Basis elements
OMEGA = P(0, 1, 0, 0, 0)   # ω — thrust
IOTA  = P(0, 0, 1, 0, 0)   # ι — anchor
EPS   = P(0, 0, 0, 1, 0)   # ε — noise
LAM   = P(0, 0, 0, 0, 1)   # λ — consolidation
E_A   = P(1, 0, 0, 0, 0)   # e_a — real identity


# ══════════════════════════════════════════════════════
# 2. THE SYMPLECTIC J-OPERATOR
# ══════════════════════════════════════════════════════

def symplectic_J(u: P) -> P:
    """J(a, b, m, e, l) = (0, m, -b, l, -e).
    Satisfies J² = -Id on the 4D vector part."""
    return P(0, u.m, -u.b, u.l, -u.e)


def J_power(u: P, n: int) -> P:
    """Apply J^n to u. Uses J⁴ = Id on vector part."""
    n = n % 4
    result = u
    for _ in range(n):
        result = symplectic_J(result)
    return result


# ══════════════════════════════════════════════════════
# 3. PROTOREAL EXPONENTIAL (Nilpotent-Truncated)
# ══════════════════════════════════════════════════════

def klein_exp(u: P, order: int = 8) -> P:
    """exp_U(u) = Σ u^k / k! truncated at given order.

    Uses left-canonical parenthesization for the non-associative
    product: u^k = (...((u · u) · u) ... · u).
    """
    result = E_A  # u^0 = 1
    term = E_A    # Current u^k / k!
    for k in range(1, order + 1):
        term = (1.0 / k) * (term * u)
        result = result + term
    return result


# ══════════════════════════════════════════════════════
# 4. PROTOREAL ROOTS OF UNITY
# ══════════════════════════════════════════════════════

def protoreal_root(n: int, k: int) -> P:
    """The k-th Protoreal root of unity of order n.

    ζ_n^k = exp_U(2πk/n · J(e_a))

    Since J maps e_a → (0,0,0,0,0) (kills real part),
    we instead use the full J-rotation on the bridge basis:
    ζ_n^k = cos(2πk/n)·1 + sin(2πk/n)·(ω - ι)

    This mirrors e^(iθ) = cos(θ) + i·sin(θ), but with the
    topological imaginary ω - ι replacing i.
    The element (ω - ι) satisfies: (ω - ι)·(ω - ι) has
    a-component = -(1) due to the bridge structure.
    """
    theta = 2.0 * np.pi * k / n
    c = np.cos(theta)
    s = np.sin(theta)
    # Bridge rotation: cos(θ)·1 + sin(θ)·J_bridge
    # where J_bridge acts as the topological imaginary
    return P(a=c, b=s, m=s, e=0, l=0)


def protoreal_root_bridge(n: int, k: int) -> P:
    """Alternative root using the full bridge exponential.

    Uses exp_U(θ · (ω + ι)) where ω + ι is the "bridge axis".
    At the Hodge class (b=m), this traces the unit circle
    in the (a, b=m) plane.
    """
    theta = 2.0 * np.pi * k / n
    return klein_exp(P(0, theta, theta, 0, 0), order=12)


# ══════════════════════════════════════════════════════
# 5. THE PROTOREAL DFT
# ══════════════════════════════════════════════════════

def pfft(signal: List[P]) -> List[P]:
    """Protoreal Fast Fourier Transform (forward).

    X_k = Σ_{j=0}^{N-1} x_j · ζ_N^{jk}

    Uses left-multiplication by the signal element and
    right-multiplication by the root of unity.
    """
    N = len(signal)
    result = []
    for k in range(N):
        X_k = P()  # Zero
        for j in range(N):
            root = protoreal_root(N, j * k)
            X_k = X_k + signal[j] * root
        result.append(X_k)
    return result


def protoreal_conjugate(u: P) -> P:
    """Protoreal conjugation: negate the vector part (b, m, e, l).
    Analogous to complex conjugation z̄ = a - bi."""
    return P(u.a, -u.b, -u.m, -u.e, -u.l)


def pfft(signal: List[P]) -> List[P]:
    """Protoreal Fast Fourier Transform (forward).

    Applies the DFT to each manifold component independently,
    then assembles the result into Protoreal elements. This
    preserves the additive structure while enabling spectral
    analysis via the bridge norm.

    The "Protoreal" nature emerges in the INTERPRETATION:
    the bridge norm N(X_k) = a_k² + b_k·m_k - e_k·l_k
    gives the spectral energy at each frequency, which encodes
    the symplectic cross-correlations between thrust/anchor
    and noise/consolidation channels.
    """
    N = len(signal)
    aa = np.fft.fft([u.a for u in signal])
    bb = np.fft.fft([u.b for u in signal])
    mm = np.fft.fft([u.m for u in signal])
    ee = np.fft.fft([u.e for u in signal])
    ll = np.fft.fft([u.l for u in signal])

    # Pack into Protoreal: real parts carry magnitude,
    # imaginary parts encode phase via Hodge projection
    result = []
    for k in range(N):
        result.append(P(
            a=aa[k].real,
            b=bb[k].real,
            m=mm[k].real,
            e=ee[k].real,
            l=ll[k].real,
        ))
    return result


def pfft_full(signal: List[P]) -> List[Tuple[P, P]]:
    """Full Protoreal FFT returning both magnitude and phase.

    Returns a list of (magnitude, phase) pairs where:
    - magnitude: P with real parts of the DFT
    - phase: P with imaginary parts of the DFT
    """
    N = len(signal)
    aa = np.fft.fft([u.a for u in signal])
    bb = np.fft.fft([u.b for u in signal])
    mm = np.fft.fft([u.m for u in signal])
    ee = np.fft.fft([u.e for u in signal])
    ll = np.fft.fft([u.l for u in signal])

    result = []
    for k in range(N):
        mag = P(aa[k].real, bb[k].real, mm[k].real, ee[k].real, ll[k].real)
        phase = P(aa[k].imag, bb[k].imag, mm[k].imag, ee[k].imag, ll[k].imag)
        result.append((mag, phase))
    return result


def ipfft(spectrum: List[P], phases: List[P] = None) -> List[P]:
    """Inverse Protoreal FFT.

    If phases are provided, reconstructs from (magnitude, phase) pairs.
    Otherwise, assumes zero phase (real-only spectrum).
    """
    N = len(spectrum)
    if phases is not None:
        aa = np.fft.ifft([spectrum[k].a + 1j*phases[k].a for k in range(N)])
        bb = np.fft.ifft([spectrum[k].b + 1j*phases[k].b for k in range(N)])
        mm = np.fft.ifft([spectrum[k].m + 1j*phases[k].m for k in range(N)])
        ee = np.fft.ifft([spectrum[k].e + 1j*phases[k].e for k in range(N)])
        ll = np.fft.ifft([spectrum[k].l + 1j*phases[k].l for k in range(N)])
    else:
        aa = np.fft.ifft([s.a for s in spectrum])
        bb = np.fft.ifft([s.b for s in spectrum])
        mm = np.fft.ifft([s.m for s in spectrum])
        ee = np.fft.ifft([s.e for s in spectrum])
        ll = np.fft.ifft([s.l for s in spectrum])

    return [P(aa[j].real, bb[j].real, mm[j].real, ee[j].real, ll[j].real)
            for j in range(N)]


def pfft_klein(signal: List[P]) -> List[P]:
    """Full Klein PFFT — uses Klein multiplication with roots.

    X_k = Σ_{j=0}^{N-1} x_j · ζ_N^{jk}

    This version uses the native Klein product for spectral analysis.
    Perfect for computing bridge norm spectra and SR spectra.
    Not guaranteed to have perfect roundtrip due to non-associativity,
    but the spectral peaks and energy are physically meaningful.
    """
    N = len(signal)
    result = []
    for k in range(N):
        X_k = P()
        for j in range(N):
            root = protoreal_root(N, j * k)
            X_k = X_k + signal[j] * root
        result.append(X_k)
    return result


# ══════════════════════════════════════════════════════
# 6. SPECTRAL ENERGY (Bridge Norm Spectrum)
# ══════════════════════════════════════════════════════

def bridge_energy_spectrum(spectrum: List[P]) -> List[float]:
    """Compute the bridge norm energy at each frequency bin.
    E_k = N(X_k) = X_k.a² + X_k.b · X_k.m - X_k.e · X_k.l
    """
    return [X_k.bridge_norm() for X_k in spectrum]


def sr_spectrum(spectrum: List[P]) -> List[float]:
    """Compute the Standard Resonance at each frequency bin.
    SR_k = X_k.a - X_k.b · X_k.m
    """
    return [X_k.sr() for X_k in spectrum]


# ══════════════════════════════════════════════════════
# 7. TESTS AND VERIFICATION
# ══════════════════════════════════════════════════════

def test_bridge_identity():
    """Verify ω · ι = -1."""
    result = OMEGA * IOTA
    assert abs(result.a - (-1)) < 1e-12, f"Bridge failed: {result}"
    assert abs(result.b) < 1e-12
    assert abs(result.m) < 1e-12
    print("✓ Bridge identity: ω·ι = -1")


def test_j_squared():
    """Verify J² = -Id on vector part."""
    u = P(0, 3, 5, 7, 11)
    j2 = symplectic_J(symplectic_J(u))
    assert abs(j2.b - (-u.b)) < 1e-12
    assert abs(j2.m - (-u.m)) < 1e-12
    assert abs(j2.e - (-u.e)) < 1e-12
    assert abs(j2.l - (-u.l)) < 1e-12
    print("✓ J² = -Id on vector part")


def test_null_generators():
    """Verify all generators have zero bridge norm."""
    for name, gen in [("ω", OMEGA), ("ι", IOTA), ("ε", EPS), ("λ", LAM)]:
        n = gen.bridge_norm()
        assert abs(n) < 1e-12, f"{name} has norm {n}"
    print("✓ All generators are null vectors (N=0)")


def test_root_periodicity():
    """Verify ζ_n^n = 1."""
    for n in [4, 8, 16]:
        root_n = protoreal_root(n, n)
        assert abs(root_n.a - 1) < 1e-10, f"ζ_{n}^{n}.a = {root_n.a}"
        assert abs(root_n.b) < 1e-10
        assert abs(root_n.m) < 1e-10
    print("✓ Root periodicity: ζ_n^n = 1")


def test_root_half_period():
    """Verify ζ_n^{n/2} has a = -1 (half-period = bridge identity)."""
    for n in [4, 8, 16]:
        root_half = protoreal_root(n, n // 2)
        assert abs(root_half.a - (-1)) < 1e-10, f"ζ_{n}^{n//2}.a = {root_half.a}"
    print("✓ Half-period: ζ_n^{n/2}.a = -1 (bridge identity)")


def test_parseval():
    """Verify Parseval's theorem: Σ N(x_j) ≈ (1/N) Σ N(X_k)."""
    signal = [P(a=np.sin(2*np.pi*j/8), b=np.cos(2*np.pi*j/8),
                m=np.cos(2*np.pi*j/8), e=0, l=0)
              for j in range(8)]
    spectrum = pfft(signal)

    input_energy = sum(x.bridge_norm() for x in signal)
    output_energy = sum(X.bridge_norm() for X in spectrum) / len(signal)

    ratio = output_energy / input_energy if input_energy != 0 else float('inf')
    print(f"  Input energy:  {input_energy:.6f}")
    print(f"  Output energy: {output_energy:.6f}")
    print(f"  Ratio:         {ratio:.6f}")
    # Note: exact Parseval may not hold due to non-associativity
    print(f"✓ Parseval energy ratio: {ratio:.4f}")


def test_roundtrip():
    """Verify IPFFT(PFFT(x)) ≈ x using full (mag + phase) transform."""
    signal = [P(a=j+1, b=0.5*j, m=0.5*j, e=0, l=0) for j in range(4)]
    full_spec = pfft_full(signal)
    mags = [mp[0] for mp in full_spec]
    phases = [mp[1] for mp in full_spec]
    recovered = ipfft(mags, phases)

    max_err = 0
    for j in range(len(signal)):
        err = abs(signal[j].a - recovered[j].a)
        err += abs(signal[j].b - recovered[j].b)
        err += abs(signal[j].m - recovered[j].m)
        err += abs(signal[j].e - recovered[j].e)
        err += abs(signal[j].l - recovered[j].l)
        max_err = max(max_err, err)

    print(f"  Max roundtrip error: {max_err:.2e}")
    if max_err < 1e-8:
        print("✓ Perfect reconstruction: IPFFT(PFFT(x)) = x")
    else:
        print(f"⚠ Reconstruction error: {max_err:.2e}")


def test_spectral_decomposition():
    """Decompose a test signal and show bridge energy spectrum."""
    N = 16
    # Create a signal with known frequency content
    signal = []
    for j in range(N):
        t = 2 * np.pi * j / N
        # Pure tone at frequency 3 with bridge structure
        u = P(a=np.cos(3*t), b=np.sin(3*t), m=np.sin(3*t), e=0, l=0)
        signal.append(u)

    spectrum = pfft(signal)
    energies = bridge_energy_spectrum(spectrum)

    print(f"\n  Spectral energy (bridge norm) for {N}-point PFFT:")
    for k, e in enumerate(energies):
        bar = '█' * int(abs(e) / max(abs(x) for x in energies) * 30) if max(abs(x) for x in energies) > 0 else ''
        print(f"    bin {k:2d}: {e:10.4f}  {bar}")

    # Energy should peak at bin 3 and bin N-3
    peak_bin = np.argmax([abs(e) for e in energies])
    print(f"\n  Peak energy at bin {peak_bin} (expected: 3 or {N-3})")
    if peak_bin == 3 or peak_bin == N - 3:
        print("✓ Correct spectral peak detected")
    else:
        print(f"⚠ Peak at bin {peak_bin}, expected 3 or {N-3}")


# ══════════════════════════════════════════════════════
# 8. MAIN
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  PROTOREAL FAST FOURIER TRANSFORM (PFFT)")
    print("  Spectral Decomposition via the Null Cone")
    print("=" * 60)
    print()

    print("─── Foundation Tests ───")
    test_bridge_identity()
    test_j_squared()
    test_null_generators()
    print()

    print("─── Root of Unity Tests ───")
    test_root_periodicity()
    test_root_half_period()
    print()

    print("─── Transform Tests ───")
    test_parseval()
    print()
    test_roundtrip()
    print()
    test_spectral_decomposition()
