import json
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from flask import Flask, session, request, redirect

DATA_DIR = Path(__file__).parent / "data"
clients = {}
linkedin_data = {}
if DATA_DIR.exists():
    for f in sorted(DATA_DIR.glob("*.json")):
        with open(f) as fh: d = json.load(fh)
        if "prospects" in d:
            linkedin_data = d
        else:
            clients[d["naam"]] = d

server = Flask(__name__)
server.secret_key = "bw-final-v2"
server.config["SESSION_COOKIE_SAMESITE"] = "Lax"
server.config["SESSION_COOKIE_HTTPONLY"] = True
server.config["SESSION_COOKIE_PATH"] = "/"
server.config["SESSION_PERMANENT"] = True

app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/",
    external_stylesheets=[dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"],
    suppress_callback_exceptions=True, title="BigWaves Conversiebureau",
    show_undo_redo=False)

app.index_string = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BigWaves Conversiebureau</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
{%metas%}
<style>
:root{--bg:#f5f6fa;--surface:#fff;--card:#fff;--border:#edf0f5;--text:#1a1a2e;--text-sec:#7e8299;--text-muted:#b5b7c4;--card-shadow:rgba(0,0,0,0.04);--sidebar-bg:#1e1e2d;--sidebar-text:#8a8ba7;--sidebar-hover:rgba(255,255,255,0.04);--sidebar-active:rgba(82,115,255,0.12);--sidebar-label:rgba(255,255,255,0.25);--sidebar-border:rgba(255,255,255,0.06);--sidebar-user:rgba(255,255,255,0.35);--primary:#5273ff;--green:#22c55e;--red:#ef4444;--yellow:#f59e0b;--purple:#8b5cf6;--chart-bg:#fff;--hover-shadow:0 4px 20px rgba(0,0,0,0.04)}
body.dark{--bg:#0f1117;--surface:#1a1d27;--card:#1e2231;--border:#2a2d3a;--text:#e8e8ed;--text-sec:#8a8ba7;--text-muted:#6b6d7b;--card-shadow:0 4px 20px rgba(0,0,0,0.2);--sidebar-bg:#0d0e15;--sidebar-text:#8a8ba7;--sidebar-hover:rgba(255,255,255,0.06);--sidebar-active:rgba(82,115,255,0.2);--sidebar-label:rgba(255,255,255,0.3);--sidebar-border:rgba(255,255,255,0.08);--sidebar-user:rgba(255,255,255,0.4);--chart-bg:#1a1d27;--hover-shadow:0 4px 20px rgba(0,0,0,0.3)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);transition:background 0.2s,color 0.2s}
.sidebar{position:fixed;top:0;left:0;width:255px;height:100vh;background:var(--sidebar-bg);z-index:1000;display:flex;flex-direction:column}
.sidebar-brand{padding:1.4rem 1.2rem 1rem;border-bottom:1px solid var(--sidebar-border)}
.sidebar-brand h2{color:#fff;font-size:1.1rem;font-weight:700}
.sidebar-brand small{color:var(--sidebar-user);font-size:0.65rem}
.sidebar-nav{flex:1;padding:0.6rem 0;overflow-y:auto}
.sidebar-nav a{display:flex;align-items:center;gap:0.7rem;padding:0.6rem 1.2rem;margin:1px 0.6rem;color:var(--sidebar-text);text-decoration:none;font-size:0.8rem;font-weight:500;border-radius:8px;transition:all 0.15s}
.sidebar-nav a:hover{color:#fff;background:var(--sidebar-hover)}
.sidebar-nav a.active{color:#fff;background:var(--sidebar-active)}
.sidebar-nav a i{width:16px;text-align:center;font-size:0.85rem}
.sidebar-nav .nav-label{font-size:0.6rem;color:var(--sidebar-label);font-weight:600;text-transform:uppercase;letter-spacing:0.6px;padding:1rem 1.2rem 0.4rem}
.sidebar-footer{padding:0.8rem 1rem;border-top:1px solid var(--sidebar-border)}
.sidebar-footer .client-row{display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem}
.sidebar-footer .client-avatar{width:28px;height:28px;border-radius:8px;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:0.9rem}
.sidebar-footer .client-name{color:#fff;font-size:0.78rem;font-weight:600}
.sidebar-footer .client-meta{color:var(--sidebar-user);font-size:0.63rem}
.sidebar-footer .logout-btn{width:100%;margin-top:0.4rem;padding:0.4rem;background:rgba(255,255,255,0.05);border:1px solid var(--sidebar-border);color:rgba(255,255,255,0.45);border-radius:8px;font-size:0.7rem;cursor:pointer;transition:all 0.15s;display:block;text-align:center;text-decoration:none}
.sidebar-footer .logout-btn:hover{background:rgba(255,255,255,0.1);color:#fff}
.main-content{margin-left:255px;padding:1.5rem 2rem;min-height:100vh}
.page-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem}
.page-header h1{font-size:1.3rem;font-weight:700;color:var(--text)}
.page-header .subtitle{color:var(--text-sec);font-size:0.75rem;margin-top:0.15rem}
.kpi-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;height:100%;transition:background 0.2s}
.kpi-card:hover{box-shadow:var(--hover-shadow)}
.kpi-icon{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.9rem;margin-bottom:0.5rem}
.kpi-label{font-size:0.65rem;color:var(--text-sec);font-weight:500;text-transform:uppercase;letter-spacing:0.5px}
.kpi-value{font-size:1.5rem;font-weight:700;color:var(--text);letter-spacing:-0.3px;line-height:1.2;margin:0.15rem 0 0.1rem}
.kpi-target{font-size:0.65rem;color:var(--text-muted)}
.kpi-trend{font-size:0.68rem;font-weight:500;margin-top:0.3rem}
.kpi-trend.up{color:var(--green)}.kpi-trend.down{color:var(--red)}.kpi-trend.neutral{color:var(--text-sec)}
.kpi-bar{width:100%;height:4px;background:var(--border);border-radius:4px;margin-top:0.4rem;overflow:hidden}
.kpi-bar-fill{height:100%;border-radius:4px;transition:width 0.4s ease}
.kpi-uitleg{font-size:0.6rem;color:var(--text-muted);margin-top:0.2rem;line-height:1.3}
.chart-box{background:var(--chart-bg);border:1px solid var(--border);border-radius:10px;padding:0.5rem;margin-bottom:0.8rem;transition:background 0.2s}
.kanal-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:0.8rem;text-align:center;height:100%;transition:background 0.2s}
.kanal-icon{font-size:1.4rem;margin-bottom:0.2rem;color:var(--primary)}
.kanal-name{font-size:0.6rem;color:var(--text-sec);text-transform:uppercase;letter-spacing:0.5px}
.kanal-val{font-size:1.3rem;font-weight:700;color:var(--text);margin:0.1rem 0}
.kanal-sub{font-size:0.68rem;color:var(--primary)}
.section-title{font-size:0.85rem;font-weight:600;color:var(--text);margin:1.2rem 0 0.6rem;display:flex;align-items:center;gap:0.4rem}
.bn-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:0.8rem 1rem;font-size:0.78rem;color:var(--text);border-left:3px solid var(--primary);margin:0.5rem 0;transition:background 0.2s}
.checkin-card{padding:0.8rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:10px;border-left:4px solid var(--green);transition:background 0.2s}
.checkin-card .ci-label{font-size:0.68rem;color:var(--text-sec)}
.checkin-card .ci-date{font-size:0.8rem;font-weight:600;color:var(--text);margin:0.1rem 0}
.checkin-card .ci-note{font-size:0.75rem;color:var(--text);opacity:0.7}
.login-wrapper{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--bg) 0%,#eef0f7 100%)}
.login-box{width:380px;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:2.5rem 2rem;box-shadow:0 8px 40px rgba(0,0,0,0.06);text-align:center}
.login-box .logo{font-size:2.2rem;margin-bottom:0.3rem}
.login-box h2{font-size:1.3rem;font-weight:700;color:var(--text);margin-bottom:0.2rem}
.login-box .tagline{color:var(--text-sec);font-size:0.78rem;margin-bottom:1.5rem}
.login-err{color:var(--red);font-size:0.75rem;margin-top:0.5rem;min-height:1.2rem}
.btn-pill{border-radius:200px;padding:0.35rem 1rem;font-size:0.75rem;font-weight:500;border:1px solid var(--border);background:var(--surface);cursor:pointer;transition:all 0.15s;color:var(--text)}
.btn-pill:hover{border-color:var(--primary);color:var(--primary)}
.info-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:0.8rem 1rem;height:100%;transition:background 0.2s}
.admin-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.5rem}
.detail-table{width:100%;border-collapse:collapse;font-size:0.75rem;margin-top:0.5rem}
.detail-table th{text-align:left;padding:0.4rem 0.6rem;color:var(--text-sec);font-weight:500;border-bottom:1px solid var(--border)}
.detail-table td{padding:0.4rem 0.6rem;border-bottom:1px solid var(--border)}
.badge{display:inline-block;padding:0.15rem 0.45rem;border-radius:200px;font-size:0.6rem;font-weight:600}
.badge.groen{background:rgba(34,197,94,0.1);color:var(--green)}
.badge.oranje{background:rgba(245,158,11,0.1);color:var(--yellow)}
.badge.rood{background:rgba(239,68,68,0.1);color:var(--red)}
.theme-toggle{padding:0.3rem 1rem;display:flex;align-items:center;gap:0.5rem;color:var(--sidebar-text);font-size:0.7rem;cursor:pointer;transition:all 0.15s;border:none;background:none;width:100%;text-align:left;border-radius:8px;margin:2px 0.6rem}
.theme-toggle:hover{color:#fff;background:var(--sidebar-hover)}
.theme-toggle i{width:16px;text-align:center;font-size:0.85rem}

/* Onboarding overlay */
.bw-onboard-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.55);z-index:9999;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.3s}
.bw-onboard-overlay.show{opacity:1;pointer-events:all}
.bw-onboard-box{background:#fff;border-radius:16px;padding:2.5rem 2.2rem;max-width:440px;text-align:center;box-shadow:0 16px 60px rgba(0,0,0,0.2)}
.bw-onboard-box .logo{font-size:2.5rem;margin-bottom:0.5rem}
.bw-onboard-box h2{font-size:1.2rem;font-weight:700;color:#1a1a2e;margin-bottom:0.3rem}
.bw-onboard-box .tag{color:#7e8299;font-size:0.78rem;margin-bottom:1.2rem;line-height:1.5}
.bw-onboard-box ul{text-align:left;list-style:none;padding:0;margin:0 0 1.2rem}
.bw-onboard-box ul li{padding:0.35rem 0;font-size:0.8rem;color:#1a1a2e;display:flex;align-items:center;gap:0.5rem}
.bw-onboard-box ul li i{width:18px;color:#5273ff;font-size:0.9rem}
.bw-onboard-box .btn{background:#5273ff;color:#fff;border:none;border-radius:200px;padding:0.5rem 2rem;font-size:0.82rem;font-weight:600;cursor:pointer}
.bw-onboard-box .btn:hover{background:#3f5ee6}

body.dark .bw-onboard-box{background:#1e2231}
body.dark .bw-onboard-box h2{color:#e8e8ed}
body.dark .bw-onboard-box .tag{color:#8a8ba7}
body.dark .bw-onboard-box ul li{color:#e8e8ed}

/* Period dropdown in sidebar */
.period-dropdown .Select-control{background:rgba(255,255,255,0.06)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:6px!important;min-height:28px!important;height:28px!important}
.period-dropdown .Select-control .Select-value{line-height:26px!important;color:rgba(255,255,255,0.7)!important;font-size:0.68rem!important;padding-left:6px!important}
.period-dropdown .Select-control .Select-arrow{border-color:rgba(255,255,255,0.3) transparent transparent!important}
.period-dropdown .Select-menu-outer{background:#2a2a3d!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:6px!important;z-index:9999!important}
.period-dropdown .Select-option{color:rgba(255,255,255,0.7)!important;font-size:0.68rem!important;padding:4px 8px!important}
.period-dropdown .Select-option:hover{background:rgba(82,115,255,0.2)!important;color:#fff!important}
.period-dropdown .Select-option.is-focused{background:rgba(82,115,255,0.15)!important;color:#fff!important}
.period-dropdown .Select-option.is-selected{background:rgba(82,115,255,0.25)!important;color:#fff!important}
.period-dropdown .Select-placeholder{color:rgba(255,255,255,0.4)!important;font-size:0.68rem!important;line-height:26px!important;padding-left:6px!important}
.period-dropdown .Select-input{height:26px!important}
.period-dropdown .Select-clear{color:rgba(255,255,255,0.3)!important}
.period-dropdown.is-open .Select-control .Select-arrow{border-color:transparent transparent rgba(255,255,255,0.3)!important}

@media(max-width:768px){
    .sidebar{width:60px}
    .sidebar-brand h2,.sidebar-brand small,.sidebar-nav .nav-label,.sidebar-nav a span,.sidebar-period,.sidebar-footer .client-meta,.sidebar-footer .client-name{display:none}
    .sidebar-footer .client-avatar{margin:0 auto}
    .sidebar-nav a{justify-content:center;padding:0.5rem 0;margin:1px 0.3rem}
    .sidebar-nav a i{margin:0}
    .theme-toggle span{display:none}
    .main-content{margin-left:60px;padding:0.8rem}
    .page-header{flex-direction:column;gap:0.5rem}
    .page-header h1{font-size:1rem}
    .kpi-card{padding:0.7rem 0.8rem}
    .kpi-value{font-size:1.1rem}
    .kpi-icon{width:26px;height:26px;font-size:0.7rem}
    .chart-box{padding:0.3rem}
}
@media(max-width:480px){
    .sidebar{width:48px}
    .main-content{margin-left:48px;padding:0.5rem}
    .page-header h1{font-size:0.9rem}
    .page-header .subtitle{font-size:0.65rem}
    .kpi-card{padding:0.5rem 0.6rem}
    .kpi-value{font-size:0.95rem}
    .kpi-icon{width:22px;height:22px;font-size:0.6rem}
    .kpi-label{font-size:0.55rem}
    .kpi-target,.kpi-trend{font-size:0.6rem}
    .kanal-card{padding:0.5rem}
    .kanal-val{font-size:1rem}
    .kanal-name{font-size:0.55rem}
    .checkin-card{padding:0.5rem 0.6rem}
    .checkin-card .ci-date{font-size:0.7rem}
    .checkin-card .ci-note{font-size:0.65rem}
    .section-title{font-size:0.75rem;margin:0.8rem 0 0.4rem}
    .btn-pill{font-size:0.65rem;padding:0.25rem 0.6rem}
}
</style>
{%css%}
</head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer>
<div class="bw-onboard-overlay" id="bw-onboard">
<div class="bw-onboard-box">
<div class="logo">🌊</div>
<h2>Welkom bij BigWaves</h2>
<p class="tag">Jij 1 call per week, wij regelen de rest.</p>
<ul>
<li><i class="fas fa-check-circle"></i> Jij hebt wekelijks 1 check-in call</li>
<li><i class="fas fa-robot"></i> Wij verwerken al het binnenkomende verkeer</li>
<li><i class="fas fa-chart-line"></i> Dit dashboard toont je resultaten</li>
<li><i class="fas fa-headset"></i> Bij vragen staan we voor je klaar</li>
</ul>
<button class="btn" onclick="document.getElementById('bw-onboard').classList.remove('show');try{localStorage.setItem('bw-onboarded','1')}catch(e){}">Aan de slag</button>
</div>
</div>
<div class="bw-notif-overlay" id="bw-notif">
<div class="bw-notif-panel">
<span class="close" onclick="document.getElementById('bw-notif').classList.remove('show')">&times;</span>
<h3>🔔 Notificaties</h3>
<div style="font-size:0.7rem;color:var(--text-sec);margin-bottom:1rem">Meldingen en herinneringen</div>
<div id="bw-notif-list"></div>
</div>
</div>
<script>
(function(){
  var o=document.getElementById('bw-onboard');
  if(o){
    try{
      if(!localStorage.getItem('bw-onboarded'))o.classList.add('show');
    }catch(e){o.classList.add('show')}
  }
  var nl=document.getElementById('bw-notif-list');
  if(nl){
    var n=[
      {l:'Check-in verlopen',t:'Gepland op 5 mei 2026.',d:'2 weken geleden',c:'#ef4444'},
      {l:'KPI data bijgewerkt',t:'Mei 2026 is geladen.',d:'2 dagen geleden',c:'#5273ff'},
      {l:'Doel behaald',t:'847 items verwerkt (doel: 800).',d:'Vandaag',c:'#22c55e'},
    ];
    nl.innerHTML=n.map(function(x){return '<div class=\"bw-notif-item\"><div class=\"ni-label\" style=\"color:'+x.c+'\">'+x.l+'</div><div>'+x.t+'</div><div class=\"ni-date\">'+x.d+'</div></div>';}).join('');
  }
})();
function toggleTheme(){
  var b=document.body;
  b.classList.toggle('dark');
  try{localStorage.setItem('bw-theme',b.classList.contains('dark')?'dark':'light')}catch(e){}
}
document.addEventListener('click',function(e){
  var t=e.target.closest('#theme-btn');
  if(t){e.preventDefault();toggleTheme()}
  var n=e.target.closest('#notif-btn');
  if(n){e.preventDefault();document.getElementById('bw-notif').classList.toggle('show')}
});
</script>
</body></html>"""

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="nl">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BigWaves — Inloggen</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:#f5f6fa;min-height:100vh;display:flex;align-items:center;justify-content:center}
.login-box{width:380px;background:#fff;border:1px solid #edf0f5;border-radius:16px;padding:2.5rem 2rem;box-shadow:0 8px 40px rgba(0,0,0,0.06);text-align:center}
.login-box .logo{font-size:2.2rem;margin-bottom:0.3rem}
.login-box h2{font-size:1.3rem;font-weight:700;color:#1a1a2e;margin-bottom:0.2rem}
.login-box .tagline{color:#7e8299;font-size:0.78rem;margin-bottom:1.5rem}
.login-box select{width:100%;padding:0.55rem 0.8rem;border:1px solid #e4e6ef;border-radius:10px;font-size:0.82rem;margin-bottom:0.7rem;background:#fff}
.login-box input{width:100%;padding:0.55rem 0.8rem;border:1px solid #e4e6ef;border-radius:10px;font-size:0.82rem;outline:none;margin-bottom:0.7rem}
.login-box input:focus{border-color:#5273ff}
.login-box button{width:100%;padding:0.55rem;background:#5273ff;color:#fff;border:none;border-radius:200px;font-size:0.82rem;font-weight:600;cursor:pointer}
.login-box button:hover{background:#3f5ee6}
.login-err{color:#ef4444;font-size:0.75rem;margin-top:0.5rem}
</style>
</head>
<body><div class="login-box"><div class="logo">🌊</div><h2>BigWaves</h2><p class="tagline">Performance Dashboard</p>
<form method="POST" action="/login"><select name="client">"""
for k in clients: LOGIN_PAGE += f'<option value="{k}">{k}</option>'
LOGIN_PAGE += """</select>
<input type="password" name="password" placeholder="Voer wachtwoord in">
<button type="submit">Inloggen</button>
<div class="login-err">ERROR_PLACEHOLDER</div></form></div></body></html>"""

@server.route("/")
def index():
    c = session.get("client")
    if c and c in clients: return redirect("/dashboard/")
    return LOGIN_PAGE.replace("ERROR_PLACEHOLDER", "")

@server.route("/login", methods=["POST"])
def login():
    c = request.form.get("client")
    pw = request.form.get("password")
    if c in clients and pw == clients[c].get("wachtwoord", "demo"):
        periods = list(clients[c].get("periodes", {}).keys())
        session["client"] = c; session["periode"] = periods[0] if periods else None
        session.permanent = True
        return redirect("/dashboard/")
    return LOGIN_PAGE.replace("ERROR_PLACEHOLDER", "Onjuist wachtwoord.")

@server.route("/uitloggen")
def logout():
    session.clear(); return redirect("/")

KPI_ICONS = {
    "Verwerkte items": ("fa-boxes", "rgba(82,115,255,0.08)", "#5273ff"),
    "Gem. responstijd": ("fa-clock", "rgba(34,197,94,0.08)", "#22c55e"),
    "Nauwkeurigheid": ("fa-bullseye", "rgba(245,158,11,0.08)", "#f59e0b"),
    "Uptime": ("fa-shield-alt", "rgba(82,115,255,0.08)", "#5273ff"),
    "Kwaliteitsborging": ("fa-shield-alt", "rgba(34,197,94,0.08)", "#22c55e"),
    "Kostenbesparing": ("fa-euro-sign", "rgba(34,197,94,0.08)", "#22c55e"),
}
KAN_ICON = {"website":"fa-globe","mail":"fa-envelope","whatsapp":"fa-whatsapp","telefoon":"fa-phone"}
PAGE_LABELS = {"dashboard":"Dashboard","conversie":"Conversie","inzichten":"Inzichten","admin":"Admin","linkedin":"LinkedIn Outreach"}
PAGE_ICONS = {"dashboard":"fa-chart-pie","conversie":"fa-chart-line","inzichten":"fa-lightbulb","admin":"fa-cog","linkedin":"fa-linkedin"}
PAGE_ORDERS = ["dashboard", "conversie", "inzichten", "linkedin"]

def status_emoji(s): return {"groen":"🟢","oranje":"🟠","rood":"🔴"}.get(s,"⚪")
se = status_emoji
def trend_class(t):
    if not t: return "neutral"
    if "+" in t or "lager" in t.lower(): return "up"
    if "-" in t: return "down"
    return "neutral"
tc = trend_class
def trend_arrow(t): return "↑" if trend_class(t)=="up" else "↓" if trend_class(t)=="down" else "→"
ta = trend_arrow
def trend_col(t): return "#22c55e" if trend_class(t)=="up" else "#ef4444" if trend_class(t)=="down" else "#7e8299"
tcol = trend_col
def fmt_val(w,e):
    if e=="euro": return f"€{w:,}" if isinstance(w,int) else f"€{w}"
    if e=="seconden": return f"{w}s"
    if e=="%": return f"{w}%"
    return f"{w:,}" if isinstance(w,int) else str(w)
fv = fmt_val
PAGE_LABELS = {"dashboard":"Dashboard","conversie":"Conversie","inzichten":"Inzichten","admin":"Admin","linkedin":"LinkedIn Outreach"}

def kpi_progress(waarde, doel):
    if not doel or doel == 0:
        return ""
    pct = min(round(waarde / doel * 100), 100)
    color = "#22c55e" if pct >= 100 else "#f59e0b" if pct >= 80 else "#ef4444"
    return html.Div(html.Div(style={"width": f"{pct}%", "background": color}, className="kpi-bar-fill"), className="kpi-bar")

def build_checkin_badge(d):
    gt = d.get("groei_team", {})
    if not gt:
        return ""
    volgende = gt.get("volgende_checkin", "")
    if not volgende:
        return ""
    from datetime import datetime, date
    try:
        v_datum = datetime.strptime(volgende, "%Y-%m-%d").date()
        vandaag = date.today()
        delta = (v_datum - vandaag).days
        if delta < 0:
            icon, label, color = "🔴", "Check-in verlopen", "#ef4444"
        elif delta <= 2:
            icon, label, color = "🟡", f"Check-in over {delta} dag", "#f59e0b"
        elif delta <= 7:
            icon, label, color = "🟢", f"Check-in over {delta} dagen", "#22c55e"
        else:
            icon, label, color = "⚪", f"Check-in over {delta} dagen", "rgba(255,255,255,0.35)"
        return html.Div([html.Span(icon, style={"marginRight":"0.3rem"}), html.Span(label)], style={"fontSize":"0.62rem","color":color,"margin":"0.2rem 0 0.4rem 0","padding":"0 0.2rem"})
    except (ValueError, TypeError):
        return ""

def build_sidebar(cn, pe, active_page):
    d = clients[cn]
    nav_items = []
    for key in PAGE_ORDERS:
        label = PAGE_LABELS.get(key, key)
        icon = PAGE_ICONS.get(key, "fa-circle")
        active_cls = " active" if key == active_page else ""
        url = "/dashboard/" + key if key != "dashboard" else "/dashboard/"
        icon_base = "fab" if key == "linkedin" else "fas"
        nav_items.append(
            html.A([html.I(className=f"{icon_base} {icon}"), html.Span(label)], href=url, className=active_cls)
        )
    return html.Div([html.Div([html.H2("🌊 BigWaves"), html.Small("Conversiebureau")], className="sidebar-brand"),
        html.Div([html.Div("Menu", className="nav-label"), *nav_items,
            html.A([html.I(className="fas fa-moon"), html.Span("Donker thema")], href="#", className="theme-toggle", id="theme-btn"),
            html.Div("Periode", className="nav-label"),
            html.Div(dcc.Dropdown(id="period-select", options=[{"label": p, "value": p} for p in list(d.get("periodes", {}).keys())], value=pe, clearable=False, className="period-dropdown"), style={"padding": "0 0.8rem 0.6rem"}),
            html.A([html.I(className="fas fa-chart-simple"), html.Span("Vergelijk met vorige")], href="/dashboard/vergelijk", className="theme-toggle", id="compare-btn"),
        ], className="sidebar-nav"),
        html.Div([html.Div([html.Div(d.get("logo", "🌊"), className="client-avatar"),
            html.Div([html.Div(cn, className="client-name"), html.Div(f"Periode: {pe}", className="client-meta")])], className="client-row"),
            # Check-in notificatie badge
            build_checkin_badge(d),
            html.A("Uitloggen", href="/uitloggen", className="logout-btn")], className="sidebar-footer")], className="sidebar")

def build_page(cn, pe, active_page="dashboard", vergelijk=False):
    d = clients[cn]; ps = d.get("periodes",{})
    if not pe or pe not in ps: pe = list(ps.keys())[0] if ps else None
    if not pe: return "Geen data"
    pd = ps[pe].copy()
    full = {k:v for k,v in d.items() if k!="periodes"}; full.update(pd); full["periode"] = pe
    kpis = full.get("kpis",{}); graf = full.get("grafieken",{}); kan = full.get("kanalen",{})
    bn = full.get("bottleneck",{}); gt = d.get("groei_team",{}); chk = gt.get("checkin_historie",[]) if gt else []
    logo = d.get("logo","🌊")

    # Laad vorige periode voor vergelijking
    vorige_data = None
    vorige_pe = None
    if vergelijk:
        period_keys = sorted(ps.keys())
        cur_idx = period_keys.index(pe) if pe in period_keys else -1
        if cur_idx > 0:
            vorige_pe = period_keys[cur_idx - 1]
            vorige_data = ps[vorige_pe]

    kpi_cards = []
    for i,(nm,inf) in enumerate(list(kpis.items())[:4]):
        w,e = inf["waarde"],inf.get("eenheid",""); t = inf.get("trend",""); do = inf.get("doel",0)
        ic = KPI_ICONS.get(nm,("fa-chart-bar","rgba(82,115,255,0.08)","#5273ff"))
        
        # Vergelijkingskolom
        vergelijk_html = []
        if vergelijk and vorige_data:
            v_kpis = vorige_data.get("kpis", {})
            if nm in v_kpis:
                vw = v_kpis[nm]["waarde"]
                delta = w - vw
                delta_pct = round((delta / vw) * 100, 1) if vw else 0
                delta_str = f"+{delta_pct}%" if delta >= 0 else f"{delta_pct}%"
                delta_color = "#22c55e" if delta >= 0 else "#ef4444"
                vergelijk_html = [html.Div([
                    html.Span(f"Vorige: {fv(vw,e)}", style={"fontSize":"0.6rem","color":"var(--text-muted)","marginRight":"0.3rem"}),
                    html.Span(delta_str, style={"fontSize":"0.6rem","fontWeight":"600","color":delta_color}),
                ], style={"marginTop":"0.15rem"})]
        
        kpi_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {ic[0]}",style={"color":ic[2]}),className="kpi-icon",style={"background":ic[1]}),
            html.Div(nm,className="kpi-label"),html.Div(fv(w,e),className="kpi-value"),
            html.Div(f"Doel: {do}",className="kpi-target"),
            html.Div(f"{ta(t)} {t}",className=f"kpi-trend {tc(t)}",style={"color":tcol(t)}),
            *vergelijk_html,
            kpi_progress(w, do)],className="kpi-card"),
            width=3,style={"padding":"0 0.4rem","marginBottom":"0.5rem"},
            xs=12,sm=6,md=3))

    charts = []
    if graf:
        row = []
        for k,gr in graf.items():
            if k == "hitl_trend":
                continue  # skip HITL grafiek, niet klantgericht
            fig = go.Figure(); fig.add_trace(go.Bar(x=gr["labels"],y=gr["waarden"],marker_color="#5273ff",opacity=0.85))
            if "doel" in gr: fig.add_hline(y=gr["doel"],line_dash="dash",line_color="#f59e0b",annotation_text=f"Doel: {gr['doel']}",annotation_position="top left")
            fig.update_layout(title=dict(text=gr["titel"],font=dict(size=12,color="#1a1a2e"),x=0.02),height=240,margin=dict(l=16,r=16,t=32,b=16),paper_bgcolor="#fff",plot_bgcolor="#fff",font=dict(size=10,color="#7e8299"),yaxis=dict(gridcolor="#f1efed"),xaxis=dict(gridcolor="#f1efed"),hoverlabel=dict(bgcolor="#5273ff",font_color="white"),showlegend=False)
            row.append(dbc.Col(html.Div(dcc.Graph(figure=fig,config={"displayModeBar":False}),className="chart-box"),width=6,style={"padding":"0 0.4rem","marginBottom":"0.5rem"},xs=12,lg=6))
        charts = [dbc.Row(row,style={"margin":"0 -0.4rem"})]

    kan_section = []
    if kan:
        row = []
        for nm,inf in sorted(kan.items()):
            ic = KAN_ICON.get(nm.lower(),"fa-inbox")
            row.append(dbc.Col(html.Div([html.Div(html.I(className=f"fas {ic}"),className="kanal-icon"),html.Div(nm,className="kanal-name"),html.Div(str(inf.get("verwerkt",0)),className="kanal-val"),html.Div(f"{inf.get('bestellingen',0)} bestellingen",className="kanal-sub")],className="kanal-card"),width=12//len(kan),style={"padding":"0 0.4rem","marginBottom":"0.5rem"}))
        kan_section = [html.Div([html.I(className="fas fa-inbox",style={"color":"#5273ff"})," Kanalen"],className="section-title"),dbc.Row(row,style={"margin":"0 -0.4rem"})]

    bn_section = []
    if bn and bn.get("tekst"): bn_section = [html.Div([html.Strong("🔍 Bottleneck-analyse "),bn["tekst"]],className="bn-card")]

    inz_section = []
    if chk:
        laatste = chk[0]; s = laatste.get("status","groen"); c = "#22c55e" if s=="groen" else "#f59e0b"
        inz_section = [html.Div([html.I(className="fas fa-lightbulb",style={"color":"#f59e0b"})," Inzichten"],className="section-title"),
            dbc.Row([dbc.Col(html.Div([html.Div("Laatste check-in",className="ci-label"),html.Div(laatste.get("datum",""),className="ci-date"),html.Div(laatste.get("notities",""),className="ci-note")],className="checkin-card",style={"borderLeftColor":c}),width=6,style={"padding":"0 0.4rem"}),
                dbc.Col(html.Div([html.Div("Check-ins totaal",className="ci-label"),html.Div(str(len(chk)),className="ci-date"),html.Div("allemaal op groen" if all(ch.get("status")=="groen" for ch in chk) else f"{sum(1 for ch in chk if ch.get('status')=='groen')} groen",className="ci-note")],className="checkin-card",style={"borderLeftColor":"#5273ff"}),width=6,style={"padding":"0 0.4rem"})],style={"margin":"0 -0.4rem"})]

    # Vergelijk badge in header
    vergelijk_badge = []
    if vergelijk and vorige_data:
        vergelijk_badge = [html.Span(" vs " + vorige_pe, style={"fontSize":"0.7rem","fontWeight":"500","color":"var(--primary)","marginLeft":"0.3rem"})]

    main = html.Div([html.Div([html.Div([html.H1("Dashboard"),html.Div(f"Performance overzicht . {pe}",className="subtitle"),*vergelijk_badge]),
        html.Div([
            html.A("📄 PDF", href="/export/pdf", className="btn-pill", style={"marginRight":"0.3rem","textDecoration":"none"}),
            html.A("📧 Mail PDF", href="/export/mail-pdf", className="btn-pill", style={"marginRight":"0.3rem","textDecoration":"none"}),
            html.A("📊 CSV", href="/export/csv", className="btn-pill", style={"marginRight":"0.3rem","textDecoration":"none"}),
            html.A("🔔 Notificaties", href="#", className="btn-pill", style={"textDecoration":"none"}, id="notif-btn"),
        ])],className="page-header"),
        dbc.Row(kpi_cards,style={"margin":"0 -0.4rem"}),*charts,*kan_section,*bn_section,*inz_section],className="main-content")
    return main

# ── Export routes ────────────────────────────────────────────────────────────

@server.route("/export/csv")
def export_csv():
    c = session.get("client")
    pe = session.get("periode")
    if not c or c not in clients:
        return redirect("/")
    d = clients[c]
    ps = d.get("periodes", {})
    if not pe or pe not in ps:
        pe = list(ps.keys())[0] if ps else None
    if not pe:
        return "Geen data", 404
    pd = ps[pe]
    kpis = pd.get("kpis", {})
    kan = d.get("kanalen", {})
    hitl = pd.get("hitl_detail", {})
    gt = d.get("groei_team", {})

    import csv, io
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["BigWaves Conversiebureau - Export", c, pe])
    w.writerow([])
    w.writerow(["KPI", "Waarde", "Doel", "Eenheid", "Trend"])
    for nm, inf in kpis.items():
        w.writerow([nm, inf["waarde"], inf.get("doel",""), inf.get("eenheid",""), inf.get("trend","")])
    w.writerow([])
    w.writerow(["Kanaal", "Verwerkt", "Bestellingen"])
    for nm, inf in sorted(kan.items()):
        w.writerow([nm, inf.get("verwerkt",0), inf.get("bestellingen",0)])
    if hitl:
        w.writerow([])
        w.writerow(["HITL Categorie", "Totaal", "HITL", "%"])
        for cn_, cd in hitl.get("categorieen",{}).items():
            w.writerow([cn_, cd.get("totaal",0), cd.get("hitl",0), f"{cd.get('percentage',0)}%"])
    if gt:
        w.writerow([])
        w.writerow(["Workflow", "Type", "Items", "Status"])
        for wf in gt.get("workflows",[]):
            w.writerow([wf.get("naam",""), wf.get("type",""), wf.get("items_verwerkt",0), wf.get("status","")])

    resp = app.server.response_class(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="bigwaves-{c}-{pe}.csv"'},
    )
    return resp

@server.route("/export/pdf")
def export_pdf():
    c = session.get("client")
    pe = session.get("periode")
    if not c or c not in clients:
        return redirect("/")
    d = clients[c]
    ps = d.get("periodes", {})
    if not pe or pe not in ps:
        pe = list(ps.keys())[0] if ps else None
    if not pe:
        return "Geen data", 404
    pd = ps[pe]
    kpis = pd.get("kpis", {})
    kan = d.get("kanalen", {})
    gt = d.get("groei_team", {})
    chk = gt.get("checkin_historie", []) if gt else []
    hitl = pd.get("hitl_detail", {})

    def s(v):
        return fmt_val(v.get("waarde"), v.get("eenheid","")) if isinstance(v,dict) else str(v)
    def e(v):
        return v.get("eenheid","") if isinstance(v,dict) else ""

    kpi_rows = ""
    for nm, inf in kpis.items():
        kpi_rows += f"<tr><td>{nm}</td><td>{inf['waarde']}{' '+inf.get('eenheid','') if inf.get('eenheid','') else ''}</td><td>{inf.get('doel','')}</td><td>{inf.get('trend','')}</td></tr>"

    kan_rows = ""
    for nm, inf in sorted(kan.items()):
        kan_rows += f"<tr><td>{nm}</td><td>{inf.get('verwerkt',0)}</td><td>{inf.get('bestellingen',0)}</td></tr>"

    wf_rows = ""
    for wf in gt.get("workflows",[]):
        wf_rows += f"<tr><td>{wf.get('naam','')}</td><td>{wf.get('type','')}</td><td>{wf.get('items_verwerkt',0)}</td><td>{wf.get('status','')}</td></tr>"

    chk_rows = ""
    for ch in chk:
        chk_rows += f"<tr><td>{ch.get('datum','')}</td><td>{ch.get('type','')}</td><td>{ch.get('notities','')}</td><td>{ch.get('status','')}</td></tr>"

    hitl_rows = ""
    if hitl:
        for cn_, cd in hitl.get("categorieen",{}).items():
            hitl_rows += f"<tr><td>{cn_}</td><td>{cd.get('totaal',0)}</td><td>{cd.get('hitl',0)}</td><td>{cd.get('percentage',0)}%</td></tr>"

    html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
body{{font-family:'Inter',sans-serif;padding:2rem;color:#1a1a2e;font-size:12px}}
h1{{font-size:1.3rem;margin-bottom:0.2rem}}
.sub{{color:#7e8299;font-size:0.75rem;margin-bottom:1rem}}
table{{width:100%;border-collapse:collapse;margin-bottom:1.5rem}}
th{{text-align:left;padding:6px 8px;background:#f5f6fa;color:#7e8299;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid #edf0f5}}
td{{padding:6px 8px;border-bottom:1px solid #f5f6fa;font-size:0.75rem}}
h2{{font-size:0.9rem;margin:1rem 0 0.3rem;color:#1a1a2e}}
@media print{{body{{padding:0}}}}
</style></head><body>
<h1>🌊 BigWaves Conversiebureau</h1>
<div class="sub">{c} • {pe} • Gegenereerd op ___DATE___</div>
<h2>📊 KPI's</h2>
<table><thead><tr><th>KPI</th><th>Waarde</th><th>Doel</th><th>Trend</th></tr></thead><tbody>{kpi_rows}</tbody></table>
<h2>📬 Kanalen</h2>
<table><thead><tr><th>Kanaal</th><th>Verwerkt</th><th>Bestellingen</th></tr></thead><tbody>{kan_rows}</tbody></table>"""

    if wf_rows:
        html_content += f"""<h2>⚙️ Workflows</h2><table><thead><tr><th>Workflow</th><th>Type</th><th>Items</th><th>Status</th></tr></thead><tbody>{wf_rows}</tbody></table>"""

    if hitl_rows:
        html_content += f"""<h2>🤖 HITL Categorieën</h2><table><thead><tr><th>Categorie</th><th>Totaal</th><th>HITL</th><th>%</th></tr></thead><tbody>{hitl_rows}</tbody></table>"""

    if chk_rows:
        html_content += f"""<h2>📋 Check-ins</h2><table><thead><tr><th>Datum</th><th>Type</th><th>Notities</th><th>Status</th></tr></thead><tbody>{chk_rows}</tbody></table>"""

    html_content += "</body></html>"
    html_content = html_content.replace("___DATE___", __import__("datetime").datetime.now().strftime("%d-%m-%Y %H:%M"))

    resp = app.server.response_class(html_content, mimetype="text/html")
    resp.headers["Content-Disposition"] = f'inline; filename="bigwaves-{c}-{pe}.html"'
    return resp

@server.route("/export/mail-pdf")
def export_mail_pdf():
    c = session.get("client")
    pe = session.get("periode")
    if not c or c not in clients:
        return redirect("/")
    import urllib.parse
    subject = f"BigWaves rapport - {c} - {pe}"
    body = f"Beste,\n\nHierbij het BigWaves rapport voor {c} - {pe}.\n\nBekijk het dashboard voor de volledige rapportage:\nhttps://dashboard.bigwaves.nl/\n\n--\nBigWaves Conversiebureau"
    mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    return redirect(mailto)

@server.route("/dashboard/vergelijk")
def toggle_vergelijk():
    c = session.get("client")
    if not c or c not in clients:
        return redirect("/")
    cur = session.get("vergelijk", False)
    session["vergelijk"] = not cur
    return redirect("/dashboard/?v=1")

@server.route("/admin/nieuw", methods=["GET", "POST"])
def admin_nieuwe_klant():
    c = session.get("client")
    if not c or c not in clients:
        return redirect("/")
    if request.method == "GET":
        admin_form = """<h1>Nieuwe klant aanmaken</h1>
<div class="sub">Er wordt een JSON template gegenereerd in de data directory</div>
<form method="POST">
<label>Klantnaam</label><input name="naam" required>
<label>Wachtwoord</label><input name="wachtwoord" value="demo">
<label>Pakket</label><select name="pakket"><option>Start</option><option selected>Groei</option><option>Pro</option></select>
<label>Maandprijs (EUR)</label><input name="prijs" type="number" value="1497">
<label>Setup (EUR)</label><input name="setup" type="number" value="2500">
<label>Aantal workflows</label><input name="workflows" type="number" value="2">
<button class="btn" type="submit">Genereer template</button>
</form></body></html>"""
        msg = request.args.get("msg", "")
        success = '<div class="success">' + msg + "</div>" if msg else ""
        return admin_form.replace("<form", success + "<form")
    
    # POST: genereer template
    import json, os
    from datetime import datetime
    n = request.form.get("naam", "Nieuwe Klant").strip()
    pw = request.form.get("wachtwoord", "demo")
    pakket = request.form.get("pakket", "Groei")
    prijs = int(request.form.get("prijs", 1497))
    setup = int(request.form.get("setup", 2500))
    wf_count = int(request.form.get("workflows", 2))
    
    jaarprijs = prijs * 12 - (prijs * 12 // 10)  # 10% korting
    jaarprijs = round(jaarprijs, -2)  # afronden op 100
    
    template = {
        "naam": n,
        "logo": "🌊",
        "accent_kleur": "#5273ff",
        "wachtwoord": pw,
        "groei_team": {
            "pakket": pakket,
            "sinds": datetime.now().strftime("%Y-%m-%d"),
            "prijs": {"huidig": prijs, "eenheid": "maand", "setup": setup, "jaar": jaarprijs, "workflows": wf_count},
            "status": "actief",
            "contact_frequentie": "wekelijks",
            "health_score": 85,
            "workflows": [{"naam": f"Workflow {i+1}", "type": "lead", "actief": True, "items_verwerkt": 0, "opvolgmomenten": 0, "status": "groen"} for i in range(wf_count)],
            "hitl_samenvatting": {"deze_maand_goedgekeurd": 0, "deze_maand_geweigerd": 0, "wachttijd_gemiddeld": "0 uur"},
            "checkin_historie": []
        },
        "kanalen": {"website": {"verwerkt": 0, "bestellingen": 0}, "mail": {"verwerkt": 0, "bestellingen": 0}, "whatsapp": {"verwerkt": 0, "bestellingen": 0}, "telefoon": {"verwerkt": 0, "bestellingen": 0}},
        "periodes": {}
    }
    
    filepath = DATA_DIR / f"{n.lower().replace(' ', '-')}.json"
    with open(filepath, "w") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    return redirect("/admin/nieuw?msg=Template+opgeslagen:+{}".format(filepath.name))

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="dash-content"),
])

@app.callback(Output("dash-content", "children"), Input("url", "pathname"), Input("url", "search"))
def router(pathname, search):
    c = session.get("client")
    pe = session.get("periode")
    if not c or c not in clients:
        return html.Div([html.H2("Niet ingelogd"), html.P(html.A("Ga naar inlogpagina", href="/"))],
                        style={"textAlign": "center", "marginTop": "4rem"})

    path = pathname or "/dashboard/"
    if path in ("/dashboard/", "/dashboard", "/dashboard/dashboard"):
        active = "dashboard"
    else:
        parts = path.strip("/").split("/")
        active = parts[-1] if len(parts) > 1 else "dashboard"
        if active not in PAGE_ORDERS:
            active = "dashboard"

    vergelijk = session.get("vergelijk", False) or (search and "v=1" in search)

    if active == "dashboard":
        main = build_page(c, pe, active, vergelijk)
    elif active == "conversie":
        main = build_conversie_page(c, pe)
    elif active == "inzichten":
        main = build_inzichten_page(c, pe)
    elif active == "admin":
        main = build_admin_page(c, pe)
    elif active == "linkedin":
        main = build_linkedin_page(c, pe)
    else:
        main = build_page(c, pe, "dashboard")
    sidebar = build_sidebar(c, pe, active)
    return html.Div([sidebar, main])
@app.callback(Output("period-store", "data"),
              Input("period-select", "value"),
              prevent_initial_call=True)
def update_period(pe):
    c = session.get("client")
    if c and pe:
        session["periode"] = pe
    return {"periode": pe}

def build_conversie_page(cn, pe):
    d = clients[cn]
    ps = d.get("periodes", {})
    if not pe or pe not in ps:
        pe = list(ps.keys())[0] if ps else None
    if not pe:
        return "Geen data"
    pd = ps[pe]
    kpis = pd.get("kpis", {})
    hitl = pd.get("hitl_detail", {})

    # Hernoem de HITL-ratio KPI naar "Kwaliteitsborging" in de conversie pagina
    kpi_cards = []
    for nm, inf in list(kpis.items())[:6]:
        w, e = inf["waarde"], inf.get("eenheid", "")
        t = inf.get("trend", "")
        do = inf.get("doel", 0)
        # Hernoem HITL-ratio naar klantvriendelijke term
        label = "Kwaliteitsborging" if nm == "HITL-ratio" else nm
        ic = KPI_ICONS.get(nm, ("fa-chart-bar", "rgba(82,115,255,0.08)", "#5273ff"))
        kpi_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {ic[0]}", style={"color": ic[2]}), className="kpi-icon", style={"background": ic[1]}),
            html.Div(label, className="kpi-label"),
            html.Div(fmt_val(w, e), className="kpi-value"),
            html.Div(f"Doel: {do}", className="kpi-target"),
            html.Div(f"{trend_arrow(t)} {t}", className=f"kpi-trend {trend_class(t)}", style={"color": trend_col(t)}),
            kpi_progress(w, do),
        ], className="kpi-card"), width=4, style={"padding": "0 0.4rem", "marginBottom": "0.5rem"}, xs=12, sm=6, lg=4))

    kwaliteit_section = []
    if hitl:
        totaal = hitl.get("totaal_acties", 0)
        mens = hitl.get("menselijke_check", 0)
        auto = hitl.get("geautomatiseerd", 0)
        saved = hitl.get("bespaarde_uren", 0)
        cat = hitl.get("categorieen", {})

        # Klantvriendelijke kwaliteitscontrole kaarten
        kwaliteit_cards = dbc.Row([
            dbc.Col(html.Div([html.Div("Totaal verwerkt", className="ci-label"), html.Div(str(totaal), className="ci-date")], className="checkin-card", style={"borderLeftColor": "#5273ff"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Extra gecontroleerd", className="ci-label"), html.Div(str(mens), className="ci-date"), html.Div(f"{round(mens/totaal*100) if totaal else 0}% voor kwaliteit", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#22c55e"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Foutloos verwerkt", className="ci-label"), html.Div(str(auto), className="ci-date"), html.Div("geen fouten gemeld", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#8b5cf6"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Tijd bespaard", className="ci-label"), html.Div(f"{saved}h", className="ci-date"), html.Div("deze periode", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#f59e0b"}), width=3, style={"padding": "0 0.3rem"}),
        ], style={"margin": "0 -0.3rem", "marginBottom": "0.8rem"})

        cat_rows = []
        for cn_, cd in cat.items():
            cat_rows.append(html.Tr([html.Td(cn_), html.Td(str(cd.get("totaal", 0))), html.Td(str(cd.get("hitl", 0))), html.Td(f"{cd.get('percentage', 0)}%")]))

        cat_table = html.Table([
            html.Thead(html.Tr([html.Th("Categorie"), html.Th("Totaal"), html.Th("Gecontroleerd"), html.Th("%")])),
            html.Tbody(cat_rows),
        ], className="detail-table")

        kwaliteit_section = [
            html.Div([html.I(className="fas fa-shield-alt", style={"color": "#22c55e"}), " Kwaliteitscontrole"], className="section-title"),
            kwaliteit_cards,
            html.Div(cat_table, className="admin-card"),
        ]

    return html.Div([html.Div([html.H1("Conversie"), html.Div(f"KPI-overzicht . {pe}", className="subtitle")], className="page-header"),
        dbc.Row(kpi_cards, style={"margin": "0 -0.4rem"}),
        *kwaliteit_section], className="main-content")

def build_inzichten_page(cn, pe):
    d = clients[cn]
    gt = d.get("groei_team", {})
    chk = gt.get("checkin_historie", []) if gt else []
    ps = d.get("periodes", {})
    pd = ps.get(pe, {})
    bn = pd.get("bottleneck", {})
    kan = d.get("kanalen", {})

    checkin_cards = []
    for ch in chk:
        s = ch.get("status", "groen")
        c = "#22c55e" if s == "groen" else "#f59e0b" if s == "oranje" else "#ef4444"
        checkin_cards.append(dbc.Col(html.Div([
            html.Div(ch.get("type", "Check-in"), className="ci-label"),
            html.Div(ch.get("datum", ""), className="ci-date"),
            html.Div(ch.get("notities", ""), className="ci-note"),
            html.Div(status_emoji(s), style={"marginTop": "0.3rem", "fontSize": "0.8rem"}),
        ], className="checkin-card", style={"borderLeftColor": c}), width=6, style={"padding": "0 0.4rem", "marginBottom": "0.5rem"}))

    bn_section = []
    if bn and bn.get("tekst"):
        bc = "#ef4444" if bn.get("prioriteit") == "hoog" else "#f59e0b" if bn.get("prioriteit") == "medium" else "#22c55e"
        bn_section = [html.Div([html.Strong(" Bottleneck-analyse "), bn["tekst"]], className="bn-card", style={"borderLeftColor": bc})]

    kan_cards = []
    for nm, inf in sorted(kan.items()):
        ic = KAN_ICON.get(nm.lower(), "fa-inbox")
        verwerkt = inf.get("verwerkt", 0)
        best = inf.get("bestellingen", 0)
        conv = round(best / verwerkt * 100, 1) if verwerkt else 0
        kan_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {ic}"), className="kanal-icon"),
            html.Div(nm, className="kanal-name"),
            html.Div(str(verwerkt), className="kanal-val"),
            html.Div(f"{best} bestellingen", className="kanal-sub"),
            html.Div(f"{conv}% conversie", style={"fontSize": "0.6rem", "color": "#22c55e"}),
        ], className="kanal-card"), width=12//len(kan), style={"padding": "0 0.4rem", "marginBottom": "0.5rem"}))

    return html.Div([html.Div([html.H1("Inzichten"), html.Div(f"Analyse en historie . {pe}", className="subtitle")], className="page-header"),
        *bn_section,
        html.Div([html.I(className="fas fa-inbox", style={"color": "#5273ff"}), " Kanalen met conversie"], className="section-title"),
        dbc.Row(kan_cards, style={"margin": "0 -0.4rem"}),
        html.Div([html.I(className="fas fa-history", style={"color": "#f59e0b"}), " Check-in geschiedenis"], className="section-title"),
        dbc.Row(checkin_cards, style={"margin": "0 -0.4rem"})], className="main-content")

def build_admin_page(cn, pe):
    d = clients[cn]
    gt = d.get("groei_team", {})

    gt_info = []
    if gt:
        pakket = gt.get("pakket", "-")
        status = gt.get("status", "-")
        prijs = gt.get("prijs", {})
        wfs = gt.get("workflows", [])
        hitl = gt.get("hitl_samenvatting", {})

        gt_info = [html.Div([
            html.Div([html.Div("Pakket", className="ci-label"), html.Div(pakket, style={"fontSize": "1rem", "fontWeight": "700", "color": "#1a1a2e"}), html.Div(f"EUR{prijs.get('huidig', 0):,}/mnd", style={"fontSize": "0.75rem", "color": "#5273ff"})], className="checkin-card", style={"borderLeftColor": "#5273ff"}),
            html.Div([html.Div("Status", className="ci-label"), html.Div(status, className="ci-date"), html.Div(f"Sinds {gt.get('sinds', '-')}", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#22c55e"}),
        ], style={"display": "flex", "gap": "0.5rem", "marginBottom": "0.8rem"})]

        wf_rows = []
        for wf in wfs:
            s = wf.get("status", "groen")
            wf_rows.append(html.Tr([
                html.Td(wf.get("naam", "-")),
                html.Td(wf.get("type", "-")),
                html.Td(str(wf.get("items_verwerkt", 0))),
                html.Td(str(wf.get("opvolgmomenten", 0))),
                html.Td(html.Span(s, className=f"badge {s}")),
            ]))

        wf_table = html.Table([
            html.Thead(html.Tr([html.Th("Workflow"), html.Th("Type"), html.Th("Items"), html.Th("Opvolgingen"), html.Th("Status")])),
            html.Tbody(wf_rows),
        ], className="detail-table")
        gt_info.append(html.Div([html.H3("Workflows"), wf_table], className="admin-card"))

        if hitl:
            gt_info.append(dbc.Row([
                dbc.Col(html.Div([html.Div("Goedgekeurd", className="ci-label"), html.Div(str(hitl.get("deze_maand_goedgekeurd", 0)), className="ci-date")], className="checkin-card", style={"borderLeftColor": "#22c55e"}), width=4),
                dbc.Col(html.Div([html.Div("Geweigerd", className="ci-label"), html.Div(str(hitl.get("deze_maand_geweigerd", 0)), className="ci-date")], className="checkin-card", style={"borderLeftColor": "#ef4444"}), width=4),
                dbc.Col(html.Div([html.Div("Wachttijd", className="ci-label"), html.Div(hitl.get("wachttijd_gemiddeld", "-"), className="ci-date")], className="checkin-card", style={"borderLeftColor": "#f59e0b"}), width=4),
            ], style={"marginBottom": "0.8rem"}))

    return html.Div([html.Div([html.H1("Admin"), html.Div(f"Accountbeheer . {cn}", className="subtitle")], className="page-header"),
        *gt_info,
        html.Div([html.I(className="fas fa-database", style={"color": "#5273ff"}), " Alle klanten"], className="section-title"),
        html.Div(html.Table([
            html.Thead(html.Tr([html.Th("Klant"), html.Th("Pakket"), html.Th("Status"), html.Th("Sinds")])),
            html.Tbody([
                html.Tr([html.Td(nm), html.Td(c.get("groei_team",{}).get("pakket","-") if "groei_team" in c else "-"), html.Td(c.get("groei_team",{}).get("status","-") if "groei_team" in c else "-"), html.Td(c.get("groei_team",{}).get("sinds","-") if "groei_team" in c else "-")])
                for nm, c in sorted(clients.items())
            ]),
        ], className="detail-table"), className="admin-card"),
        html.Div([html.A("+ Nieuwe klant", href="/admin/nieuw", className="btn-pill", style={"textDecoration":"none","display":"inline-block"})], style={"marginTop":"0.5rem"})], className="main-content")

def build_linkedin_page(cn, pe):
    d = linkedin_data
    if not d or "metrics" not in d:
        return html.Div([html.Div([html.H1("LinkedIn Outreach"), html.Div("Geen data — start de outreach tool", className="subtitle")], className="page-header"),
            html.Div([html.I(className="fas fa-tools", style={"color": "#f59e0b", "fontSize": "1.5rem"}),
                      html.P("Configureer de LinkedIn Outreach module in de admin console.", style={"color": "#7e8299", "fontSize": "0.82rem"})],
                     style={"textAlign": "center", "padding": "3rem 1rem"})], className="main-content")

    m = d.get("metrics", {})
    prospects = d.get("prospects", [])[:8]
    acties = d.get("recente_acties", [])[:6]
    inst = d.get("instellingen", {})

    metric_icons = {
        "totaal_prospects": ("fa-users", "#5273ff"),
        "connecties_verzonden": ("fa-paper-plane", "#f59e0b"),
        "connecties_geaccepteerd": ("fa-handshake", "#22c55e"),
        "acceptatiegraad": ("fa-percent", "#22c55e"),
        "berichten_verzonden": ("fa-comment-dots", "#8b5cf6"),
        "responsen_ontvangen": ("fa-reply", "#5273ff"),
        "responsgraad": ("fa-chart-line", "#22c55e"),
        "gesprekken_gaande": ("fa-comments", "#f59e0b"),
        "afspraken_ingeboekt": ("fa-calendar-check", "#22c55e"),
    }

    metric_cards = []
    for key, (icon, color) in metric_icons.items():
        val = m.get(key, 0)
        label = key.replace("_", " ").title()
        metric_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {icon}", style={"color": color}), className="lc-icon", style={"background": f"{color}15"}),
            html.Div(label, className="lc-label"),
            html.Div(str(val), className="lc-value"),
        ], className="linkedin-card"), width=3, style={"padding": "0 0.4rem", "marginBottom": "0.5rem"}))

    acc = m.get("acceptatiegraad", 0)
    resp_gr = m.get("responsgraad", 0)
    insight_cards = dbc.Row([
        dbc.Col(html.Div([
            html.Div("Connecties", className="ci-label"),
            html.Div(f"{m.get('connecties_geaccepteerd', 0)}/{m.get('connecties_verzonden', 0)} geaccepteerd", className="ci-date"),
            html.Div(f"{acc}% acceptatiegraad", style={"fontSize": "0.68rem", "color": "#22c55e" if acc >= 70 else "#f59e0b"}),
        ], className="checkin-card", style={"borderLeftColor": "#22c55e"}), width=6, style={"padding": "0 0.4rem"}),
        dbc.Col(html.Div([
            html.Div("Berichten", className="ci-label"),
            html.Div(f"{m.get('responsen_ontvangen', 0)}/{m.get('berichten_verzonden', 0)} respons", className="ci-date"),
            html.Div(f"{resp_gr}% responsgraad", style={"fontSize": "0.68rem", "color": "#22c55e" if resp_gr >= 30 else "#f59e0b"}),
        ], className="checkin-card", style={"borderLeftColor": "#8b5cf6"}), width=6, style={"padding": "0 0.4rem"}),
    ], style={"margin": "0 -0.4rem", "marginBottom": "0.8rem"})

    inst_cards = dbc.Row([
        dbc.Col(html.Div([
            html.Div("Dagelijkse limiet", className="ci-label"), html.Div(str(inst.get("dagelijkse_limiet", 0)), className="ci-date"),
            html.Div(f"{inst.get('connecties_per_dag', 0)} connecties, {inst.get('berichten_per_dag', 0)} berichten", className="ci-note"),
        ], className="checkin-card", style={"borderLeftColor": "#5273ff"}), width=4, style={"padding": "0 0.4rem"}),
        dbc.Col(html.Div([
            html.Div("Status", className="ci-label"), html.Div("Actief" if inst.get("actief") else "Gepauzeerd", className="ci-date"),
            html.Div(f"Laatste run: {inst.get('laatste_run', '-')}", className="ci-note"),
        ], className="checkin-card", style={"borderLeftColor": "#22c55e" if inst.get("actief") else "#f59e0b"}), width=4, style={"padding": "0 0.4rem"}),
        dbc.Col(html.Div([
            html.Div("Gesprekken", className="ci-label"), html.Div(str(m.get("gesprekken_gaande", 0)), className="ci-date"),
            html.Div(f"{m.get('afspraken_ingeboekt', 0)} afspraken ingeboekt", className="ci-note"),
        ], className="checkin-card", style={"borderLeftColor": "#8b5cf6"}), width=4, style={"padding": "0 0.4rem"}),
    ], style={"margin": "0 -0.4rem", "marginBottom": "0.8rem"})

    status_labels = {"connected": "Verbonden", "pending": "In afwachting", "message": "Bericht gestuurd", "meeting": "Afspraak" }
    status_colors = {"connected": "#22c55e", "pending": "#f59e0b", "message": "#5273ff", "meeting": "#8b5cf6"}

    prospect_items = []
    for p in prospects:
        s = p.get("status", "pending")
        c = status_colors.get(s, "#7e8299")
        lbl = status_labels.get(s, s)
        prospect_items.append(html.Div([
            html.Div([
                html.Div(p.get("naam", "")[:2].upper(), className="profile-avatar"),
                html.Div([
                    html.Div(p.get("naam", ""), className="profile-name"),
                    html.Div(f"{p.get('titel', '')} • {p.get('bedrijf', '')}", className="profile-title"),
                ]),
            ], style={"display": "flex", "alignItems": "center", "gap": "0.6rem", "flex": "1"}),
            html.Div([
                html.Div(f"{p.get('berichten', 0)} berichten", style={"fontSize": "0.62rem", "color": "#7e8299"}),
                html.Div(lbl, className="profile-status", style={"color": c}),
            ], style={"textAlign": "right"}),
        ], className="profile-card"))

    actie_items = []
    for a in acties:
        icon_type = "fa-user-plus" if a.get("type") == "connectie" else "fa-comment"
        actie_items.append(html.Tr([
            html.Td(html.I(className=f"fas {icon_type}", style={"color": "#5273ff", "marginRight": "0.3rem"})),
            html.Td(a.get("prospect", "")),
            html.Td(a.get("notitie", "")),
            html.Td(a.get("datum", "")),
        ]))

    return html.Div([html.Div([html.H1("LinkedIn Outreach"), html.Div("Prospect management", className="subtitle")], className="page-header"),
        html.Div([html.I(className="fas fa-chart-bar", style={"color": "#5273ff"}), " Overzicht"], className="section-title"),
        dbc.Row(metric_cards, style={"margin": "0 -0.4rem"}),
        insight_cards,
        inst_cards,
        html.Div([html.I(className="fas fa-address-card", style={"color": "#5273ff"}), " Recente prospects"], className="section-title"),
        html.Div(prospect_items),
        html.Div([html.I(className="fas fa-history", style={"color": "#f59e0b"}), " Recente acties"], className="section-title"),
        html.Div(html.Table([
            html.Thead(html.Tr([html.Th(""), html.Th("Prospect"), html.Th("Actie"), html.Th("Datum")])),
            html.Tbody(actie_items),
        ], className="detail-table"), className="admin-card")], className="main-content")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
