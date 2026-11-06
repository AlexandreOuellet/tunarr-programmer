# Roadmap

## Phase 0: skeleton (now)
Repository, documentation, the verified API facts, and the script that verified them.

## Phase 1: the engine
- Move the planning code (ad planner, water-filling, packing, fit-aware picking, grid and clock
  handling) into `packages/engine`, with its tests.
- A pure `plan(schedule, library, state, window)` that returns lineup items and new state.
- Golden tests: the same schedule and seed always give the same lineup.

## Phase 2: Tunarr client and CLI
- Read the library; write manual lineups (replace and append).
- `preview` prints the metrics in [`metrics.md`](metrics.md) for any window.
- Run end to end on a test copy of Tunarr for one channel.

## Phase 3: state and worker
- Per channel: next episode of ordered shows, seeds, end of the lineup written, commit log.
- A top-up job that plans from the end of the lineup and appends.
- Open the remaining unknowns from [`tunarr-api.md`](tunarr-api.md): playback and guide checks.

## Phase 4: schedules in git
- One YAML file per channel (see [`schedules/example.yaml`](../schedules/example.yaml)).
- Pull request previews with the metrics; merge applies.

## Phase 5: web interface
- Edit schedules, preview, see what is scheduled, link to the channel in Tunarr.

## Open decisions
- Name and licence of the project.
- Language (TypeScript is assumed, to reuse the planner).
- How far ahead to write by default (a day or two keeps changes quick to apply).
- How to rebase a lineup that grows without moving the start time.
- Whether ordered shows should skip and defer.
