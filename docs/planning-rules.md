# Planning rules

The rules the engine must implement. They come from running real schedules and measuring them.

## The grid

- Every program starts on the grid (for example every 15 minutes), exactly.
- Every duration written to the lineup is a whole number of milliseconds, and the rounding error
  is carried into the next item. Without this, a few milliseconds a block added up to minutes
  over a year, and 93% of programs ended up more than 10 seconds off the grid.
- A block ends exactly where a window ends. No tolerance, no overflow, no lateness: a late window
  was shown to push the delay into the next window, again and again.

## Blocks

- A block is one program plus everything around it: head, pre, mid breaks, post, tail, bumpers.
- Its length is the first grid point at or after `content + bumpers + max(minimum ads, required
  ads)`. Required ads are the minimums of every position that applies (post and mid for a
  program, head for the first of a window, tail for the last).
- **The ad ratio is a cap on ads inside the block, not a promise to fill it.** On a 15-minute
  grid a 22-minute show gets a 30-minute block; the 8 minutes of room are 36% of the show.
  Either ads fill it, or something else must.

## Ad positions

- Mid-break positions are *offers*: a break every N minutes of **content time** (ads and bumpers
  do not count), with a tail buffer so none lands right before the end. The planner uses as many
  as the budget allows, spread evenly.
- Each position has a range (for example mid 2 to 3 minutes, post 0 to 5, tail 0 to 25). A
  minimum of 0 means the position may stay empty. Planned lengths are multiples of a step
  (15 seconds), because ad clips are about 15 to 30 seconds.
- **Distribution: a rising water level.** Reserve every minimum, then raise all positions together
  one step at a time, always the shortest first. Order on ties: tail, post, pre, head, then the
  mid breaks together as one group. A position that reached its maximum drops out. When only the
  mid breaks can still rise and a full round does not fit, single mid breaks take the leftover
  steps (so some are one step longer). Compared with "post and tail first", this moved mid-roll
  from 59% to 69% of the ad time and cut blocks with most ads after the show from 50% to 8%.
- The last block of a window may run to the window's end only if its ads stay within the ratio
  ceiling and each position's maximum. Otherwise the rest is fallback or dead air.
- The last 10 to 15 seconds of a break often cannot be filled: the clip list has almost no short
  clips. A fallback clip (one clip with the leftover time) or more short clips closes it.

## Picking programs

- Shuffled pools are **fit-aware**: if the next pick does not fit the time left in the window,
  take a later one that does.
- Ordered shows cannot skip. When the next episode does not fit, the window ends with unused
  time. Option: skip and defer (play what fits, the skipped one next time).
- Reruns are acceptable. Pools should be large enough that repeats are not noticeable.

## Windows

- **One program per slot, with the slot length chosen from the program lengths.** Windows that
  hold exactly one program (or an exact multiple) leave nothing unused; mixed lengths leave a
  different leftover every time. For example, with a 15-minute grid and 15% minimum ads, a movie
  of up to 117 minutes needs a 2h15 block, up to 143 minutes 2h45, and so on.
- Hour-long episodes (about 43 to 57 minutes) take a 60-minute block, so four fit a 4-hour
  window exactly.
- Very different lengths belong in different slots. Specials of 30 to 70 minutes do not belong
  in movie slots.
- A theme is chosen *after* grouping by length, and the evening slots are the best groups.

## Dead air and time

- Dead air at the end of a block counts as advertising when judging a schedule.
- Daylight saving and the schedule's clock are owned by this project, tested explicitly,
  and the day of a change is excluded from the metrics.
