"""Regenerate assets/contributions.svg (animated "space shooter" contribution graph).

Reads the public contribution calendar of GITHUB_USER through the GitHub GraphQL API
(token from GH_TOKEN) and writes the SVG. Standard library only.
"""
import datetime
import json
import os
import random
import urllib.request

USER = os.environ.get("GITHUB_USER", "eduardomartim")
TOKEN = os.environ["GH_TOKEN"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "contributions.svg")

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{firstDay contributionDays{date contributionCount contributionLevel weekday}}}}}}"""


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


cal = fetch_calendar()
weeks=cal["weeks"]; total=cal["totalContributions"]
M="font-family=\"ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace\""
RED="#ff3b3b"
LV={"FIRST_QUARTILE":"#7a1d23","SECOND_QUARTILE":"#b02630","THIRD_QUARTILE":"#e0323c","FOURTH_QUARTILE":"#ff4d4d"}
W,H=860,262; CS=11; STEP=15; X0=(W-53*STEP+ (STEP-CS))/2; Y0=84
SHIP_Y=H-34
cells=[]; empty=[]
for c,w in enumerate(weeks):
    for d in w["contributionDays"]:
        x=X0+c*STEP; y=Y0+d["weekday"]*STEP
        if d["contributionCount"]>0: cells.append(dict(x=x,y=y,c=c,r=d["weekday"],n=d["contributionCount"],lv=d["contributionLevel"],date=d["date"]))
        else: empty.append((x,y))
# months
months=[]; last=None
for c,w in enumerate(weeks):
    m=datetime.date.fromisoformat(w["firstDay"]).strftime("%b")
    if m!=last and c<52: months.append((X0+c*STEP,m)); last=m
# --- timeline ---
SHIP_V=360.0; BUL_V=480.0; FIRE_GAP=0.45; SETTLE=0.3
order=sorted(cells,key=lambda k:(k["c"],-k["r"]))
shipx=(W/2); t=1.0
ship_kf=[(0.0,shipx)]; ship_kf.append((t,shipx))
for k in order: k["tx"]=k["x"]+CS/2
bullets=[]; prev=None; hits=[]
for k in order:
    if prev is None or abs(prev["tx"]-k["tx"])>1:
        dist=abs(k["tx"]-shipx); t+=dist/SHIP_V+SETTLE; shipx=k["tx"]
        ship_kf.append((t,shipx))
    tf=t; dy=SHIP_Y-14-(k["y"]+CS); th=tf+dy/BUL_V
    bullets.append((tf,th,k)); k["th"]=th; t=tf+FIRE_GAP; ship_kf.append((t,shipx)); prev=k
END=t+2.0; T=END+0.8
ship_kf.append((END,shipx))
def kt(v): return f"{v/T:.4f}"
out=[]
def anim(attr,vals,kts,extra=""):
    return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{";".join(kts)}" dur="{T:.2f}s" repeatCount="indefinite" {extra}/>'
# ship (return to centre at end)
ship_kf=[(0.0,W/2)]+[(a,b) for a,b in ship_kf[1:]]
ship_kf.append((END+0.5,W/2))
ship_kf.append((T,W/2))
sk=";".join(kt(a) for a,_ in ship_kf); sv=";".join(f"{b-W/2:.1f} 0" for _,b in ship_kf)
ship=f'''<g transform="translate({W/2},{SHIP_Y})"><animateTransform attributeName="transform" type="translate" values="{";".join(f"{b:.1f} {SHIP_Y}" for _,b in ship_kf)}" keyTimes="{sk}" dur="{T:.2f}s" repeatCount="indefinite"/>
  <path d="M0 -13 L5 -2 L13 6 L13 9 L4 6 L2 12 L-2 12 L-4 6 L-13 9 L-13 6 L-5 -2 Z" fill="#4d8dff" stroke="#9cc2ff" stroke-width="0.8"/>
  <rect x="-1.2" y="12" width="2.4" height="5" rx="1" fill="#ffffff" opacity="0.8"><animate attributeName="height" values="3;7;3" dur="0.35s" repeatCount="indefinite"/></rect></g>'''
cellsvg=""; bulsvg=""; expsvg=""
for tf,th,k in bullets:
    col=LV[k["lv"]]; cx=k["tx"]; cy=k["y"]+CS/2
    fade=f'{kt(0)};{kt(th)};{kt(th+0.001)};{kt(T-0.7)};1'
    cellsvg+=f'<rect x="{k["x"]:.1f}" y="{k["y"]}" width="{CS}" height="{CS}" rx="2.5" fill="{col}">{anim("opacity","1;1;0;0;1",fade.split(";"))}<title>{k["date"]}: {k["n"]} contributions</title></rect>\n'
    ys=SHIP_Y-18; ye=k["y"]+CS
    bulsvg+=f'<rect x="{cx-1.2:.1f}" y="{ys}" width="2.4" height="9" rx="1.2" fill="#ffffff" opacity="0">{anim("opacity","0;0;1;0;0",[kt(0),kt(tf),kt(tf+0.001),kt(th),"1"] ,"")}{anim("y",f"{ys};{ys};{ye};{ye}",[kt(0),kt(tf),kt(th),"1"])}</rect>\n'
    expsvg+=f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2" fill="none" stroke="#ffd9d9" stroke-width="1.6" opacity="0">{anim("opacity","0;0;1;0;0",[kt(0),kt(th),kt(th+0.001),kt(th+0.45),"1"])}{anim("r","2;2;2;14;14",[kt(0),kt(th),kt(th+0.001),kt(th+0.45),"1"])}</circle>\n'
random.seed(7)
stars="".join(f'<circle cx="{random.uniform(8,W-8):.0f}" cy="{random.uniform(60,H-8):.0f}" r="{random.choice([0.6,0.8,1.0,1.2])}" fill="#fff" opacity="{random.choice([0.18,0.3,0.45])}"/>' for _ in range(70))
twinkle="".join(f'<circle cx="{random.uniform(20,W-20):.0f}" cy="{random.uniform(70,H-20):.0f}" r="1.3" fill="#fff"><animate attributeName="opacity" values="0.1;0.8;0.1" dur="{random.uniform(2.5,5):.1f}s" begin="{random.uniform(0,3):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(8))
emp="".join(f'<rect x="{x:.1f}" y="{y}" width="{CS}" height="{CS}" rx="2.5" fill="#ffffff" fill-opacity="0.045"/>' for x,y in empty+[(k["x"],k["y"]) for k in cells])
mon="".join(f'<text x="{x:.1f}" y="76" {M} font-size="9" fill="#6b727c">{m}</text>' for x,m in months)
leg=''.join(f'<rect x="{W-168+i*16}" y="31" width="10" height="10" rx="2.5" fill="{c}"'+(' fill-opacity="0.08"' if i==0 else '')+'/>' for i,c in enumerate(["#ffffff"]+list(LV.values())))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Contribution activity: {total} contributions in the last year</title>
  <desc id="d">Animated contribution graph. A spaceship moves along the bottom and shoots the days that have contributions, then the graph resets. {len(cells)} active days, {total} contributions in the last year.</desc>
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0d12"/><stop offset="1" stop-color="#14171d"/></linearGradient></defs>
  <rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
  {stars}
  {twinkle}
  <text x="30" y="40" {M} font-size="12" letter-spacing="2" fill="{RED}">CONTRIBUTIONS</text>
  <text x="170" y="40" {M} font-size="11" fill="#8b949e" fill-opacity="0.8">{total} contributions in the last year</text>
  <text x="{W-178}" y="39" text-anchor="end" {M} font-size="10" fill="#6b727c">less</text>
  {leg}
  <text x="{W-22}" y="39" text-anchor="end" {M} font-size="10" fill="#6b727c">more</text>
  <line x1="28" y1="52" x2="{W-28}" y2="52" stroke="{RED}" stroke-opacity="0.5" stroke-width="1.5"/>
  {mon}
  {emp}
{cellsvg}{bulsvg}{expsvg}  {ship}
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="19.5" fill="none" stroke="#ffffff" stroke-opacity="0.10"/>
</svg>
'''
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(svg)
print(len(svg), "T=%.1fs"%T, len(cells),"cells", total)
