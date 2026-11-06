# Tunarr API: what was verified

Everything here was tested on **stock Tunarr** (upstream `main` at commit `86cf43e3`, no
modifications), running on a copy of a real database, using only the HTTP API. The script is in
[`tools/spike/run.py`](../tools/spike/run.py).

## The write path

`POST /api/channels/{id}/programming` accepts a **manual** lineup:

```json
{ "type": "manual", "lineup": [ ...items... ], "append": false }
```

Item types: `content` (with `startOffsetMs`, which is how a program is split at its ad breaks),
`filler` (`fillerListId`, `fillerType`), `flex` (optionally with a `fillerConfig`), `custom`,
`redirect`. These are the same shapes the stock scheduler writes.

## Verified

| Check | Result |
|---|---|
| Save a day: 874 items (content, ad clips for mid/post/tail, flex) | Stored lineup is identical to what was sent |
| Expand with `append: true` | Stored lineup is identical to day 1 + day 2; duration is the exact sum |
| Rewrite the future (`append: false`, same past, new future) | Stored identical; `now_playing` unchanged |
| Filler types `head`, `pre`, `mid`, `post`, `tail`, `fallback` | All accepted and stored as sent |
| Flex with and without a `fillerConfig` | Both accepted and stored as sent |
| Program ids the channel does not already contain | Accepted. They only have to exist in the library |
| Channel `startTime` through manual saves | Never changes |
| `GET /api/channels/{id}/now_playing` | Reports the right program after each step |
| Channel duration | Always equals the sum of the lineup (to the millisecond) |

Ad clips and bumpers are ordinary `filler` items pointing at a clip (a program id) in a filler
list, with that clip's duration. Choosing the clips is the engine's job ("eager" scheduling).

## Do not do

- **Do not change a channel's `startTime`** (`PUT /api/channels/{id}`). It is stored to the whole
  minute, and changing it on a channel with a lineup changed the stored lineup in ways that were
  not understood (the duration shrank and a long flex appeared at the start). The lineup can
  only grow; plan for a year or so of lineup (about 60 to 75 MB) as Tunarr does today.
- Do not let the channel be saved from Tunarr's own interface while managed here.

## Not verified yet

- Real playback through ffmpeg and the media server for a manually written lineup.
- The XMLTV guide and the media server's guide after an append (caching was a problem before).
- How a very long lineup (several years) behaves.
- Behaviour of `append: true` exactly at the moment a viewer crosses the join.

## Useful endpoints

`GET /openapi.json` (the schema), `GET /api/channels`, `GET /api/channels/{id}`,
`GET /api/channels/{id}/programming` (the stored lineup), `GET /api/channels/{id}/now_playing`,
`GET /api/channels/{id}/lineup?from=&to=` (the guide, which hides ad filler),
`GET /api/smart_collections`, `POST /api/programs/search`.
