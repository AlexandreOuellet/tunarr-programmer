# Vision

## Goal

Run themed TV channels from a personal media library, where **a person describes the channel
and the system works out the lineup**: which program in which slot, how much advertising and
where, when the next program starts, and which episode comes next. Tunarr plays the result.

## Principles

1. **Tunarr streams, this project schedules.** No duplicated library, no second streamer.
2. **The schedule is data.** One file per channel in git. A change is a pull request, and the pull
   request shows what the change does to the channel before it goes live.
3. **Never disturb a viewer.** What is playing, and what is about to play, is never rewritten.
   Changes land in the future only.
4. **Measure, do not guess.** Every schedule is judged by the same numbers
   ([`metrics.md`](metrics.md)): grid accuracy, ad share, waits at the end of a slot, dead air.
5. **The grid is a hard rule.** Programs start on the grid (for example every 15 minutes),
   exactly, for the whole lineup. Ad lengths flex to make that true.
6. **Deterministic.** The same schedule, library and seed give the same lineup.

## Non-goals

- Not a media server, not a streamer, not a transcoder.
- Not a replacement for Tunarr's channel, source and filler configuration.
- Not a general EPG product. It targets Tunarr channels only.
- No multi-user accounts or permissions in the first versions.

## Success looks like

- A new channel layout is previewed, reviewed and applied without building an image.
- Over a 365-day lineup, **100% of programs start within one second of the grid**.
- Dead air is a few seconds per program, and a long run of ads after a show is rare and
  visible in the preview before it ever airs.
- Applying a change never moves what is currently playing.
- "What plays next" survives a rebuild: ordered shows continue where they left off.
