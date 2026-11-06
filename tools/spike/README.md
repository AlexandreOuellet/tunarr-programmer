# API spike

`run.py` is the script that verified the Tunarr API on stock Tunarr. See
[`../../docs/tunarr-api.md`](../../docs/tunarr-api.md) for the results.

It needs a Tunarr you can write to (use a **copy**, never the one people are watching), a channel
id, and `spike/lineups.json` with three lists of lineup items (`day1`, `day2`, `day3`, each about
24 hours: content, filler and flex items taken from a real eager schedule).

    python3 run.py http://127.0.0.1:8000 <channel-id>

Steps it runs, printing every value: save a day, expand with `append`, rewrite the future while the
past and present stay identical, trim attempt, and every filler type. **Warning:** the trim step
changes the channel's `startTime` through `PUT /api/channels/{id}`, which this project must not do
in real use (see the docs). It is kept only to reproduce the finding.
