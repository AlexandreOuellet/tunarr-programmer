import json, sys, time, urllib.request, urllib.error, collections

B = sys.argv[1]
CH = sys.argv[2]
D = json.load(open('spike/lineups.json'))
day1, day2 = D['day1'], D['day2']
day3 = D.get('day3')


def req(m, p, b=None):
    r = urllib.request.Request(B + p, method=m, data=json.dumps(b).encode() if b is not None else None,
                               headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=600) as f:
            t = f.read()
            return f.status, json.loads(t or b"null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def key(x):
    return (x['type'], x.get('id'), round(x['duration']), x.get('fillerType'), x.get('startOffsetMs'), x.get('fillerListId'))


def same(stored, sent):
    return len(stored) == len(sent) and all(key(a) == key(b) for a, b in zip(stored, sent))


def ch():
    return req("GET", f"/api/channels/{CH}")[1]


def lineup():
    return req("GET", f"/api/channels/{CH}/programming")[1]['lineup']


def now_playing():
    st, n = req("GET", f"/api/channels/{CH}/now_playing")
    return (n.get('id'), n.get('type')) if st == 200 and isinstance(n, dict) else (st, str(n)[:60])


def hours(ms):
    return f"{ms / 3600000:.3f} h"


st, v = req("GET", "/api/version")
print("server:", v)
c0 = ch()
print(f"channel '{c0['name']}': startTime {c0['startTime']}, duration {hours(c0['duration'])}")

# 1. save the first day (replace)
st, _ = req("POST", f"/api/channels/{CH}/programming", {"type": "manual", "lineup": day1, "append": False})
c1 = ch()
print(f"\n1. SAVE day 1 (manual, append false): HTTP {st} | {len(day1)} items | stored identical: {same(lineup(), day1)} | duration {hours(c1['duration'])} (sent {hours(sum(x['duration'] for x in day1))}) | startTime kept: {c1['startTime'] == c0['startTime']}")
kinds = collections.Counter((x['type'], x.get('fillerType')) for x in day1)
print("   item kinds saved:", dict(kinds))

# 2. expand (append)
st, _ = req("POST", f"/api/channels/{CH}/programming", {"type": "manual", "lineup": day2, "append": True})
c2 = ch()
print(f"\n2. EXPAND (append true): HTTP {st} | stored identical to day1+day2: {same(lineup(), day1 + day2)} | duration {hours(c2['duration'])} (expected 48.000 h) | startTime kept: {c2['startTime'] == c0['startTime']}")
print("   now playing:", now_playing())

# 3. rewrite the future only, keeping the past and the present untouched
start = c2['startTime']
L = lineup()
off = (int(time.time() * 1000) - start) % c2['duration']
acc = 0
cut = None
for i, x in enumerate(L):
    acc += x['duration']
    if acc > off + 2 * 3600000:
        cut = i + 1
        break
before = now_playing()
newfuture = day3 or list(reversed(day2))
new = L[:cut] + newfuture
st, _ = req("POST", f"/api/channels/{CH}/programming", {"type": "manual", "lineup": new, "append": False})
c3 = ch()
print(f"\n3. REWRITE THE FUTURE (keep the first {cut} items = past + now + 2 h, replace the rest): HTTP {st} | stored identical: {same(lineup(), new)} | startTime kept: {c3['startTime'] == start} | duration {hours(c3['duration'])}")
print(f"   now playing before {before} / after {now_playing()} -> unchanged: {before == now_playing()}")

# 4. trim the past (drop old items, move startTime forward by their length), with every step printed
L = lineup()
c = ch()
off = (int(time.time() * 1000) - c['startTime']) % c['duration']
acc = 0
k = 0
for i, x in enumerate(L):
    if acc + x['duration'] > off - 3600000:
        break
    acc += x['duration']
    k = i + 1
print(f"\n4. TRIM THE PAST: drop the first {k} items ({hours(acc)}), then move startTime forward by that")
print(f"   before: startTime {c['startTime']} duration {hours(c['duration'])} now playing {now_playing()}")
trimmed = L[k:]
st, _ = req("POST", f"/api/channels/{CH}/programming", {"type": "manual", "lineup": trimmed, "append": False})
ca = ch()
print(f"   after saving the shorter lineup: HTTP {st} | startTime {ca['startTime']} | duration {hours(ca['duration'])} (lineup is {hours(sum(x['duration'] for x in trimmed))}) | now playing {now_playing()}")
body = dict(ca)
body['startTime'] = c['startTime'] + acc
st, r = req("PUT", f"/api/channels/{CH}", body)
cb = ch()
print(f"   after PUT startTime +{hours(acc)}: HTTP {st} {'' if st == 200 else r} | startTime {cb['startTime']} (moved {hours(cb['startTime'] - c['startTime'])}) | duration {hours(cb['duration'])} | now playing {now_playing()}")
print("   playback unchanged by the trim:", now_playing() == before or now_playing())

# 5. every filler type (bumpers included) and both kinds of flex
L = lineup()
clip = [x for x in L if x['type'] == 'filler'][0]
syn = [{**clip, "fillerType": ft} for ft in ("head", "pre", "mid", "post", "tail", "fallback")]
syn += [{"type": "flex", "duration": 15000, "fillerConfig": {"fillerListIds": [clip['fillerListId']], "origin": "midroll"}}, {"type": "flex", "duration": 5000}]
st, r = req("POST", f"/api/channels/{CH}/programming", {"type": "manual", "lineup": syn, "append": True})
tail = lineup()[-8:]
print(f"\n5. APPEND filler types head/pre/mid/post/tail/fallback + two kinds of flex: HTTP {st} {'' if st == 200 else r}")
print("   stored:", [(x['type'], x.get('fillerType') or ('config' if x.get('fillerConfig') else '')) for x in tail])
