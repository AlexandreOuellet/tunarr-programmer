# Architecture

## Components

**Engine** (`packages/engine`) is pure code: durations in, lineup out. No network, no database,
no clock except the one it is given. It contains the slot packing, the ad planner, the pool
picking (shuffled, ordered, fit-aware), the grid and clock handling, and the rounding rules
([`planning-rules.md`](planning-rules.md)). Because it is pure, it is tested with plain unit tests
and can run anywhere: the CLI, a CI job, the web interface, a worker.

**Tunarr client** (`packages/tunarr-client`) reads the library and writes lineups. It wraps only
the endpoints in [`tunarr-api.md`](tunarr-api.md).

**State** is a small store (SQLite on a volume is enough) holding, per channel: the next episode
of each ordered show, shuffle seeds, the end of the lineup already written, and a log of every
commit. It is what makes "continue where we left off" survive.

**Worker** tops each channel up on a schedule (for example daily, a day or two ahead). It plans
from the end of the lineup already written, and appends. It never touches the past or the present.

**CLI** (`apps/cli`) does the same planning on demand: `preview` prints the metrics for a
schedule, `apply` commits it.

**Web interface** (`apps/web`) edits schedules, shows the preview and its metrics, shows what is
scheduled, and links to the matching channel in Tunarr. Later phase.

## Data flow

1. A schedule file (`schedules/<channel>.yaml`) defines slots, pools and ad settings.
2. The client reads the library from Tunarr (programs, shows, filler lists).
3. The engine plans a window of time starting at the end of the lineup already written.
4. The preview computes the metrics for that window. In a pull request they are posted as a comment.
5. On apply, the client writes the planned items to Tunarr (append, or a replace that keeps the
   past and the present identical) and the state records what was written.
6. A guide refresh is requested for the media server that reads Tunarr's guide.

## Schedules in git

A schedule is reviewed like code. The pull request carries the preview, so a reviewer sees, for
example, that a new layout lowers the median wait after a show but leaves 4% of windows with
more than 30 minutes unused, before merging.

## Deployment

Runs in the same cluster as Tunarr, as a Deployment (interface and API) and a CronJob (top-ups),
configured through the existing GitOps repository. State lives on a small volume. It needs read
access to Tunarr's API, and the Tunarr address and any credentials come from sealed secrets.

## Risks and rules

- Someone saving a channel in Tunarr's own interface will overwrite what this project wrote.
  Channels managed here should be marked as such, and edited only here.
- Tunarr is the source of truth for the library. If media moves, the plan is recomputed.
- Never move a channel's start time. See [`tunarr-api.md`](tunarr-api.md).
