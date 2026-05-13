use std::ops::{Add, Sub, Mul, Neg};
use pyo3::prelude::*;

#[pyclass]
#[derive(Debug, Clone, Copy)]
pub struct ProtorealFull {
    #[pyo3(get, set)]
    pub a: f64, // Real Base
    #[pyo3(get, set)]
    pub b: f64, // Thrust (omega)
    #[pyo3(get, set)]
    pub m: f64, // Anchor (iota)
    #[pyo3(get, set)]
    pub e: f64, // Noise (epsilon)
    #[pyo3(get, set)]
    pub l: f64, // Consolidation (lambda)
}

#[pymethods]
impl ProtorealFull {
    #[new]
    #[pyo3(signature = (a=0.0, b=0.0, m=0.0, e=0.0, l=0.0))]
    pub fn new(a: f64, b: f64, m: f64, e: f64, l: f64) -> Self {
        ProtorealFull { a, b, m, e, l }
    }

    pub fn __repr__(&self) -> String {
        format!("𝕌({:.4}, {:.4}ω, {:.4}ι, {:.4}ε, {:.4}λ)", self.a, self.b, self.m, self.e, self.l)
    }

    pub fn __add__(&self, other: ProtorealFull) -> ProtorealFull {
        *self + other
    }

    pub fn __sub__(&self, other: ProtorealFull) -> ProtorealFull {
        *self - other
    }

    pub fn __mul__(&self, other: ProtorealFull) -> ProtorealFull {
        *self * other
    }

    pub fn __neg__(&self) -> ProtorealFull {
        -*self
    }

    /// Sowing: Converts noise (potential) into reality (base).
    pub fn funct(&self) -> ProtorealFull {
        ProtorealFull {
            a: self.a + self.e,
            b: self.b,
            m: self.m,
            e: 0.0,
            l: self.l + 1.0,
        }
    }

    /// Consolidation: Promotes weights and seeds new noise.
    pub fn consolidate(&self) -> ProtorealFull {
        ProtorealFull {
            a: self.a * 2.0,
            b: self.b,
            m: self.m * 2.0,
            e: self.e + 1.0,
            l: self.l,
        }
    }

    pub fn norm(&self) -> f64 {
        (self.a.powi(2) + self.b.powi(2) + self.m.powi(2) + self.e.powi(2) + self.l.powi(2)).sqrt()
    }

    pub fn phase(&self) -> f64 {
        self.a - self.b * self.m
    }

    pub fn standard_resonance(&self) -> f64 {
        self.phase()
    }

    pub fn idempotent_tanh(&self) -> ProtorealFull {
        ProtorealFull {
            a: self.a.tanh(),
            b: self.b.tanh(),
            m: self.m.tanh(),
            e: self.e.tanh(),
            l: self.l.tanh(),
        }
    }

    #[staticmethod]
    pub fn curvature(u: &ProtorealFull, v: &ProtorealFull, w: &ProtorealFull) -> ProtorealFull {
        (*u * *v) * *w - *u * (*v * *w)
    }

    pub fn r4_reflection(&self) -> ProtorealFull {
        ProtorealFull {
            a: self.a,
            b: self.b,
            m: -self.m,
            e: self.e,
            l: self.l,
        }
    }
}

impl Add for ProtorealFull {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        ProtorealFull {
            a: self.a + other.a,
            b: self.b + other.b,
            m: self.m + other.m,
            e: self.e + other.e,
            l: self.l + other.l,
        }
    }
}

impl Sub for ProtorealFull {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        ProtorealFull {
            a: self.a - other.a,
            b: self.b - other.b,
            m: self.m - other.m,
            e: self.e - other.e,
            l: self.l - other.l,
        }
    }
}

impl Neg for ProtorealFull {
    type Output = Self;
    fn neg(self) -> Self {
        ProtorealFull {
            a: -self.a,
            b: -self.b,
            m: -self.m,
            e: -self.e,
            l: -self.l,
        }
    }
}

impl Mul for ProtorealFull {
    type Output = Self;
    fn mul(self, other: Self) -> Self {
        // ANTI-COMMUTATIVE BRIDGE MULTIPLICATION
        // w*i = -1, i*w = +1, l*e = 1, e*l = -1
        let ra = self.a * other.a - self.b * other.m + self.m * other.b + self.l * other.e - self.e * other.l;
        let rb = self.a * other.b + self.b * other.a + self.b * other.b;
        let rm = self.a * other.m + self.m * other.a;
        let re = self.a * other.e + self.e * other.a;
        let rl = self.a * other.l + self.l * other.a;
        
        ProtorealFull { a: ra, b: rb, m: rm, e: re, l: rl }
    }
}
