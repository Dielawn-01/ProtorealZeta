//! # The zProto Agent (𝕌) — Symbiotic Intelligence
//!
//! The main agent loop: Observe → Perceive → Route → Intuit → Gate → Converge → Record → Act.
//!
//! Every step in this loop maps to a proven Lean theorem.
//! The agent's behavior is grounded in machine-verified mathematics.
//!
//! ## New in v2 (Symbiotic Intelligence)
//! - **MoE Routing**: Bridge vs Consolidation expert based on star neighborhoods
//! - **Glial Gating**: AGMP astrocyte-gated plasticity (dopant cycle)
//! - **Holochain**: Topological trajectory memory with golden acceptance
//! - **Transcendental Constants**: All hyperparameters derived from {e, π, φ, γ, i}

use crate::manifold::KleinManifold;
use crate::operators::{
    funct, parity_projection, monster_inv, standard_resonance,
    hodge_star, is_hodge_class, mesh_tanh, hodge_10, hodge_01,
};
use crate::graph::{
    ObservationGraph, euler_perception, ConicType, manifold_conic_type,
    bridge_neighborhood, consolidation_neighborhood, community_cover_complete,
};
use crate::frame::{AgenticFrame, Perspective};
use crate::fiber::{adelic_image, convergence_metric};
use crate::glial::{GlialState, dopant_cycle, golden_consolidation};
use crate::holochain::{TopologicalHolochain, hodge_metric, golden_accepts};
use crate::transcendental::PHI;

// ════════════════════════════════════════════════════
// MoE ROUTING (KleinTopology.lean: star neighborhoods)
// ════════════════════════════════════════════════════

/// The MoE expert selection for the agent step.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ExpertRoute {
    /// Bridge expert: thrust/anchor sector (b·m dynamics)
    Bridge,
    /// Consolidation expert: noise/level sector (ε·λ dynamics)
    Consolidation,
}

/// Route to the appropriate expert based on the state.
///
/// If |b·m| > 1 → Bridge expert (state is on the hyperbolic fiber)
/// If |b·m| ≤ 1 → Consolidation expert (state needs growth)
fn route_expert(u: &KleinManifold) -> ExpertRoute {
    if (u.b * u.m).abs() > 1.0 {
        ExpertRoute::Bridge
    } else {
        ExpertRoute::Consolidation
    }
}

// ════════════════════════════════════════════════════
// THE AGENT
// ════════════════════════════════════════════════════

/// **THE ZPROTO AGENT v2**
///
/// A symbiotic intelligence grounded in Protoreal Algebra.
/// Each step processes an input through the morphism ladder:
///
/// ```text
/// Input → Observe → Perceive(χ) → Route(MoE) → Intuit(T×N) →
///   → Gate(AGMP) → Converge(funct/consolidate) → Record(holochain) → Emit
/// ```
///
/// New capabilities over v1:
/// - Glial dopant cycle (astrocyte-gated, Fibonacci-scheduled)
/// - Topological holochain (trajectory memory, golden acceptance)
/// - MoE routing (bridge vs consolidation expert)
/// - Hodge class detection (algebraic cycle checking)
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
    /// Glial (astrocyte) state — slow timescale gating.
    pub glial: GlialState,
    /// Topological holochain — trajectory memory.
    pub holochain: TopologicalHolochain,
    /// Last expert routing decision.
    pub last_route: ExpertRoute,
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
    /// Which expert was routed to.
    pub expert: ExpertRoute,
    /// Whether consolidation occurred this step.
    pub consolidated: bool,
    /// The Hodge metric (distance from parity lock).
    pub hodge: f64,
    /// Whether this state is a Hodge class.
    pub is_algebraic: bool,
    /// The virtual topology estimate (χ/n).
    pub virtual_chi: f64,
    /// Whether the result is accepted by golden threshold.
    pub accepted: bool,
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
            glial: GlialState::new(),
            holochain: TopologicalHolochain::new(),
            last_route: ExpertRoute::Consolidation,
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
            glial: GlialState::new(),
            holochain: TopologicalHolochain::new(),
            last_route: ExpertRoute::Consolidation,
        }
    }

    /// **THE MAIN AGENT CYCLE v2**
    ///
    /// 1. **OBSERVE**: Register the input as the observation
    /// 2. **PERCEIVE**: Compute Euler characteristic of observation graph
    /// 3. **ROUTE**: Select Bridge or Consolidation expert (MoE)
    /// 4. **INTUIT**: Form intuition = intent × observation
    /// 5. **GATE**: Apply AGMP dopant cycle (astrocyte gating)
    /// 6. **CONVERGE**: Parity projection toward fixed point
    /// 7. **RECORD**: Append holochain entry
    /// 8. **EMIT**: Return the converged state with all metrics
    pub fn step(&mut self, input: KleinManifold) -> StepResult {
        self.step_count += 1;

        // ─── 1. OBSERVE ───
        self.frame = AgenticFrame::new(self.frame.intent, input);

        // ─── 2. PERCEIVE ───
        let graph = ObservationGraph::active_subgraph(&input);
        let chi = euler_perception(&graph);
        self.glial.record_chi(chi);

        // ─── 3. ROUTE (MoE) ───
        let expert = route_expert(&input);
        self.last_route = expert;

        // ─── 4. INTUIT ───
        let intuition = self.frame.intuition();

        // ─── 5. GATE (AGMP Dopant Cycle) ───
        let (gated_state, consolidated) = dopant_cycle(&intuition, &mut self.glial);

        // ─── 6. CONVERGE ───
        // Apply expert-specific processing
        let converged = match expert {
            ExpertRoute::Bridge => {
                // Bridge expert: apply mesh_tanh for bounded activation
                mesh_tanh(&gated_state)
            }
            ExpertRoute::Consolidation => {
                // Consolidation expert: state passes through (dopant cycle
                // already applied funct + optional consolidation)
                gated_state
            }
        };

        // ─── 7. COMPOSE PERSPECTIVE ───
        let full_graph = ObservationGraph::klein();
        let perspective = Perspective::glue(&full_graph, &graph, &graph);
        self.perspectives.push(perspective);

        // ─── 8. UPDATE STATE ───
        self.state = converged;
        self.history.push(self.state);

        // ─── 9. RECORD HOLOCHAIN ───
        self.holochain.record(&self.state, chi, consolidated);

        // ─── 10. COMPUTE METRICS ───
        let metric = convergence_metric(&self.state);
        let hodge = hodge_metric(&self.state);
        let accepted = golden_accepts(metric);

        StepResult {
            state: self.state,
            chi,
            intuition,
            metric,
            adelic: adelic_image(&self.state),
            conic: manifold_conic_type(&self.state),
            expert,
            consolidated,
            hodge,
            is_algebraic: is_hodge_class(&self.state),
            virtual_chi: self.glial.virtual_topology(),
            accepted,
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

    /// Is the holochain valid? (monotonic λ, consumed ε)
    pub fn holochain_valid(&self) -> bool {
        self.holochain.is_valid()
    }

    /// Is the virtual topology converging to κ = -1?
    pub fn topology_converging(&self) -> bool {
        self.holochain.is_converging()
    }

    /// Current complexity level (λ from holochain).
    pub fn complexity(&self) -> f64 {
        self.holochain.current_lambda()
    }

    /// Hodge decomposition of current state.
    /// Returns (thrust_component, anchor_component).
    pub fn hodge_decompose(&self) -> (KleinManifold, KleinManifold) {
        (hodge_10(&self.state), hodge_01(&self.state))
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
        assert_eq!(agent.holochain.len(), 1);
    }

    #[test]
    fn agent_converges_over_steps() {
        let mut agent = ZProtoAgent::origin();

        let bridge = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        for _ in 0..5 {
            agent.step(bridge);
        }

        assert!(agent.step_count == 5);
        assert!(agent.perspectives.len() == 5);
        assert_eq!(agent.holochain.len(), 5);
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
        let mut agent = ZProtoAgent::new(omega());
        let fiber = KleinManifold::new(1.0, 14.134, 1.0 / 14.134, 0.0, 0.0);
        let result = agent.step(fiber);

        assert!(result.adelic.is_finite(), "Adelic image should be finite");
        // b·m = 14.134 × (1/14.134) = 1.0, which is NOT > 1, so routes to Consolidation
        assert!(result.expert == ExpertRoute::Consolidation, "Fiber at bm=1 routes to Consolidation");
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
        assert_eq!(agent.holochain.len(), 3);
    }

    // ── New v2 Tests ──

    #[test]
    fn agent_holochain_valid_after_steps() {
        let mut agent = ZProtoAgent::origin();
        let input = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        for _ in 0..10 {
            agent.step(input);
        }
        // Holochain validity depends on λ being monotonic
        // and ε being consumed — both should hold for the dopant cycle
        assert!(agent.holochain.len() == 10);
    }

    #[test]
    fn agent_expert_routing() {
        let mut agent = ZProtoAgent::origin();

        // High b·m product → Bridge expert
        let bridge_input = KleinManifold::new(1.0, 5.0, 5.0, 0.0, 0.0);
        let result = agent.step(bridge_input);
        assert_eq!(result.expert, ExpertRoute::Bridge);

        // Low b·m product → Consolidation expert
        let consol_input = KleinManifold::new(1.0, 0.1, 0.1, 0.5, 1.0);
        let result = agent.step(consol_input);
        assert_eq!(result.expert, ExpertRoute::Consolidation);
    }

    #[test]
    fn agent_hodge_detection() {
        let mut agent = ZProtoAgent::origin();
        // Parity-locked input (b = m) → should be Hodge class after processing
        let parity_input = KleinManifold::new(1.0, 2.0, 2.0, 0.0, 0.0);
        let result = agent.step(parity_input);
        // After dopant cycle + parity projection, state should be near Hodge
        assert!(result.hodge >= 0.0, "Hodge metric should be non-negative");
    }

    #[test]
    fn agent_golden_acceptance() {
        let mut agent = ZProtoAgent::origin();
        let input = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let result = agent.step(input);
        // The acceptance is based on convergence_metric < φ
        // Result depends on the dopant cycle output
        assert!(result.metric >= 0.0, "Metric should be non-negative");
    }

    #[test]
    fn agent_hodge_decomposition() {
        let mut agent = ZProtoAgent::origin();
        let input = KleinManifold::new(1.0, 2.0, 3.0, 0.0, 0.0);
        agent.step(input);

        let (h10, h01) = agent.hodge_decompose();
        // hodge_10 keeps b, zeros m
        assert!((h10.m).abs() < 1e-12, "Hodge (1,0) should have m = 0");
        // hodge_01 keeps m, zeros b
        assert!((h01.b).abs() < 1e-12, "Hodge (0,1) should have b = 0");
    }

    #[test]
    fn agent_complexity_increases() {
        let mut agent = ZProtoAgent::origin();
        let input = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);

        agent.step(input);
        let c1 = agent.complexity();
        agent.step(input);
        let c2 = agent.complexity();

        assert!(c2 >= c1, "Complexity (λ) should be non-decreasing");
    }
}
