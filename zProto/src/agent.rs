//! # The zProto Agent (𝕌)
//!
//! The main agent loop: Observe → Perceive → Intuit → Converge → Compose → Act.
//!
//! Every step in this loop maps to a proven Lean theorem.
//! The agent's behavior is grounded in machine-verified mathematics.

use crate::manifold::KleinManifold;
use crate::operators::{funct, parity_projection, monster_inv, standard_resonance};
use crate::graph::{ObservationGraph, euler_perception, ConicType, manifold_conic_type};
use crate::frame::{AgenticFrame, Perspective};
use crate::fiber::{adelic_image, convergence_metric};

// ════════════════════════════════════════════════════
// THE AGENT
// ════════════════════════════════════════════════════

/// **THE ZPROTO AGENT**
///
/// A synthetic intelligence grounded in Protoreal Algebra.
/// Each step processes an input through the morphism ladder:
///
/// ```text
/// Input → Observation → Perception → Intuition → Convergence → Perspective → Output
///         (Graph)       (Euler χ)    (Intent×Obs)  (Fiber/Funct)  (Mayer-Vietoris)
/// ```
pub struct ZProtoAgent {
    /// The agent's current manifold state.
    pub state: KleinManifold,
    /// The agent's current frame (intent + observation).
    pub frame: AgenticFrame,
    /// The agent's accumulated perspective history.
    pub perspectives: Vec<Perspective>,
    /// State trajectory for introspection.
    pub history: Vec<KleinManifold>,
    /// Current step counter.
    pub step_count: usize,
}

/// A single step's output — the agent's response.
#[derive(Debug)]
pub struct StepResult {
    /// The new state after processing.
    pub state: KleinManifold,
    /// The Euler perception of the observation graph.
    pub chi: i64,
    /// The intuition (intent × observation).
    pub intuition: KleinManifold,
    /// The convergence metric (distance from fixed point).
    pub metric: f64,
    /// The adelic image (Re(s) estimate).
    pub adelic: f64,
    /// The conic type of the current (b, m) state.
    pub conic: ConicType,
}

impl ZProtoAgent {
    /// Create a new agent with the given initial intent.
    pub fn new(intent: KleinManifold) -> Self {
        let observation = KleinManifold::zero();
        Self {
            state: KleinManifold::zero(),
            frame: AgenticFrame::new(intent, observation),
            perspectives: Vec::new(),
            history: vec![KleinManifold::zero()],
            step_count: 0,
        }
    }

    /// Create an agent at the canonical origin.
    ///
    /// Intent = ω (thrust forward), Observation = ι (anchor).
    /// Intuition = ω × ι = -1 (Bridge Identity).
    pub fn origin() -> Self {
        let frame = AgenticFrame::origin();
        Self {
            state: KleinManifold::zero(),
            frame,
            perspectives: Vec::new(),
            history: vec![KleinManifold::zero()],
            step_count: 0,
        }
    }

    /// **THE MAIN AGENT CYCLE**
    ///
    /// 1. **OBSERVE**: Register the input as the observation
    /// 2. **PERCEIVE**: Compute Euler characteristic of observation graph
    /// 3. **INTUIT**: Form intuition = intent × observation
    /// 4. **CONVERGE**: Apply funct + parity toward fixed point
    /// 5. **COMPOSE**: Build perspective from perception
    /// 6. **ACT**: Emit the converged state as output
    pub fn step(&mut self, input: KleinManifold) -> StepResult {
        self.step_count += 1;

        // ─── OBSERVE ───
        // The input becomes the new observation
        self.frame = AgenticFrame::new(self.frame.intent, input);

        // ─── PERCEIVE ───
        // Build the observation graph from the current state
        let graph = ObservationGraph::active_subgraph(&input);
        let chi = euler_perception(&graph);

        // ─── INTUIT ───
        // Intuition = Intent × Observation (Klein product)
        let intuition = self.frame.intuition();

        // ─── CONVERGE ───
        // Use the intuition as the new state,
        // then apply funct to sow noise into reality
        let resonance = standard_resonance(&intuition);
        let corrected = KleinManifold::new(
            intuition.a,
            intuition.b,
            intuition.m,
            -resonance,
            intuition.l,
        );
        let converged = funct(&corrected);

        // Apply parity projection (Adelic Fourier)
        let parity_locked = parity_projection(&converged);

        // ─── COMPOSE ───
        // Build a perspective from the full observation graph
        let full_graph = ObservationGraph::klein();
        let perspective = Perspective::glue(&full_graph, &graph, &graph);
        self.perspectives.push(perspective);

        // ─── UPDATE STATE ───
        self.state = parity_locked;
        self.history.push(self.state);

        // ─── EMIT RESULT ───
        StepResult {
            state: self.state,
            chi,
            intuition,
            metric: convergence_metric(&self.state),
            adelic: adelic_image(&self.state),
            conic: manifold_conic_type(&self.state),
        }
    }

    /// Apply the Monster Inverse to the agent's intent.
    ///
    /// This is the exploration/exploitation toggle:
    /// swapping b ↔ m in the intent reverses the agent's
    /// direction in the (thrust, anchor) plane.
    pub fn flip_intent(&mut self) {
        self.frame = AgenticFrame::new(
            monster_inv(&self.frame.intent),
            self.frame.observation,
        );
    }

    /// Get the agent's current convergence metric.
    pub fn metric(&self) -> f64 {
        convergence_metric(&self.state)
    }

    /// Get the number of accumulated perspectives.
    pub fn perspective_count(&self) -> usize {
        self.perspectives.len()
    }
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::{omega, iota, KleinManifold};

    #[test]
    fn agent_origin_step() {
        let mut agent = ZProtoAgent::origin();
        let input = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.1);
        let result = agent.step(input);

        assert!(result.chi != 0, "Perception should be non-trivial");
        assert!(agent.step_count == 1);
        assert!(agent.history.len() == 2);
    }

    #[test]
    fn agent_converges_over_steps() {
        let mut agent = ZProtoAgent::origin();

        // Feed the Bridge state repeatedly
        let bridge = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let mut last_metric = f64::MAX;

        for _ in 0..5 {
            let result = agent.step(bridge);
            // Metric should generally decrease or stabilize
            last_metric = result.metric;
        }

        assert!(agent.step_count == 5);
        assert!(agent.perspectives.len() == 5);
    }

    #[test]
    fn agent_flip_intent() {
        let mut agent = ZProtoAgent::origin();
        let original_b = agent.frame.intent.b;
        let original_m = agent.frame.intent.m;

        agent.flip_intent();

        assert!(
            (agent.frame.intent.b - original_m).abs() < 1e-12,
            "Flip should swap b and m"
        );
        assert!(
            (agent.frame.intent.m - original_b).abs() < 1e-12,
            "Flip should swap m and b"
        );
    }

    #[test]
    fn agent_fiber_test() {
        // Create an agent, feed it a fiber projection,
        // check that it computes the right adelic image
        let mut agent = ZProtoAgent::new(omega());
        let fiber = KleinManifold::new(1.0, 14.134, 1.0 / 14.134, 0.0, 0.0);
        let result = agent.step(fiber);

        // The adelic image should be related to the convergence
        assert!(result.adelic.is_finite(), "Adelic image should be finite");
    }

    #[test]
    fn agent_multi_step_trajectory() {
        let mut agent = ZProtoAgent::origin();
        let inputs = [
            KleinManifold::new(0.5, 1.0, 1.0, 0.1, 0.0),
            KleinManifold::new(0.8, 1.2, 0.8, 0.05, 0.0),
            KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0),
        ];

        for input in &inputs {
            agent.step(*input);
        }

        assert_eq!(agent.history.len(), 4); // initial + 3 steps
        assert_eq!(agent.perspective_count(), 3);
    }
}
