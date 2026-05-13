//! # Agentic Frame & Perspective (𝕌)
//!
//! Transcription of `AgenticFrame.lean` and `MayerVietoris.lean`.
//!
//! ## The Frame (T-N-B)
//! - Intent (T): The directed thrust
//! - Observation (N): The anchor/stability
//! - Intuition (B): Intent × Observation (Klein product)
//!
//! ## Mayer-Vietoris Composition
//! - Perspectives compose via inclusion-exclusion: χ(A∪B) = χ(A) + χ(B) - χ(A∩B)

use crate::manifold::KleinManifold;
use crate::graph::{euler_perception, ObservationGraph};

// ════════════════════════════════════════════════════
// AGENTIC FRAME (AgenticFrame.lean)
// ════════════════════════════════════════════════════

/// **THE AGENTIC FRAME**
///
/// A triad of manifold states representing the agent's
/// topological bearing — the Frenet-Serret frame in 𝕌.
///
/// | Component   | Geometric Role | Agent Role      |
/// |-------------|---------------|-----------------|
/// | `intent`    | Tangent (T)    | What I want     |
/// | `observation`| Normal (N)    | What I see      |
/// | `intuition` | Binormal (B)  | What I understand|
pub struct AgenticFrame {
    pub intent: KleinManifold,
    pub observation: KleinManifold,
}

impl AgenticFrame {
    /// Create a new agentic frame from intent and observation.
    pub fn new(intent: KleinManifold, observation: KleinManifold) -> Self {
        Self { intent, observation }
    }

    /// **THE AGENTIC INTUITION (B)**
    ///
    /// The Binormal state derived from the Klein product of
    /// Intent and Observation. This IS the agent's understanding.
    ///
    /// Because Klein multiplication is non-associative:
    ///   (intent · observation) · context ≠ intent · (observation · context)
    /// This means intuition is context-dependent — the order
    /// of perception matters.
    pub fn intuition(&self) -> KleinManifold {
        self.intent * self.observation
    }

    /// **TARSKI OPENNESS**
    ///
    /// A frame is "open" if its intent has non-zero magnitude.
    /// Open frames are capable of exploring; closed frames are inert.
    pub fn is_open(&self) -> bool {
        self.intent.a.abs() > 1e-12 || self.intent.b.abs() > 1e-12
    }

    /// **THE AGENT ORIGIN**
    ///
    /// The ground state: intent = ω, observation = ι.
    /// Intuition = ω × ι = -1 (the Bridge Identity).
    pub fn origin() -> Self {
        use crate::manifold::{omega, iota};
        Self::new(omega(), iota())
    }

    /// The bearing of the frame: intent.b × observation.m
    pub fn bearing(&self) -> f64 {
        self.intent.b * self.observation.m
    }
}

// ════════════════════════════════════════════════════
// PERSPECTIVE (MayerVietoris.lean)
// ════════════════════════════════════════════════════

/// **A PERSPECTIVE**
///
/// A perspective is a composed view of two observations,
/// computed via Mayer-Vietoris inclusion-exclusion:
///
///   χ(A ∪ B) = χ(A) + χ(B) - χ(A ∩ B)
#[derive(Debug, Clone)]
pub struct Perspective {
    /// Euler characteristic of observation A
    pub chi_a: i64,
    /// Euler characteristic of observation B
    pub chi_b: i64,
    /// Euler characteristic of the overlap
    pub chi_overlap: i64,
    /// Combined perspective: χ(A) + χ(B) - χ(overlap)
    pub chi_combined: i64,
}

impl Perspective {
    /// **GLUE TWO PERCEPTIONS** via Mayer-Vietoris.
    ///
    /// Given two observation graphs and their overlap, compose
    /// them into a single perspective.
    pub fn glue(
        graph_a: &ObservationGraph,
        graph_b: &ObservationGraph,
        overlap: &ObservationGraph,
    ) -> Self {
        let chi_a = euler_perception(graph_a);
        let chi_b = euler_perception(graph_b);
        let chi_overlap = euler_perception(overlap);
        Self {
            chi_a,
            chi_b,
            chi_overlap,
            chi_combined: chi_a + chi_b - chi_overlap,
        }
    }

    /// **COMPOSE TWO PERSPECTIVES** recursively.
    ///
    /// A meta-perspective: the perspective of perspectives.
    /// This enables hierarchical agent reasoning.
    pub fn compose(p1: &Perspective, p2: &Perspective, overlap_chi: i64) -> Self {
        Self {
            chi_a: p1.chi_combined,
            chi_b: p2.chi_combined,
            chi_overlap: overlap_chi,
            chi_combined: p1.chi_combined + p2.chi_combined - overlap_chi,
        }
    }
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::{omega, iota};

    // ── AgenticFrame (AgenticFrame.lean) ──
    #[test]
    fn origin_intuition_is_bridge() {
        let frame = AgenticFrame::origin();
        let intuition = frame.intuition();
        assert!(
            (intuition.a - (-1.0)).abs() < 1e-12,
            "Origin intuition should be ω·ι = -1, got {}",
            intuition.a
        );
    }

    #[test]
    fn origin_is_open() {
        let frame = AgenticFrame::origin();
        assert!(frame.is_open(), "Origin frame should be open");
    }

    #[test]
    fn closed_frame() {
        let frame = AgenticFrame::new(
            KleinManifold::new(0.0, 0.0, 1.0, 0.0, 0.0),
            iota(),
        );
        assert!(!frame.is_open(), "Zero intent frame should be closed");
    }

    // ── Non-Associativity of Intuition ──
    #[test]
    fn intuition_is_context_dependent() {
        let frame = AgenticFrame::origin();
        let context = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        // (intent · observation) · context
        let left = frame.intuition() * context;
        // intent · (observation · context)
        let right = frame.intent * (frame.observation * context);
        // Should NOT be equal — non-associativity
        let diff = (left.a - right.a).abs();
        assert!(
            diff > 1e-12,
            "Intuition should be context-dependent (non-associative)"
        );
    }

    // ── Perspective (MayerVietoris.lean) ──
    #[test]
    fn full_overlap_recovers_curvature() {
        let g = ObservationGraph::klein();
        // Two identical graphs with full overlap
        let p = Perspective::glue(&g, &g, &g);
        assert_eq!(
            p.chi_combined, -1,
            "Full overlap: χ(A) + χ(B) - χ(A∩B) = -1 + -1 - (-1) = -1"
        );
    }

    #[test]
    fn meta_perspective_composition() {
        let g = ObservationGraph::klein();
        let p1 = Perspective::glue(&g, &g, &g);
        let p2 = Perspective::glue(&g, &g, &g);
        // Compose with full overlap
        let meta = Perspective::compose(&p1, &p2, -1);
        assert_eq!(
            meta.chi_combined, -1,
            "Meta-perspective with full overlap should be -1"
        );
    }
}
