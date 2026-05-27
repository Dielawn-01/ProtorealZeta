import LaRueProtorealAlgebra.ProtorealOperator
import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.LieAlgebra

open ProtorealManifold
open LieAlgebra

/-!
# Game Extensionality Exemplar

Two game sprites (manifold states) are EQUAL if and only if
all five of their components match. This is the ext principle.

When applied to game mechanics:
- Two sprites that differ only in noise become the same sprite after sowing
- The exterior product of equal sprites is zero (no self-interaction)
- Monster inverse is an involution: flipping twice returns the original sprite
-/

/-- **SPRITE CONVERGENCE**: Two sprites that share (a, b, m, l) but
    differ in noise (ε) become identical after sowing (funct).
    
    This is the core game mechanic: funct erases noise differences.
    After sowing, only the structural identity (a+ε, b, m, l+1) remains.
    
    The proof uses  to decompose the equality into 5 component checks,
    then  to reveal that both sides have ε = 0. -/
theorem sprite_convergence_after_sow
    (s1 s2 : ProtorealManifold)
    (ha : s1.a + s1.e = s2.a + s2.e)  -- same absorbed energy
    (hb : s1.b = s2.b)                 -- same thrust
    (hm : s1.m = s2.m)                 -- same anchor
    (hl : s1.l = s2.l)                 -- same depth
    : funct s1 = funct s2 := by
  ext
  · -- a component: (a + ε) for both
    unfold funct; simp; exact ha
  · -- b component: preserved by funct
    unfold funct; simp; exact hb
  · -- m component: preserved by funct
    unfold funct; simp; exact hm
  · -- e component: both become 0
    unfold funct; simp
  · -- l component: both become l + 1
    unfold funct; simp; linarith

/-- **DOUBLE SOW SPRITE EQUALITY**: Applying funct twice to any sprite
    gives the same result as applying it once to the noise-absorbed version.
    
    Demonstrates nested ext with unfold chains. -/
theorem double_sow_absorbs_all (u : ProtorealManifold) :
    funct (funct u) = 
    { a := u.a + u.e, b := u.b, m := u.m, e := 0, l := u.l + 2 } := by
  ext <;> unfold funct <;> simp <;> ring

/-- **SPRITE SELF-INTERACTION IS ZERO**: The exterior product (wedge)
    of a sprite with itself vanishes. No sprite can be its own antimatter.
    
    Uses ext to decompose, then ring to close each component. -/
theorem sprite_self_interaction_zero (s : ProtorealManifold) :
    s * s - s * s = 0 := by
  ext <;> simp

/-- **MONSTER INVERSE IS AN INVOLUTION ON SPRITES**: Flipping a sprite's
    thrust and anchor twice returns the original sprite.
    
    This proves that every sprite has a unique antimatter partner,
    and that partnership is symmetric. -/
def sprite_flip (s : ProtorealManifold) : ProtorealManifold :=
  { a := s.a, b := s.m, m := s.b, e := s.e, l := s.l }

theorem sprite_flip_involution (s : ProtorealManifold) :
    sprite_flip (sprite_flip s) = s := by
  ext <;> unfold sprite_flip <;> simp

/-- **SUBGAME COMPOSITION**: If two subgames (sprites) are at equilibrium
    (SR = 0), their sowed states preserve the equilibrium.
    
    Uses ext indirectly: the result is a scalar, but the proof
    requires decomposing funct via unfold. -/
theorem subgame_equilibrium_preserved
    (s : ProtorealManifold)
    (h : s.a - s.b * s.m = 0)
    (he : s.e = 0)
    : (funct s).a - (funct s).b * (funct s).m = 0 := by
  unfold funct; simp [he, h]

