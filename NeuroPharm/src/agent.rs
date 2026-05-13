use crate::ProtorealElement;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::Bound;

#[pyclass]
pub struct AgenticFrame {
    #[pyo3(get)]
    pub intent: ProtorealElement,
    #[pyo3(get)]
    pub observation: ProtorealElement,
    #[pyo3(get)]
    pub intuition: ProtorealElement,
}

#[pymethods]
impl AgenticFrame {
    #[new]
    #[pyo3(signature = (intent, observation=None))]
    fn new(intent: ProtorealElement, observation: Option<ProtorealElement>) -> Self {
        let obs = observation.unwrap_or(ProtorealElement::new(0.0, 0.0, 0.0, 0.0, 0.0));
        let int = intent * obs;
        AgenticFrame {
            intent,
            observation: obs,
            intuition: int,
        }
    }

    fn get_protoreal_resonance(&self) -> f64 {
        let total = self.intent + self.observation + self.intuition;
        total.norm() // Verified Adelic Norm
    }

    fn get_uncomplex_phase(&self) -> (f64, f64) {
        let u = self.intent + self.observation + self.intuition;
        let phi = u.phase(); // Verified Spectral Phase
        (phi.cos(), phi.sin())
    }

    /// Generational Shift: Consolidates the agent's frame.
    pub fn shift(&mut self) {
        self.intent = self.intent.consolidate();
        self.observation = self.observation.consolidate();
        self.intuition = self.intent * self.observation;
    }

    /// Sow: Manifests the agent's exploration noise into reality.
    pub fn sow(&mut self) {
        self.intent = self.intent.funct();
        self.observation = self.observation.funct();
        self.intuition = self.intent * self.observation;
    }
}

#[pyfunction]
fn calculate_mu(rho: f64, eps: ProtorealElement, omega: ProtorealElement) -> ProtorealElement {
    // μ = ε * ρ * ω
    let rho_elem = ProtorealElement::new(rho, 0.0, 0.0, 0.0, 0.0);
    eps * rho_elem * omega
}

pub fn register_agent(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AgenticFrame>()?;
    m.add_function(wrap_pyfunction!(calculate_mu, m)?)?;
    Ok(())
}
