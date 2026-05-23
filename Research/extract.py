import json
with open("/home/phrxmaz/Documents/Protoreal_Zeta/Research/agent_memory.json", "r") as f:
    data = json.load(f)

recent = [d for d in data if d.get("timestamp", "") >= "2026-05-22T17:49"]

out_lines = ["# 🌌 ZBuddy Plasma Lake Candidates\n\n"]
out_lines.append("Here are the formally verified theorems ZBuddy synthesized using the new math-driven RAG pipeline. These are candidates for adoption into the InfoPhys/Plasma repository.\n\n")

for d in recent:
    epoch = d.get("epoch")
    tensor = d.get("tensor")
    thought = d.get("thought")
    lean = d.get("lean_code")
    out_lines.append(f"## Epoch {epoch} (Tensor: {tensor})\n")
    out_lines.append(f"**Thought:**\n{thought}\n\n")
    out_lines.append(f"**Lean 4 Theorem:**\n```lean\n{lean}\n```\n")
    out_lines.append("---\n\n")

with open("/home/phrxmaz/.gemini/antigravity/brain/70b55930-91c8-4419-bcb6-f80f19c162c7/zbuddy_plasma_candidates.md", "w") as f:
    f.writelines(out_lines)
print(f"Done. Extracted {len(recent)} items.")
