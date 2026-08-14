# Non-duplicate phase contract

Phase ZIPs are additive, not cumulative.

- Phase 1 owns all files listed in `PHASE_1_MANIFEST.json`.
- Phase 2 must contain only new file paths.
- Phase 3 must contain only new file paths.
- Phase 4 must contain only new file paths.
- To assemble the complete PowerX project, extract Phase 1, then Phase 2, then Phase 3, then Phase 4 into the same project root.

Future phases are designed to extend Phase 1 through new modules, registries, adapters,
and runtime plugins instead of re-packaging Phase 1 files.
