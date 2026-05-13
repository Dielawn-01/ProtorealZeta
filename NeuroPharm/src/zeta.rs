use crate::ProtorealElement;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::Bound;

#[pyclass]
pub struct ZetaScout {
    pub zeros: Vec<f64>,
}

#[pymethods]
impl ZetaScout {
    #[new]
    fn new(zeros: Vec<f64>) -> Self {
        ZetaScout { zeros }
    }

    fn find_nearest(&self, t: f64) -> (f64, f64) {
        // Binary search for the nearest zero
        let pos = self.zeros.binary_search_by(|z| z.partial_cmp(&t).unwrap());
        match pos {
            Ok(_) => (t, 0.0),
            Err(i) => {
                if i == 0 {
                    (self.zeros[0], (self.zeros[0] - t).abs())
                } else if i == self.zeros.len() {
                    (self.zeros[i - 1], (self.zeros[i - 1] - t).abs())
                } else {
                    let d1 = (self.zeros[i - 1] - t).abs();
                    let d2 = (self.zeros[i] - t).abs();
                    if d1 < d2 {
                        (self.zeros[i - 1], d1)
                    } else {
                        (self.zeros[i], d2)
                    }
                }
            }
        }
    }

    fn batch_resonance(&self, states: Vec<ProtorealElement>, jitter: f64) -> Vec<f64> {
        // High-performance batch resonance calculation
        states.iter().map(|s| {
            let res = s.standard_resonance();
            // Resonance Probability (Stochastic identity)
            (- (res * res) / (2.0 * (jitter * jitter + 1.0))).exp()
        }).collect()
    }
}

pub fn register_zeta(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ZetaScout>()?;
    Ok(())
}
