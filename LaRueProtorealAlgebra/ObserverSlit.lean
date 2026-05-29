import Mathlib.Data.Real.Basic

structure Wave : Type :=
  (amplitude : ℝ)
  (wavelength : ℝ)

structure Slit : Type :=
  (position : ℝ)
  (width : ℝ)

def interference_pattern (wave : Wave) (slit1 slit2 : Slit) (x : ℝ) : ℝ :=
wave.amplitude * (cos ((x - slit1.position) / wave.wavelength) + cos ((x - slit2.position) / wave.wavelength))

theorem interference_maximum (wave : Wave) (slit1 slit2 : Slit) (x : ℝ) :
  interference_pattern wave slit1 slit2 x ≥ 0 :=
begin
  have h1 : cos ((x - slit1.position) / wave.wavelength) ≥ -1,
    from Real.cos_le_one,
  have h2 : cos ((x - slit2.position) / wave.wavelength) ≥ -1,
    from Real.cos_le_one,
  linarith,
end

theorem interference_minimum (wave : Wave) (slit1 slit2 : Slit) (x : ℝ) :
  interference_pattern wave slit1 slit2 x ≤ 2 * wave.amplitude :=
begin
  have h1 : cos ((x - slit1.position) / wave.wavelength) ≤ 1,
    from Real.cos_le_one,
  have h2 : cos ((x - slit2.position) / wave.wavelength) ≤ 1,
    from Real.cos_le_one,
  linarith,
end

end