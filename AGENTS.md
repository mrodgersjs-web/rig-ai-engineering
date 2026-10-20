
## RIG lattice contract (stamped)

This repository runs the shared RIG lattice: loops in `.rig/loop.yaml`, pre-tool
hooks in `.rig/hooks/`, CI gate in `.github/workflows/rig-lattice.yml`, execution
owner routing in `.rig/work-routing.yaml` (operator standard 2026-09-11), and a
results-driven MCP server at `mcp/server.py` returning verified results only.
Determinism rules apply to builds: every outward action needs a Gate-D request and typed approval;
durable builds need four ratios >= 0.85 and a sealed proof. Done-claims need the coding-agent playbook
close-gate sealed evidence. Shared agent substrate lives in Supabase schema
`rig_shared` (see PROGRAM.md in rig-lattice-retrofit).
