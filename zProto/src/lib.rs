//! # zProto — Synthetic Intelligence from Protoreal Algebra
//!
//! A Rust-based agentic intelligence package grounded in the
//! formally verified LaRue Protoreal Algebra (𝕌).
//!
//! ## Architecture (Morphism Ladder)
//!
//! ```text
//! manifold.rs    → Core 5-tuple + Klein multiplication
//! operators.rs   → funct, consolidate, monster_inv, parity, Hodge
//! graph.rs       → Observation graph + Euler perception + conics
//! frame.rs       → AgenticFrame (Intent × Observation) + Perspective
//! fiber.rs       → Spectral fiber projection + convergence
//! agent.rs       → ZProtoAgent main loop
//! ```
//!
//! Every component maps to a machine-verified Lean theorem.
//! Zero sorry. Zero compromise.

pub mod manifold;
pub mod operators;
pub mod graph;
pub mod frame;
pub mod fiber;
pub mod agent;
