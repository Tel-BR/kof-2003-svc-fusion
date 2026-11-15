---
title: "Probe fighter memory in the native player"
triage: ready-for-agent
---

# 08 Probe fighter memory in the native player

[Parent specification](../spec.md)

## What to build

Give the native KOF 2003 player a headless option that logs selected work-RAM addresses every frame, so the import can be measured in the native build the same way `tools/kof2003/match/probe.lua` measures MAME. Change only the local runtime copy under `private/`. The owner authorized the rebuild on 2026-11-15.

## Blocked by

None.

## Acceptance criteria

- [ ] A scripted native run writes one line per frame with the requested addresses, and the option is off by default.
- [ ] For the scripted Iori team match, the native log of P1's pose pointer (`$101080 + 0x60`) and both fighters' health matches the MAME probe for the same frames.
- [ ] The native MVS control run still passes `--verify` with the option off.
- [ ] Commands to build and run it are recorded under `tools/kof2003/`.
