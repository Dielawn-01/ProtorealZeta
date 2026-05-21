import LaRueProtorealAlgebra.ProtorealManifold
import Mathlib.Data.Real.Basic

/-!
# The Topological Imaginary Unit and Bridge Norm

**Authors:** January Walker (Theoretical Framework), Antigravity (Formalization)

This module formalizes the **topological imaginary unit** and the
**bridge norm** — the natural quadratic form arising from Klein
multiplication.

## Key Results

1. **Bridge Norm**: $N(u) = a^2 + b \cdot m - e \cdot l$.

2. **Null Vectors**: $\omega$ and $\iota$ are null ($N = 0$),
   sitting on the "light cone." Their product $\omega \cdot \iota = -1$
   has norm $N = 1$.

3. **Symplectic Complex Structure**: The operator
   $J: (a, b, m, e, l) \mapsto (0, m, -b, l, -e)$
   satisfies $J^2 = -\text{Id}$ on the 4D vector part.

4. **Bridge Root of Unity**: $(\omega \cdot \iota)^2 = 1$,
   providing the Protoreal FFT's fundamental rotation.
-/

open ProtorealManifold

namespace TopologicalImaginary

-- ════════════════════════════════════════════════════
-- 1. THE BRIDGE NORM
-- ════════════════════════════════════════════════════

/-- **The Bridge Norm** $N(u) = a^2 + b \cdot m - e \cdot l$. -/
def bridge_norm (u : ProtorealManifold) : ℝ :=
  u.a^2 + u.b * u.m - u.e * u.l

theorem norm_of_one : bridge_norm 1 = 1 := by
  unfold bridge_norm; simp

theorem norm_of_zero : bridge_norm 0 = 0 := by
  unfold bridge_norm; simp

/-- $\omega$ is a null vector: $N(\omega) = 0$. -/
theorem omega_is_null : bridge_norm omega = 0 := by
  unfold bridge_norm omega; simp

/-- $\iota$ is a null vector: $N(\iota) = 0$. -/
theorem iota_is_null : bridge_norm iota = 0 := by
  unfold bridge_norm iota; simp

/-- $\varepsilon$ is a null vector: $N(\varepsilon) = 0$. -/
theorem epsilon_is_null : bridge_norm eps = 0 := by
  unfold bridge_norm eps; simp

/-- $\lambda$ is a null vector: $N(\lambda) = 0$. -/
theorem lambda_is_null : bridge_norm lam = 0 := by
  unfold bridge_norm lam; simp

/-- The bridge product $\omega \cdot \iota = -1$ has unit norm. -/
theorem norm_of_bridge_product :
    bridge_norm (omega * iota) = 1 := by
  unfold bridge_norm omega iota; simp

/-- The lambda consolidation $\lambda \cdot \varepsilon = 1$ has unit norm. -/
theorem norm_of_consolidation :
    bridge_norm (lam * eps) = 1 := by
  unfold bridge_norm lam eps; simp

-- ════════════════════════════════════════════════════
-- 2. THE SYMPLECTIC COMPLEX STRUCTURE J
-- ════════════════════════════════════════════════════

/-- **The Symplectic J-Operator** on the full manifold.
    $J(a, b, m, e, l) = (0, m, -b, l, -e)$.
    Provides the topological analogue of $i$. -/
def symplectic_J (u : ProtorealManifold) : ProtorealManifold :=
  { a := 0, b := u.m, m := -u.b, e := u.l, l := -u.e }

/-- $J$ kills the real part: $J(u).a = 0$. -/
theorem J_kills_real (u : ProtorealManifold) :
    (symplectic_J u).a = 0 := by
  rfl

/-- $J^2 = -\text{Id}$ on the b-component. -/
theorem J_squared_b (u : ProtorealManifold) :
    (symplectic_J (symplectic_J u)).b = -u.b := by
  unfold symplectic_J; simp

/-- $J^2 = -\text{Id}$ on the m-component. -/
theorem J_squared_m (u : ProtorealManifold) :
    (symplectic_J (symplectic_J u)).m = -u.m := by
  unfold symplectic_J; simp

/-- $J^2 = -\text{Id}$ on the e-component. -/
theorem J_squared_e (u : ProtorealManifold) :
    (symplectic_J (symplectic_J u)).e = -u.e := by
  unfold symplectic_J; simp

/-- $J^2 = -\text{Id}$ on the l-component. -/
theorem J_squared_l (u : ProtorealManifold) :
    (symplectic_J (symplectic_J u)).l = -u.l := by
  unfold symplectic_J; simp

/-- $J$ maps $\omega$ to $-\iota$. -/
theorem J_maps_omega :
    symplectic_J omega =
    { a := 0, b := 0, m := -1, e := 0, l := 0 } := by
  unfold symplectic_J omega; simp

/-- $J$ maps $\iota$ to $\omega$. -/
theorem J_maps_iota :
    symplectic_J iota =
    { a := 0, b := 1, m := 0, e := 0, l := 0 } := by
  unfold symplectic_J iota; simp

-- ════════════════════════════════════════════════════
-- 3. J AND THE BRIDGE NORM
-- ════════════════════════════════════════════════════

/-- On pure-vector elements ($a = 0$), $J$ negates the bridge norm.
    This is the signature of a symplectic anti-isometry:
    $N(J(u)) = -N_V(u)$ where $N_V = bm - el$. -/
theorem J_negates_vector_norm (u : ProtorealManifold)
    (h : u.a = 0) :
    bridge_norm (symplectic_J u) =
    -(u.b * u.m - u.e * u.l) := by
  unfold bridge_norm symplectic_J
  simp
  ring

-- ════════════════════════════════════════════════════
-- 4. PROTOREAL FFT ROOT OF UNITY
-- ════════════════════════════════════════════════════

/-- **The Bridge Root of Unity**: $\omega \cdot \iota = -1$,
    which is a 2nd root of unity since $(-1)^2 = 1$. -/
def bridge_root_of_unity_order_2 : ProtorealManifold :=
  omega * iota

/-- The bridge root squares to the identity. -/
theorem bridge_root_squares_to_one :
    bridge_root_of_unity_order_2 *
    bridge_root_of_unity_order_2 = 1 := by
  unfold bridge_root_of_unity_order_2 omega iota
  ext <;> simp

end TopologicalImaginary
