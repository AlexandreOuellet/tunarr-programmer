# tunarr-programmer

A standalone scheduling application for [Tunarr](https://github.com/chrisbenincasa/tunarr).

Tunarr stays what it is good at: it holds the media library, streams the channels, and stores
each channel's lineup. **This project owns everything about deciding what plays and when**:
the schedule definition, the planning (grid, ads, bumpers), the preview with metrics, the commit,
and the memory of "which episode plays next".

> **Status: skeleton.** The documentation describes the goal and the rules learned so far.
> Nothing runs yet. See [`docs/roadmap.md`](docs/roadmap.md).

## Why

Scheduling inside Tunarr turned out to be the hard part of running a themed channel lineup:

- Changing a rule means building an image, opening a PR and redeploying.
- Saving a schedule replaces the whole lineup (60 to 75 MB for a year) and moves anyone watching.
- There is no preview, no diff, no rollback, and no way to measure what a schedule will really do.
- Small timing errors add up (a few milliseconds a block became minutes over a year).
- Ordered shows cannot skip an episode that does not fit, and iterators restart on every regeneration.

Tunarr's API already accepts a hand-built ("manual") lineup, including ad clips, bumpers and flex.
That means the scheduling brain can live outside Tunarr and write to it. See
[`docs/tunarr-api.md`](docs/tunarr-api.md) for what was verified.

## How it fits

```
          schedules/*.yaml (git)                       Jellyfin / players
                  |                                           ^
                  v                                           |
  +-----------------------------+   read library     +------------------+
  |      tunarr-programmer      | <------------------ |      Tunarr      |
  |  engine . preview . worker  |   write lineup      |  library . lineup |
  |  state . web interface      | ------------------> |  streaming . EPG  |
  +-----------------------------+   (append / replace)+------------------+
```

## Documentation

| Document | What it covers |
|---|---|
| [`docs/vision.md`](docs/vision.md) | The goal, principles, non-goals, and how we will know it works |
| [`docs/architecture.md`](docs/architecture.md) | Components, data flow, state, deployment |
| [`docs/tunarr-api.md`](docs/tunarr-api.md) | What was verified against stock Tunarr, and what is still unknown |
| [`docs/planning-rules.md`](docs/planning-rules.md) | The scheduling rules the engine must implement |
| [`docs/metrics.md`](docs/metrics.md) | The measurements used to judge a schedule |
| [`docs/roadmap.md`](docs/roadmap.md) | Phases and open decisions |

## Layout

```
packages/engine         pure planning code: no network, no database
packages/tunarr-client  typed client for the parts of Tunarr's API we use
apps/cli                preview and apply from the command line
apps/web                the interface (later)
schedules/              one file per channel, versioned in git
tools/spike             the script that verified the Tunarr API
docs/                   the documents above
```
