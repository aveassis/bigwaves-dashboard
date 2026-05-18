import json
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from flask import Flask, session, request, redirect

DATA_DIR = Path(__file__).parent / "data"
clients = {}
if DATA_DIR.exists():
    for f in sorted(DATA_DIR.glob("*.json")):
        with open(f) as fh: d = json.load(fh); clients[d["naam"]] = d

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
    .main-content{margin-left:60px;padding:1rem}
}
</style>
<script>
(function(){
  try{
    var t=localStorage.getItem('bw-theme')||'light';
    if(t==='dark')document.body.classList.add('dark');
  }catch(e){}
})();
function toggleTheme(){
  var b=document.body;
  b.classList.toggle('dark');
  try{localStorage.setItem('bw-theme',b.classList.contains('dark')?'dark':'light')}catch(e){}
}
</script>
{%css%}
</head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>"""

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
    "HITL-ratio": ("fa-robot", "rgba(139,92,246,0.08)", "#8b5cf6"),
    "Kostenbesparing": ("fa-euro-sign", "rgba(34,197,94,0.08)", "#22c55e"),
}
KAN_ICON = {"website":"fa-globe","mail":"fa-envelope","whatsapp":"fa-whatsapp","telefoon":"fa-phone"}
PAGE_LABELS = {"dashboard":"Dashboard","conversie":"Conversie","inzichten":"Inzichten","admin":"Admin","linkedin":"LinkedIn Outreach"}
PAGE_ICONS = {"dashboard":"fa-chart-pie","conversie":"fa-chart-line","inzichten":"fa-lightbulb","admin":"fa-cog","linkedin":"fa-linkedin"}
PAGE_ORDERS = ["dashboard","conversie","inzichten","admin","linkedin"]

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
            html.Button([html.I(className="fas fa-moon"), html.Span("Donker thema")], id="theme-btn", className="theme-toggle", n_clicks=0, onClick="toggleTheme()"),
            html.Div("Periode", className="nav-label"),
            html.Div(dcc.Dropdown(id="period-select", options=[{"label": p, "value": p} for p in list(d.get("periodes", {}).keys())], value=pe, clearable=False, className="period-dropdown"), style={"padding": "0 0.8rem 0.6rem"})], className="sidebar-nav"),
        html.Div([html.Div([html.Div(d.get("logo", "🌊"), className="client-avatar"),
            html.Div([html.Div(cn, className="client-name"), html.Div(f"Periode: {pe}", className="client-meta")])], className="client-row"),
            html.A("Uitloggen", href="/uitloggen", className="logout-btn")], className="sidebar-footer")], className="sidebar")

def build_page(cn, pe, active_page="dashboard"):
    d = clients[cn]; ps = d.get("periodes",{})
    if not pe or pe not in ps: pe = list(ps.keys())[0] if ps else None
    if not pe: return "Geen data"
    pd = ps[pe].copy()
    full = {k:v for k,v in d.items() if k!="periodes"}; full.update(pd); full["periode"] = pe
    kpis = full.get("kpis",{}); graf = full.get("grafieken",{}); kan = full.get("kanalen",{})
    bn = full.get("bottleneck",{}); gt = d.get("groei_team",{}); chk = gt.get("checkin_historie",[]) if gt else []
    logo = d.get("logo","🌊")

    kpi_cards = []
    for i,(nm,inf) in enumerate(list(kpis.items())[:4]):
        w,e = inf["waarde"],inf.get("eenheid",""); t = inf.get("trend","")
        ic = KPI_ICONS.get(nm,("fa-chart-bar","rgba(82,115,255,0.08)","#5273ff"))
        kpi_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {ic[0]}",style={"color":ic[2]}),className="kpi-icon",style={"background":ic[1]}),
            html.Div(nm,className="kpi-label"),html.Div(fv(w,e),className="kpi-value"),
            html.Div(f"Doel: {inf['doel']}",className="kpi-target"),
            html.Div(f"{ta(t)} {t}",className=f"kpi-trend {tc(t)}",style={"color":tcol(t)})],className="kpi-card"),
            width=3,style={"padding":"0 0.4rem","marginBottom":"0.5rem"}))

    charts = []
    if graf:
        row = []
        for k,gr in graf.items():
            fig = go.Figure(); fig.add_trace(go.Bar(x=gr["labels"],y=gr["waarden"],marker_color="#5273ff",opacity=0.85))
            if "doel" in gr: fig.add_hline(y=gr["doel"],line_dash="dash",line_color="#f59e0b",annotation_text=f"Doel: {gr['doel']}",annotation_position="top left")
            fig.update_layout(title=dict(text=gr["titel"],font=dict(size=12,color="#1a1a2e"),x=0.02),height=240,margin=dict(l=16,r=16,t=32,b=16),paper_bgcolor="#fff",plot_bgcolor="#fff",font=dict(size=10,color="#7e8299"),yaxis=dict(gridcolor="#f1efed"),xaxis=dict(gridcolor="#f1efed"),hoverlabel=dict(bgcolor="#5273ff",font_color="white"),showlegend=False)
            row.append(dbc.Col(html.Div(dcc.Graph(figure=fig,config={"displayModeBar":False}),className="chart-box"),width=6,style={"padding":"0 0.4rem","marginBottom":"0.5rem"}))
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

    main = html.Div([html.Div([html.Div([html.H1("Dashboard"),html.Div(f"Performance overzicht • {pe}",className="subtitle")]),html.Div([html.A("📄 PDF", href="/export/pdf", className="btn-pill", style={"marginRight":"0.3rem","textDecoration":"none"}),html.A("📊 CSV", href="/export/csv", className="btn-pill", style={"textDecoration":"none"})])],className="page-header"),
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

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="dash-content"),
])

@app.callback(Output("dash-content", "children"), Input("url", "pathname"))
def router(pathname):
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

    if active == "dashboard":
        main = build_page(c, pe, active)
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

    kpi_cards = []
    for nm, inf in list(kpis.items())[:6]:
        w, e = inf["waarde"], inf.get("eenheid", "")
        t = inf.get("trend", "")
        ic = KPI_ICONS.get(nm, ("fa-chart-bar", "rgba(82,115,255,0.08)", "#5273ff"))
        kpi_cards.append(dbc.Col(html.Div([
            html.Div(html.I(className=f"fas {ic[0]}", style={"color": ic[2]}), className="kpi-icon", style={"background": ic[1]}),
            html.Div(nm, className="kpi-label"),
            html.Div(fmt_val(w, e), className="kpi-value"),
            html.Div(f"Doel: {inf['doel']}", className="kpi-target"),
            html.Div(f"{trend_arrow(t)} {t}", className=f"kpi-trend {trend_class(t)}", style={"color": trend_col(t)}),
        ], className="kpi-card"), width=4, style={"padding": "0 0.4rem", "marginBottom": "0.5rem"}))

    hitl_section = []
    if hitl:
        totaal = hitl.get("totaal_acties", 0)
        mens = hitl.get("menselijke_check", 0)
        auto = hitl.get("geautomatiseerd", 0)
        saved = hitl.get("bespaarde_uren", 0)
        cat = hitl.get("categorieen", {})

        hitl_cards = dbc.Row([
            dbc.Col(html.Div([html.Div("Totaal acties", className="ci-label"), html.Div(str(totaal), className="ci-date")], className="checkin-card", style={"borderLeftColor": "#5273ff"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Menselijke check", className="ci-label"), html.Div(str(mens), className="ci-date"), html.Div(f"{round(mens/totaal*100) if totaal else 0}%", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#f59e0b"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Geautomatiseerd", className="ci-label"), html.Div(str(auto), className="ci-date"), html.Div(f"{round(auto/totaal*100) if totaal else 0}%", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#22c55e"}), width=3, style={"padding": "0 0.3rem"}),
            dbc.Col(html.Div([html.Div("Bespaarde uren", className="ci-label"), html.Div(f"{saved}h", className="ci-date"), html.Div("deze periode", className="ci-note")], className="checkin-card", style={"borderLeftColor": "#8b5cf6"}), width=3, style={"padding": "0 0.3rem"}),
        ], style={"margin": "0 -0.3rem", "marginBottom": "0.8rem"})

        cat_rows = []
        for cn_, cd in cat.items():
            cat_rows.append(html.Tr([html.Td(cn_), html.Td(str(cd.get("totaal", 0))), html.Td(str(cd.get("hitl", 0))), html.Td(f"{cd.get('percentage', 0)}%")]))

        cat_table = html.Table([
            html.Thead(html.Tr([html.Th("Categorie"), html.Th("Totaal"), html.Th("HITL"), html.Th("%")])),
            html.Tbody(cat_rows),
        ], className="detail-table")

        hitl_section = [
            html.Div([html.I(className="fas fa-robot", style={"color": "#8b5cf6"}), " HITL-overzicht"], className="section-title"),
            hitl_cards,
            html.Div(cat_table, className="admin-card"),
        ]

    return html.Div([html.Div([html.H1("Conversie"), html.Div(f"KPI-overzicht . {pe}", className="subtitle")], className="page-header"),
        dbc.Row(kpi_cards, style={"margin": "0 -0.4rem"}),
        *hitl_section], className="main-content")

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
        *gt_info], className="main-content")

def build_linkedin_page(cn, pe):
    return html.Div([html.Div([html.H1("LinkedIn Outreach"), html.Div("Volgt binnenkort", className="subtitle")], className="page-header"),
        html.Div([html.I(className="fas fa-tools", style={"color": "#f59e0b", "fontSize": "1.5rem"}),
                  html.H3("Nog in ontwikkeling", style={"margin": "0.5rem 0", "color": "#1a1a2e"}),
                  html.P("De LinkedIn Outreach module wordt binnenkort toegevoegd.", style={"color": "#7e8299", "fontSize": "0.82rem"})],
                 style={"textAlign": "center", "padding": "3rem 1rem"})], className="main-content")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
