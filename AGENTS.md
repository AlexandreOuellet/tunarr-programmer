# tunarr-programmer: notes for contributors and coding agents

- Read `docs/vision.md` and `docs/planning-rules.md` first. The rules come from measurements.
- `packages/engine` stays pure: no network, no database, no `Date.now()`. Inject the clock.
- Never write to a Tunarr that people are watching while testing. Use a copy of its data.
- Never change a channel's `startTime`. See `docs/tunarr-api.md`.
- Every duration written to a lineup is an integer number of milliseconds.
- Do not commit secrets, library dumps or lineup files.
