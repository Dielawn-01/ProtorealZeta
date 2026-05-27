import LaRueProtorealAlgebra.Basic

theorem string_worldline_advances (u : ProtorealManifold) :
    (funct u).l = u.l + 1 :=
begin
  intro u,
  -- Directly access the field `l` from the manifold instance
  have l_u := u.l,
  have fu := funct u,
  have l_fu := fu.l,
  -- Use simp to simplify the expression
  simp [funct, l_u, l_fu],
  -- Use ring to handle arithmetic simplification
  ring,
end