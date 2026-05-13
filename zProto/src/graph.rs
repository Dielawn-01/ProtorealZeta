//! # Observation Graph & Perception (𝕌 → Graph → ℤ)
//!
//! Transcription of `ProtorealGraph.lean` and `EulerPerception.lean`.
//!
//! ## The Morphism Ladder
//! - **Observation**: KleinManifold → SimpleGraph(Fin 5) via Klein adjacency
//! - **Perception**: Graph → ℤ via Euler characteristic (χ = |V| - |E|)
//!
//! ## The Conic Discriminant (SpectralFiber.lean)
//! - Δ = B² - 4AC classifies (b,m) conics

use crate::manifold::KleinManifold;

// ════════════════════════════════════════════════════
// OBSERVATION GRAPH (ProtorealGraph.lean)
// ════════════════════════════════════════════════════

/// The 5×5 adjacency matrix for the Klein interaction graph.
///
/// Components are indexed as:
///   0 = a (real), 1 = b (thrust), 2 = m (anchor),
///   3 = e (noise), 4 = l (level)
///
/// Adjacency is determined by which pairs interact in Klein multiplication:
///   - (0,1), (0,2), (0,3), (0,4): a couples to everything linearly
///   - (1,2): thrust-anchor Bridge (b·m terms in a-component)
///   - (3,4): noise-level consolidation (e·l terms in a-component)
///
/// NOT adjacent: (1,3), (1,4), (2,3), (2,4) — no direct coupling
pub struct ObservationGraph {
    /// 5×5 symmetric adjacency matrix (upper triangle)
    adj: [[bool; 5]; 5],
}

impl ObservationGraph {
    /// Construct the canonical Klein observation graph.
    ///
    /// This is the graph whose Euler characteristic equals
    /// the curvature κ = -1.
    pub fn klein() -> Self {
        let mut adj = [[false; 5]; 5];

        // a couples to all basis elements
        adj[0][1] = true; adj[1][0] = true; // a-ω
        adj[0][2] = true; adj[2][0] = true; // a-ι
        adj[0][3] = true; adj[3][0] = true; // a-ε
        adj[0][4] = true; adj[4][0] = true; // a-λ

        // Bridge coupling: ω-ι
        adj[1][2] = true; adj[2][1] = true;

        // Consolidation coupling: ε-λ
        adj[3][4] = true; adj[4][3] = true;

        Self { adj }
    }

    /// Check if two components are adjacent.
    pub fn is_adj(&self, i: usize, j: usize) -> bool {
        i < 5 && j < 5 && self.adj[i][j]
    }

    /// Count the number of vertices (always 5 for Klein).
    pub fn vertex_count(&self) -> i64 {
        5
    }

    /// Count the number of edges.
    pub fn edge_count(&self) -> i64 {
        let mut count = 0i64;
        for i in 0..5 {
            for j in (i + 1)..5 {
                if self.adj[i][j] {
                    count += 1;
                }
            }
        }
        count
    }

    /// Construct a subgraph from only the active components.
    ///
    /// A component is "active" if its value is non-zero in the
    /// given manifold state.
    pub fn active_subgraph(u: &KleinManifold) -> Self {
        let active = [
            u.a.abs() > 1e-12,
            u.b.abs() > 1e-12,
            u.m.abs() > 1e-12,
            u.e.abs() > 1e-12,
            u.l.abs() > 1e-12,
        ];
        let full = Self::klein();
        let mut adj = [[false; 5]; 5];
        for i in 0..5 {
            for j in 0..5 {
                adj[i][j] = full.adj[i][j] && active[i] && active[j];
            }
        }
        Self { adj }
    }
}

// ════════════════════════════════════════════════════
// EULER PERCEPTION (EulerPerception.lean)
// ════════════════════════════════════════════════════

/// **EULER PERCEPTION**: χ = |V| - |E|
///
/// The topological invariant of the observation graph.
/// For the full Klein graph: χ = 5 - 6 = -1 = κ
pub fn euler_perception(g: &ObservationGraph) -> i64 {
    g.vertex_count() - g.edge_count()
}

// ════════════════════════════════════════════════════
// CONIC DISCRIMINANT (SpectralFiber.lean)
// ════════════════════════════════════════════════════

/// The conic type in (b, m) space.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ConicType {
    Hyperbolic,  // Δ > 0 (Bridge: bm = 1)
    Degenerate,  // Δ = 0 (Parity: b = m)
    Elliptic,    // Δ < 0 (Thrust coupling: b² + m² = r²)
}

/// **CONIC DISCRIMINANT**: Δ = B² - 4AC
///
/// Classifies the general conic Ab² + Bbm + Cm² = D.
pub fn conic_discriminant(a_coeff: f64, b_coeff: f64, c_coeff: f64) -> f64 {
    b_coeff.powi(2) - 4.0 * a_coeff * c_coeff
}

/// Classify a conic by its discriminant.
pub fn classify_conic(a_coeff: f64, b_coeff: f64, c_coeff: f64) -> ConicType {
    let delta = conic_discriminant(a_coeff, b_coeff, c_coeff);
    if delta > 1e-12 {
        ConicType::Hyperbolic
    } else if delta.abs() < 1e-12 {
        ConicType::Degenerate
    } else {
        ConicType::Elliptic
    }
}

/// Classify the (b, m) state of a manifold element.
///
/// Returns the conic type based on the relationship between b and m.
pub fn manifold_conic_type(u: &KleinManifold) -> ConicType {
    let bm = u.b * u.m;
    let diff = (u.b - u.m).abs();

    if diff < 1e-12 && (bm - 1.0).abs() < 1e-12 {
        // At fixed point: b = m and bm = 1
        ConicType::Degenerate
    } else if (bm - 1.0).abs() < 1e-12 {
        // On hyperbola: bm = 1 but b ≠ m
        ConicType::Hyperbolic
    } else if diff < 1e-12 {
        // On parity line: b = m but bm ≠ 1
        ConicType::Elliptic
    } else {
        // General position
        ConicType::Hyperbolic
    }
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::KleinManifold;

    // ── Observation Graph (ProtorealGraph.lean) ──
    #[test]
    fn full_graph_has_6_edges() {
        let g = ObservationGraph::klein();
        assert_eq!(g.edge_count(), 6, "Klein graph should have 6 edges");
    }

    #[test]
    fn full_graph_has_5_vertices() {
        let g = ObservationGraph::klein();
        assert_eq!(g.vertex_count(), 5, "Klein graph should have 5 vertices");
    }

    #[test]
    fn bridge_adjacency() {
        let g = ObservationGraph::klein();
        assert!(g.is_adj(1, 2), "thrust-anchor should be adjacent (Bridge)");
    }

    #[test]
    fn consolidation_adjacency() {
        let g = ObservationGraph::klein();
        assert!(g.is_adj(3, 4), "noise-level should be adjacent (Consolidation)");
    }

    #[test]
    fn thrust_noise_not_adjacent() {
        let g = ObservationGraph::klein();
        assert!(!g.is_adj(1, 3), "thrust-noise should NOT be adjacent");
    }

    // ── Euler Perception (EulerPerception.lean: curvature_is_perception) ──
    #[test]
    fn euler_is_neg_one() {
        let g = ObservationGraph::klein();
        let chi = euler_perception(&g);
        assert_eq!(chi, -1, "Euler perception should be -1 = κ");
    }

    // ── Active Subgraph ──
    #[test]
    fn subgraph_of_bridge_state() {
        // Only a, b, m active (bridge state)
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.0, 0.0);
        let g = ObservationGraph::active_subgraph(&u);
        assert_eq!(g.edge_count(), 3, "Bridge subgraph: a-b, a-m, b-m");
        assert_eq!(
            euler_perception(&g),
            5 - 3, // V=5 (graph always has 5 vertices), E=3
            "Bridge subgraph χ = 2"
        );
    }

    // ── Conic Discriminant (SpectralFiber.lean) ──
    #[test]
    fn bridge_is_hyperbolic() {
        let delta = conic_discriminant(0.0, 1.0, 0.0);
        assert!(
            (delta - 1.0).abs() < 1e-12,
            "Bridge: Δ = 1 (hyperbolic)"
        );
        assert_eq!(classify_conic(0.0, 1.0, 0.0), ConicType::Hyperbolic);
    }

    #[test]
    fn parity_is_degenerate() {
        let delta = conic_discriminant(1.0, -2.0, 1.0);
        assert!(
            delta.abs() < 1e-12,
            "Parity: Δ = 0 (degenerate)"
        );
        assert_eq!(classify_conic(1.0, -2.0, 1.0), ConicType::Degenerate);
    }

    #[test]
    fn thrust_coupling_is_elliptic() {
        let delta = conic_discriminant(1.0, 0.0, 1.0);
        assert!(
            (delta - (-4.0)).abs() < 1e-12,
            "Thrust: Δ = -4 (elliptic)"
        );
        assert_eq!(classify_conic(1.0, 0.0, 1.0), ConicType::Elliptic);
    }

    #[test]
    fn discriminant_trichotomy_sum() {
        let d1 = conic_discriminant(0.0, 1.0, 0.0);  // +1
        let d2 = conic_discriminant(1.0, -2.0, 1.0);  // 0
        let d3 = conic_discriminant(1.0, 0.0, 1.0);   // -4
        assert!(
            (d1 + d2 + d3 - (-3.0)).abs() < 1e-12,
            "Sum of discriminants should be -3"
        );
    }
}
