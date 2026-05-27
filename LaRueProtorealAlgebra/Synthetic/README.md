# Synthetic Proofs (Machine-Generated Staging)

Proofs in this directory were autonomously discovered by zBuddy
(zbuddy-gen, 8B LLM) using a tactic-level REPL against the Protoreal lake.

## Workflow

1. zBuddy proves -> proof written to zbuddy_proofs.lean (InfoPhys)
2. Staged here -> deduplicated, annotated with discovery metadata
3. Reviewed -> human checks for novelty, correctness, and insight
4. Promoted -> moved to LaRueProtorealAlgebra/ZBuddyVerified.lean (in lake)

## Status

Proofs here are lake-verified (they compile) but NOT imported by
any other lake file. They exist in quarantine until promoted.
