"""Regenerate the animated "space shooter" contribution graphs.

Writes assets/contributions.svg (desktop, 53 weeks) and assets/contributions-mobile.svg
(phones, last 26 weeks, larger type). Reads the public contribution calendar of GITHUB_USER
through the GitHub GraphQL API (token from GH_TOKEN). Standard library only.
"""
import datetime
import json
import os
import random
import urllib.request

USER = os.environ.get("GITHUB_USER", "eduardomartim")
TOKEN = os.environ["GH_TOKEN"]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{firstDay contributionDays{date contributionCount contributionLevel weekday}}}}}}"""

M = "font-family=\"ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace\""
RED = "#ff3b3b"
LV = {"FIRST_QUARTILE": "#7a1d23", "SECOND_QUARTILE": "#b02630", "THIRD_QUARTILE": "#e0323c", "FOURTH_QUARTILE": "#ff4d4d"}

PROFILES = {
    "desktop": dict(out="contributions.svg", W=860, H=262, CS=11, STEP=15, Y0=84, nweeks=53, stars=36, twinkle=4,
                    ship_v=360.0, ship_y_off=34, month_y=76, line_y=52, label="in the last year"),
    "mobile": dict(out="contributions-mobile.svg", W=390, H=236, CS=11, STEP=13, Y0=90, nweeks=26, stars=18, twinkle=2,
                   ship_v=300.0, ship_y_off=28, month_y=82, line_y=62, label="in the last 6 months"),
}


def fetch_calendar():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "contributions-graph"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise SystemExit(f"GraphQL error: {payload.get('errors')}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def build(weeks_all, p):
    weeks = weeks_all[-p["nweeks"]:]
    W, H, CS, STEP, Y0 = p["W"], p["H"], p["CS"], p["STEP"], p["Y0"]
    n = len(weeks)
    X0 = (W - n * STEP + (STEP - CS)) / 2
    ship_y = H - p["ship_y_off"]
    total = sum(d["contributionCount"] for w in weeks for d in w["contributionDays"])
    cells = []
    for c, w in enumerate(weeks):
        for d in w["contributionDays"]:
            if d["contributionCount"] > 0:
                cells.append(dict(x=X0 + c * STEP, y=Y0 + d["weekday"] * STEP, c=c, r=d["weekday"],
                                  n=d["contributionCount"], lv=d["contributionLevel"], date=d["date"]))
    months, last = [], None
    for c, w in enumerate(weeks):
        m = datetime.date.fromisoformat(w["firstDay"]).strftime("%b")
        if m != last and c < n - 1:
            months.append((X0 + c * STEP, m))
            last = m

    # --- timeline ---
    BUL_V, FIRE_GAP, SETTLE = 480.0, 0.45, 0.3
    order = sorted(cells, key=lambda k: (k["c"], -k["r"]))
    shipx, t = W / 2, 1.0
    ship_kf = [(0.0, shipx), (t, shipx)]
    bullets, prev = [], None
    for k in order:
        k["tx"] = k["x"] + CS / 2
        if prev is None or abs(prev["tx"] - k["tx"]) > 1:
            t += abs(k["tx"] - shipx) / p["ship_v"] + SETTLE
            shipx = k["tx"]
            ship_kf.append((t, shipx))
        tf = t
        th = tf + (ship_y - 14 - (k["y"] + CS)) / BUL_V
        bullets.append((tf, th, k))
        t = tf + FIRE_GAP
        ship_kf.append((t, shipx))
        prev = k
    END = t + 2.0
    T = END + 0.8
    ship_kf += [(END, shipx), (END + 0.5, W / 2), (T, W / 2)]

    def kt(v):
        return f"{v / T:.4f}"

    def anim(attr, vals, kts):
        return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{";".join(kts)}" dur="{T:.2f}s" repeatCount="indefinite"/>'

    ship = (f'<g transform="translate({W / 2},{ship_y})"><animateTransform attributeName="transform" type="translate" '
            f'values="{";".join(f"{b:.1f} {ship_y}" for _, b in ship_kf)}" keyTimes="{";".join(kt(a) for a, _ in ship_kf)}" '
            f'dur="{T:.2f}s" repeatCount="indefinite"/>'
            '<path d="M0 -13 L5 -2 L13 6 L13 9 L4 6 L2 12 L-2 12 L-4 6 L-13 9 L-13 6 L-5 -2 Z" fill="#4d8dff" stroke="#9cc2ff" stroke-width="0.8"/>'
            '<rect x="-1.2" y="12" width="2.4" height="5" rx="1" fill="#ffffff" opacity="0.8"/></g>')
    cellsvg = bulsvg = expsvg = ""
    for tf, th, k in bullets:
        cx, cy = k["tx"], k["y"] + CS / 2
        fade = [kt(0), kt(th), kt(th + 0.001), kt(T - 0.7), "1"]
        cellsvg += (f'<rect x="{k["x"]:.1f}" y="{k["y"]}" width="{CS}" height="{CS}" rx="2.5" fill="{LV[k["lv"]]}">'
                    f'{anim("opacity", "1;1;0;0;1", fade)}<title>{k["date"]}: {k["n"]} contributions</title></rect>\n')
        ys, ye = ship_y - 18, k["y"] + CS
        bulsvg += (f'<rect x="{cx - 1.2:.1f}" y="{ys}" width="2.4" height="9" rx="1.2" fill="#ffffff" opacity="0">'
                   f'{anim("opacity", "0;0;1;0;0", [kt(0), kt(tf), kt(tf + 0.001), kt(th), "1"])}'
                   f'{anim("y", f"{ys};{ys};{ye};{ye}", [kt(0), kt(tf), kt(th), "1"])}</rect>\n')
        expsvg += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2" fill="none" stroke="#ffd9d9" stroke-width="1.6" opacity="0">'
                   f'{anim("opacity", "0;0;1;0;0", [kt(0), kt(th), kt(th + 0.001), kt(th + 0.45), "1"])}'
                   f'{anim("r", "2;2;2;14;14", [kt(0), kt(th), kt(th + 0.001), kt(th + 0.45), "1"])}</circle>\n')

    random.seed(7)
    stars = "".join(f'<circle cx="{random.uniform(8, W - 8):.0f}" cy="{random.uniform(p["line_y"] + 8, H - 8):.0f}" '
                    f'r="{random.choice([0.6, 0.8, 1.0, 1.2])}" fill="#fff" opacity="{random.choice([0.18, 0.3, 0.45])}"/>'
                    for _ in range(p["stars"]))
    twinkle = "".join(f'<circle cx="{random.uniform(20, W - 20):.0f}" cy="{random.uniform(p["line_y"] + 18, H - 20):.0f}" r="1.3" fill="#fff">'
                      f'<animate attributeName="opacity" values="0.1;0.8;0.1" dur="{random.uniform(2.5, 5):.1f}s" '
                      f'begin="{random.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(p["twinkle"]))

    # one patterned rectangle per column block instead of one <rect> per empty day
    first_wd = weeks[0]["contributionDays"][0]["weekday"]
    last_days = len(weeks[-1]["contributionDays"])
    blocks = []
    if n >= 2:
        blocks.append((X0, Y0 + first_wd * STEP, STEP, (7 - first_wd) * STEP))
    if n >= 3:
        blocks.append((X0 + STEP, Y0, (n - 2) * STEP, 7 * STEP))
    blocks.append((X0 + (n - 1) * STEP, Y0, STEP, last_days * STEP))
    grid = "".join(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" fill="url(#cell)"/>' for x, y, w, h in blocks)

    mon = "".join(f'<text x="{x:.1f}" y="{p["month_y"]}" {M} font-size="9" fill="#6b727c">{m}</text>' for x, m in months)
    if p["out"] == "contributions.svg":
        head = (f'<text x="30" y="40" {M} font-size="12" letter-spacing="2" fill="{RED}">CONTRIBUTIONS</text>'
                f'<text x="170" y="40" {M} font-size="11" fill="#8b949e" fill-opacity="0.8">{total} contributions {p["label"]}</text>'
                f'<text x="{W - 178}" y="39" text-anchor="end" {M} font-size="10" fill="#6b727c">less</text>'
                + "".join(f'<rect x="{W - 168 + i * 16}" y="31" width="10" height="10" rx="2.5" fill="{c}"'
                          + (' fill-opacity="0.08"' if i == 0 else "") + "/>" for i, c in enumerate(["#ffffff"] + list(LV.values())))
                + f'<text x="{W - 22}" y="39" text-anchor="end" {M} font-size="10" fill="#6b727c">more</text>')
    else:
        head = (f'<text x="20" y="32" {M} font-size="12" letter-spacing="2" fill="{RED}">CONTRIBUTIONS</text>'
                f'<text x="20" y="50" {M} font-size="11" fill="#8b949e" fill-opacity="0.9">{total} contributions {p["label"]}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Contribution activity: {total} contributions {p["label"]}</title>
  <desc id="d">Animated contribution graph. A spaceship moves along the bottom and shoots the days that have contributions, then the graph resets. {len(cells)} active days, {total} contributions {p["label"]}.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0d12"/><stop offset="1" stop-color="#14171d"/></linearGradient>
    <pattern id="cell" x="{X0:.1f}" y="{Y0}" width="{STEP}" height="{STEP}" patternUnits="userSpaceOnUse"><rect width="{CS}" height="{CS}" rx="2.5" fill="#ffffff" fill-opacity="0.045"/></pattern>
  </defs>
  <rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
  {stars}
  {twinkle}
  {head}
  <line x1="{20 if W < 500 else 28}" y1="{p["line_y"]}" x2="{W - (20 if W < 500 else 28)}" y2="{p["line_y"]}" stroke="{RED}" stroke-opacity="0.5" stroke-width="1.5"/>
  {mon}
  {grid}
{cellsvg}{bulsvg}{expsvg}  {ship}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="#ffffff" stroke-opacity="0.10"/>
</svg>
'''
    with open(os.path.join(ASSETS, p["out"]), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print(p["out"], len(svg), "bytes", f"T={T:.1f}s", len(cells), "cells", total, "contributions")


cal = fetch_calendar()
for profile in PROFILES.values():
    build(cal["weeks"], profile)
