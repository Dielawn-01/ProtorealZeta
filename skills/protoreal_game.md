---
name: protoreal-game
description: Rust systems architecture mapping the Protoreal manifold to the game engine logic.
---

# Protoreal Game Engine

This skill maps the abstract Protoreal Algebra and Agent Behavior into concrete software architecture using Rust.

## 1. Spatial Engine (`space.rs`)
The 35D Base Manifold and 7D Fiber are represented as highly optimized spatial structures in Rust.
- Avoid using floating-point coordinates where possible. Map algebraic constants ($a, \omega, \iota, \epsilon, \lambda$) directly into discretized grid logic or compressed bitfields.
- Implement Saeptation algorithms to handle the memory pruning of spaces that are mathematically unobservable due to finite aperture constraints.

## 2. Observer Nodes (`observer.rs`)
The 7D Observer Adapter dimensions ($\tau, \sigma, \mu, \alpha, \rho, \eta, \psi$) are instantiated as trait parameters on any game entity.
- These attributes dictate how the entity renders, moves, and interacts with the game loop.
- The product of $\tau \cdot \sigma \cdot \eta$ acts as the entity's "render distance" and update frequency (its observational aperture).

## 3. The Core Loop (`game.rs` & `lib.rs`)
The game loop is a continuous cycle of Tensor Couplings.
- Rather than standard collision detection, entities interact via topological overlap ($W_1$ distances).
- If two entities share a tight $W_1$ proximity (e.g., $W_1 < 0.1$), their logic branches intertwine, simulating the Pictet-Spengler condensation and resonance algorithms.

## Usage Guidelines
- Write highly performant, thread-safe Rust code prioritizing zero-cost abstractions.
- Translate concepts like "Topological Friction" directly into compute penalties or clock-cycles in the engine to enforce the Veblen game dynamics.
