#!/usr/bin/env python3
"""Roblox market intel: live search, chart snapshots and game stats from Roblox's public web APIs.

Usage:
  python3 tools/roblox_intel.py search "hatch a kaiju" [--n 10] [--json]
  python3 tools/roblox_intel.py charts [--save]          # Top Trending, Up-and-Coming, etc.
  python3 tools/roblox_intel.py game <universeId> [...]
  python3 tools/roblox_intel.py sweep "steal a" "grow a" "+1" ... [--max-age 180] [--save name]
      Searches every phrase, dedupes, keeps games created within --max-age days, and prints
      hit-rate stats: share of games at >=1K and >=10K live CCU (1K = "it worked", 10K = hit).

Metrics printed per game:
  playing   live concurrent players right now
  visits    lifetime visits
  age_d     days since the experience was created
  upd_d     days since the last update
  v/day     visits per day of life (rough momentum proxy)
  like%     upvotes / (up + down)
"""
import json, sys, time, urllib.parse, urllib.request, datetime as dt, os

UA = {"User-Agent": "Mozilla/5.0 (market-research script)"}
NOW = dt.datetime.now(dt.timezone.utc)


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception as e:  # rate limits are common; back off
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def details(ids):
    out = {}
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 50):
        chunk = ",".join(str(x) for x in ids[i:i + 50])
        for g in get(f"https://games.roblox.com/v1/games?universeIds={chunk}").get("data", []):
            out[g["id"]] = g
    votes = {}
    for i in range(0, len(ids), 50):
        chunk = ",".join(str(x) for x in ids[i:i + 50])
        try:
            for v in get(f"https://games.roblox.com/v1/games/votes?universeIds={chunk}").get("data", []):
                votes[v["id"]] = v
        except Exception:
            pass
    return out, votes


def days(ts):
    if not ts:
        return None
    return (NOW - dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))).days


def row(g, v):
    age = days(g.get("created"))
    up, down = (v or {}).get("upVotes", 0), (v or {}).get("downVotes", 0)
    return {
        "universeId": g["id"],
        "name": g["name"],
        "creator": g.get("creator", {}).get("name"),
        "playing": g.get("playing", 0),
        "visits": g.get("visits", 0),
        "favorites": g.get("favoritedCount", 0),
        "created": (g.get("created") or "")[:10],
        "age_d": age,
        "upd_d": days(g.get("updated")),
        "v_per_day": round(g.get("visits", 0) / max(age or 1, 1)),
        "like_pct": round(100 * up / (up + down)) if up + down else None,
        "url": f"https://www.roblox.com/games/{g.get('rootPlaceId')}",
    }


def table(rows):
    print(f"{'playing':>9} {'visits':>13} {'age_d':>6} {'upd_d':>5} {'v/day':>10} {'like%':>5}  name  [created]")
    for r in rows:
        print(f"{r['playing']:>9,} {r['visits']:>13,} {str(r['age_d']):>6} {str(r['upd_d']):>5} {r['v_per_day']:>10,} {str(r['like_pct']):>5}  {r['name'][:60]}  [{r['created']}] id={r['universeId']}")


def search(q, n=10):
    url = "https://apis.roblox.com/search-api/omni-search?" + urllib.parse.urlencode(
        {"searchQuery": q, "sessionId": "intel", "pageType": "all"})
    ids = []
    for grp in get(url).get("searchResults", []):
        for c in grp.get("contents", []):
            if c.get("contentType") == "Game":
                ids.append(c["universeId"])
    ids = ids[:n]
    d, v = details(ids)
    return [row(d[i], v.get(i)) for i in ids if i in d]


def charts():
    data = get("https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=intel&device=computer&country=all")
    sorts = {}
    for s in data.get("sorts", []):
        games = s.get("games") or []
        if games:
            sorts[s.get("sortDisplayName") or s["sortId"]] = [g["universeId"] for g in games]
    allids = [i for ids in sorts.values() for i in ids]
    d, v = details(allids)
    return {name: [row(d[i], v.get(i)) for i in ids if i in d] for name, ids in sorts.items()}


def sweep(phrases, max_age=180, n=40):
    seen = {}
    for q in phrases:
        try:
            for r in search(q, n):
                r.setdefault("queries", [])
                seen.setdefault(r["universeId"], r)["queries"] = sorted(set(seen.get(r["universeId"], r).get("queries", []) + [q]))
        except Exception as e:
            print("search failed:", q, e, file=sys.stderr)
        time.sleep(0.5)
    rows = [r for r in seen.values() if r["age_d"] is not None and r["age_d"] <= max_age]
    rows.sort(key=lambda r: -r["playing"])
    return rows


def stats(rows, label="all"):
    n = len(rows)
    k1 = sum(r["playing"] >= 1000 for r in rows)
    k10 = sum(r["playing"] >= 10000 for r in rows)
    print(f"{label}: {n} games | >=1K CCU: {k1} ({100*k1/max(n,1):.0f}%) | >=10K: {k10} ({100*k10/max(n,1):.0f}%)")


if __name__ == "__main__":
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if not a:
        print(__doc__); sys.exit(1)
    cmd = a[0]
    if cmd == "search":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 10
        rows = search(a[1], n)
        print(json.dumps(rows, indent=1)) if as_json else table(rows)
    elif cmd == "charts":
        c = charts()
        if "--save" in a:
            base = os.path.join(os.path.dirname(__file__), "..", "08 - Market Research", "Data")
            os.makedirs(base, exist_ok=True)
            p = os.path.join(base, f"charts-{NOW:%Y-%m-%d-%H%M}.json")
            json.dump(c, open(p, "w"), indent=1)
            print("saved", os.path.normpath(p))
        if as_json:
            print(json.dumps(c, indent=1))
        else:
            for name, rows in c.items():
                print(f"\n=== {name} ({len(rows)}) ===")
                table(rows[:25])
    elif cmd == "sweep":
        max_age = int(a[a.index("--max-age") + 1]) if "--max-age" in a else 180
        save = a[a.index("--save") + 1] if "--save" in a else None
        flags = {"--max-age", "--save"}
        phrases = [x for i, x in enumerate(a[1:], 1) if x not in flags and a[i - 1] not in flags]
        rows = sweep(phrases, max_age)
        stats(rows, f"created <= {max_age}d")
        for q in phrases:
            stats([r for r in rows if q in r["queries"]], f"  '{q}'")
        if save:
            base = os.path.join(os.path.dirname(__file__), "..", "08 - Market Research", "Data")
            os.makedirs(base, exist_ok=True)
            p = os.path.join(base, f"sweep-{save}-{NOW:%Y-%m-%d}.json")
            json.dump(rows, open(p, "w"), indent=1)
            print("saved", os.path.normpath(p))
        if as_json:
            print(json.dumps(rows, indent=1))
        else:
            table(rows[:40])
    elif cmd == "game":
        d, v = details([int(x) for x in a[1:]])
        rows = [row(g, v.get(i)) for i, g in d.items()]
        print(json.dumps(rows, indent=1)) if as_json else table(rows)
