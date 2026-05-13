pub mod protoreal;
pub mod antenna;
pub mod agent;
pub mod zeta;

use pyo3::prelude::*;
pub use crate::protoreal::ProtorealFull as ProtorealElement;
use crate::protoreal::ProtorealFull;
use crate::antenna::{calculate_jitter, bogoliubov_mixing, t_generic_protoreal};

#[pyfunction]
fn get_jitter(u: &ProtorealFull, v: &ProtorealFull, w: &ProtorealFull) -> f64 {
    calculate_jitter(*u, *v, *w)
}

#[pyfunction]
fn get_mixing(f: &ProtorealFull, b: &ProtorealFull) -> (f64, f64) {
    bogoliubov_mixing(*f, *b)
}

#[pyfunction]
fn resonance_antenna(indices: Vec<usize>, primes: Vec<f64>) -> ProtorealFull {
    t_generic_protoreal(&indices, &primes)
}

#[pymodule]
fn neuro_pharm(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ProtorealFull>()?;
    crate::agent::register_agent(m)?;
    crate::zeta::register_zeta(m)?;
    m.add_function(wrap_pyfunction!(get_jitter, m)?)?;
    m.add_function(wrap_pyfunction!(get_mixing, m)?)?;
    m.add_function(wrap_pyfunction!(resonance_antenna, m)?)?;
    Ok(())
}
