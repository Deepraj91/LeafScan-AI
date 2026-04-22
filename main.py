import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title="LeafScan AI – Detect Plant Diseases Instantly",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "🌿 AI-Powered Leaf Health Platform"}
)

# ── Hide Streamlit chrome + global styles (CSS only — no scripts here) ────────
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stAppViewContainer { padding: 0 !important; }
[data-testid="stDecoration"], .stToolbar, .stDeployButton { display: none !important; }

/* ── Root background = cream + grid ── */
.stApp {
  background-color: #faf7f0 !important;
  background-image:
    linear-gradient(rgba(74,103,65,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(74,103,65,0.04) 1px, transparent 1px) !important;
  background-size: 60px 60px !important;
}
.main,
section[data-testid="stMain"],
section[data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlock"],
div[data-testid="column"],
div[data-testid="stHorizontalBlock"] {
  background: transparent !important;
}

/* ── SPACER so content sits below the fixed nav iframe ── */
#nav-spacer-outer { height: 68px; display: block; }


</style>

<!-- Nav height spacer -->
<div id="nav-spacer-outer"></div>

<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
""", unsafe_allow_html=True)

# ── STICKY NAV as its own iframe so JS actually executes ──────────────────────
# Streamlit strips <script> from st.markdown; components.html runs in an iframe
# We make this iframe position:fixed via CSS injection into the parent from within.
NAV_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400&display=swap" rel="stylesheet"/>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 68px; overflow: hidden; background: transparent; }
nav {
  width: 100%; height: 68px;
  background: rgba(250,247,240,0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(74,103,65,0.12);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 56px;
  box-shadow: 0 2px 20px rgba(26,18,8,0.06);
}
.logo { display:flex;align-items:center;gap:10px;font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#3d4f2a;cursor:pointer; }
.logo-mark { width:38px;height:38px;background:linear-gradient(135deg,#4a6741,#3d4f2a);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem; }
ul { display:flex;gap:36px;list-style:none; }
ul a { font-size:.82rem;font-weight:500;color:#4a6741;text-decoration:none;letter-spacing:.07em;text-transform:uppercase;cursor:pointer;transition:color .2s; }
ul a:hover { color:#1a1208; }
.cta { background:#1a1208;color:#faf7f0;border:none;padding:10px 24px;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:.85rem;font-weight:600;cursor:pointer;transition:background .2s,transform .15s; }
.cta:hover { background:#3d4f2a;transform:translateY(-1px); }
/* GitHub button — explicit green, no inheritance issues */
.gh {
  width:36px;height:36px;
  background:rgba(212,232,204,0.5);
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  text-decoration:none;
  transition:background .2s;
  color: #4a6741;          /* explicit green */
  fill:  #4a6741;          /* explicit green */
}
.gh:hover { background:#a8c49a; }
.gh svg { display:block; }
.gh svg path { fill: #4a6741 !important; }   /* hard-lock green */
.right { display:flex;align-items:center;gap:12px; }
@media(max-width:900px){ nav{padding:0 20px;} ul{display:none;} }
</style>
</head>
<body>
<nav>
  <div class="logo" onclick="goHome()"><div class="logo-mark">🌿</div>LeafScan</div>

  <div class="right">
  
    <a href="https://github.com/Deepraj91/LeafScan-AI" target="_blank" class="gh" title="GitHub">
      <!-- GitHub Invertocat — fill hardcoded to green -->
      <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path fill="#4a6741" d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58
          0-.29-.01-1.04-.02-2.04-3.34.73-4.04-1.61-4.04-1.61-.55-1.38-1.34-1.75-1.34-1.75
          -1.09-.74.08-.73.08-.73 1.2.08 1.83 1.23 1.83 1.23 1.07 1.83 2.8 1.3 3.49.99
          .11-.78.42-1.3.76-1.6-2.66-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.23-3.22
          -.12-.3-.53-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4
          c1.02 0 2.05.14 3 .4 2.28-1.55 3.29-1.23 3.29-1.23.65 1.66.24 2.88.12 3.18
          .77.84 1.23 1.91 1.23 3.22 0 4.61-2.81 5.62-5.49 5.92.43.37.81 1.1.81 2.22
          0 1.6-.01 2.89-.01 3.28 0 .32.21.69.82.57C20.56 21.8 24 17.3 24 12
          24 5.37 18.63 0 12 0z"/>
      </svg>
    </a>
  </div>
</nav>

<script>
// ── Make this iframe itself position:fixed at top of the parent page ──────────
(function fixNav() {
  try {
    const frame = window.frameElement;
    if (!frame) return;
    frame.style.cssText = [
      'position:fixed !important',
      'top:0 !important',
      'left:0 !important',
      'right:0 !important',
      'width:100% !important',
      'height:68px !important',
      'z-index:99999 !important',
      'border:none !important',
      'background:transparent !important',
      'display:block !important',
    ].join(';');
  } catch(e) {}
})();

// ── Resolve parent-page scroll targets ───────────────────────────────────────
function getParentWin() {
  try { return window.parent !== window ? window.parent : window; }
  catch(e) { return window; }
}

// Returns the absolute scrollY in the parent page for a given element there
function parentScrollY(el) {
  const rect = el.getBoundingClientRect();
  return rect.top + getParentWin().scrollY;
}

function goHome() {
  try { getParentWin().scrollTo({ top: 0, behavior: 'smooth' }); }
  catch(e) {}
}

function goHow() {
  try {
    const p = getParentWin();
    // Strategy 1: use cached offset (set by content iframe on load)
    if (p._leafscanHowOffset != null) {
      p.scrollTo({ top: p._leafscanHowOffset - 80, behavior: 'smooth' });
      return;
    }
    // Strategy 2: ask content iframe to report offset NOW, then scroll
    // Find the content iframe (the one that's NOT the nav iframe)
    const iframes = p.document.querySelectorAll('iframe');
    let contentFrame = null;
    iframes.forEach(function(f) { if (f !== window.frameElement) contentFrame = f; });
    if (contentFrame) {
      // Post a request to the content iframe asking it to report its how-section offset
      contentFrame.contentWindow.postMessage({ type: 'leafscan:requestHowOffset' }, '*');
      // Wait briefly for the reply, then scroll
      setTimeout(function() {
        if (p._leafscanHowOffset != null) {
          p.scrollTo({ top: p._leafscanHowOffset - 80, behavior: 'smooth' });
        } else {
          // Strategy 3: geometry fallback — iframe is 1480px, how-section starts ~68% down
          const iTop = contentFrame.getBoundingClientRect().top + p.scrollY;
          p.scrollTo({ top: iTop + contentFrame.offsetHeight * 0.68 - 80, behavior: 'smooth' });
        }
      }, 120);
    }
  } catch(e) {}
}

function goUpload() {
  try {
    const p = getParentWin();
    const anchor = p.document.getElementById('upload-anchor');
    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  } catch(e) {}
}

// ── Receive messages from content iframe ─────────────────────────────────────
function handleMsg(e) {
  if (!e.data || !e.data.type) return;
  if (e.data.type === 'leafscan:howOffset') {
    try { getParentWin()._leafscanHowOffset = e.data.offset; } catch(ex) {}
  }
  if (e.data.type === 'leafscan:scrollToUpload') {
    goUpload();
  }
}
window.addEventListener('message', handleMsg);
try { getParentWin().addEventListener('message', handleMsg); } catch(ex) {}

</script>
</body>
</html>
"""

# height=68 exactly matches the nav; the iframe JS re-positions it as fixed
components.html(NAV_HTML, height=68, scrolling=False)

# ── Session State ─────────────────────────────────────────────────────────────
if "analysis_result"      not in st.session_state: st.session_state.analysis_result      = None
if "analysed_image_bytes" not in st.session_state: st.session_state.analysed_image_bytes = None
if "analysed_image_type"  not in st.session_state: st.session_state.analysed_image_type  = None
if "upload_key"           not in st.session_state: st.session_state.upload_key            = 0

# ═══════════════════════════════════════════════════════════════════════════════
#  TOP SECTION — Hero + Stats + How It Works  (nav REMOVED from here)
# =============================================================================
TOP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --soil:  #1a1208; --bark:  #2d1f0e; --moss:  #3d4f2a;
  --fern:  #4a6741; --sage:  #7a9b6f; --mint:  #a8c49a;
  --dew:   #d4e8cc; --paper: #f5f0e8; --cream: #faf7f0;
  --gold:  #c8a84b; --amber: #e8c56a;
}
html, body { height: auto; overflow: hidden; }
body {
  font-family: 'DM Sans', sans-serif;
  color: var(--soil);
  overflow-x: hidden;
  background-color: var(--cream);
  background-image:
    linear-gradient(rgba(74,103,65,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(74,103,65,0.04) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* ── shared blob helper ── */
.blob { position:absolute;border-radius:50%;pointer-events:none; }

/* ── HERO ── */
.hero { background:transparent;padding:60px 56px 70px;display:flex;align-items:center;position:relative;overflow:hidden; }
.hero .blob-1 { width:640px;height:640px;background:radial-gradient(circle,rgba(74,103,65,0.10) 0%,transparent 68%);top:-120px;right:-100px; }
.hero .blob-2 { width:420px;height:420px;background:radial-gradient(circle,rgba(168,196,154,0.08) 0%,transparent 68%);bottom:-80px;left:3%; }
.hero .blob-3 { width:300px;height:300px;background:radial-gradient(circle,rgba(200,168,75,0.06) 0%,transparent 68%);top:30%;left:40%; }
.hero-inner  { display:grid;grid-template-columns:1fr 1fr;gap:80px;max-width:1200px;margin:0 auto;width:100%;align-items:center;position:relative;z-index:1; }
.hero-eyebrow{ display:inline-flex;align-items:center;gap:8px;font-family:'DM Mono',monospace;font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--sage);margin-bottom:22px;animation:fadeUp .6s ease both; }
.eyebrow-dot { width:7px;height:7px;border-radius:50%;background:var(--gold);animation:pulse 2.2s ease-in-out infinite; }
.hero-title  { font-family:'Playfair Display',serif;font-size:clamp(2.8rem,4.5vw,4.5rem);font-weight:900;line-height:1.05;color:var(--soil);margin-bottom:24px;animation:fadeUp .6s .07s ease both; }
.hero-title em { font-style:italic;color:var(--fern); }
.hero-title .gradient-text { display:block;background:linear-gradient(120deg,var(--moss) 0%,var(--sage) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.hero-desc   { font-size:1rem;color:var(--sage);line-height:1.85;max-width:440px;margin-bottom:36px;animation:fadeUp .6s .14s ease both; }
.hero-btns   { display:flex;gap:14px;animation:fadeUp .6s .21s ease both; }
.btn-primary { background:var(--soil);color:var(--cream);border:none;padding:14px 30px;border-radius:10px;font-family:'DM Sans',sans-serif;font-size:0.95rem;font-weight:600;cursor:pointer;transition:all .2s;box-shadow:0 6px 20px rgba(26,18,8,0.2); }
.btn-primary:hover { background:var(--moss);transform:translateY(-2px); }
.btn-ghost   { background:transparent;color:var(--fern);border:1.5px solid rgba(74,103,65,0.4);padding:13px 26px;border-radius:10px;font-family:'DM Sans',sans-serif;font-size:0.95rem;font-weight:500;cursor:pointer;transition:all .2s; }
.btn-ghost:hover { border-color:var(--fern);background:rgba(74,103,65,0.06); }

/* ── ORB ── */
.hero-right  { display:flex;align-items:center;justify-content:center;animation:fadeUp .6s .28s ease both; }
.orb-wrap    { position:relative;width:380px;height:380px; }
.orb-outer   { position:absolute;inset:0;border-radius:50%;border:1px solid rgba(74,103,65,0.16);background:radial-gradient(circle at 35% 35%,rgba(168,196,154,0.18),rgba(74,103,65,0.06));animation:breathe 5s ease-in-out infinite; }
.orb-mid     { position:absolute;inset:36px;border-radius:50%;border:1px dashed rgba(74,103,65,0.2);animation:spin-slow 22s linear infinite; }
.orb-inner   { position:absolute;inset:72px;border-radius:50%;background:linear-gradient(145deg,var(--paper),var(--dew));box-shadow:0 24px 64px rgba(26,18,8,0.12),inset 0 2px 20px rgba(74,103,65,0.1);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:10px; }
.orb-leaf    { font-size:4rem;filter:drop-shadow(0 10px 24px rgba(74,103,65,0.35)); }
.orb-label   { font-family:'DM Mono',monospace;font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--sage); }
.orbit-dot   { position:absolute;width:10px;height:10px;border-radius:50%;background:var(--gold);top:50%;left:0;transform-origin:190px 0;animation:orbit 8s linear infinite; }
.orbit-dot:nth-child(2){ background:var(--mint);animation-delay:-4s; }
.orbit-dot:nth-child(3){ background:var(--sage);width:7px;height:7px;animation-delay:-2s;animation-duration:12s; }
.rotate-ring { position:absolute;inset:0;display:flex;align-items:center;justify-content:center; }

/* ── STATS ── */
.stats-wrap { background:transparent;padding:0 56px 0;position:relative;overflow:hidden; }
.stats-wrap .blob-1 { width:500px;height:500px;background:radial-gradient(circle,rgba(74,103,65,0.07) 0%,transparent 68%);top:-180px;left:-80px; }
.stats-wrap .blob-2 { width:380px;height:380px;background:radial-gradient(circle,rgba(200,168,75,0.06) 0%,transparent 68%);top:-100px;right:-60px; }
.stats-band { background:var(--soil);border-radius:24px;padding:44px 56px;display:flex;justify-content:center;align-items:center;max-width:1100px;margin:0 auto;position:relative;z-index:1;box-shadow:0 20px 60px rgba(26,18,8,0.18);background-image:linear-gradient(rgba(168,196,154,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(168,196,154,0.04) 1px,transparent 1px);background-size:60px 60px;background-color:var(--soil); }
.stat-item   { flex:1;max-width:220px;text-align:center;padding:0 40px;position:relative; }
.stat-item:not(:last-child)::after { content:'';position:absolute;right:0;top:50%;transform:translateY(-50%);width:1px;height:44px;background:rgba(168,196,154,0.18); }
.stat-num    { font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:var(--amber);line-height:1; }
.stat-label  { font-family:'DM Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(212,232,204,0.6);margin-top:7px; }

/* ── HOW IT WORKS ── */
.how { background:transparent;padding:90px 56px;position:relative;overflow:hidden; }
.how .blob-1 { width:560px;height:560px;background:radial-gradient(circle,rgba(200,168,75,0.07) 0%,transparent 65%);top:-140px;right:-140px; }
.how .blob-2 { width:400px;height:400px;background:radial-gradient(circle,rgba(74,103,65,0.07) 0%,transparent 65%);bottom:-100px;left:-80px; }
.how .blob-3 { width:280px;height:280px;background:radial-gradient(circle,rgba(168,196,154,0.06) 0%,transparent 65%);top:40%;left:45%; }
.section-label { font-family:'DM Mono',monospace;font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--sage);margin-bottom:14px;display:flex;align-items:center;gap:14px; }
.section-label::before { content:'';display:block;width:32px;height:1px;background:var(--sage); }
.section-title { font-family:'Playfair Display',serif;font-size:clamp(1.9rem,3.2vw,2.8rem);font-weight:900;color:var(--soil);line-height:1.18;margin-bottom:56px; }
.steps-row { display:grid;grid-template-columns:repeat(4,1fr);gap:2px;max-width:1100px;margin:0 auto; }
.step-card { background:rgba(245,240,232,0.85);backdrop-filter:blur(4px);border:1px solid rgba(74,103,65,0.07);padding:36px 26px;transition:transform .25s,box-shadow .25s,background .25s,border-color .25s;position:relative; }
.step-card:first-child { border-radius:16px 0 0 16px; }
.step-card:last-child  { border-radius:0 16px 16px 0; }
.step-card:hover { background:var(--soil);border-color:transparent;transform:translateY(-8px);box-shadow:0 20px 48px rgba(26,18,8,0.18);z-index:2;border-radius:16px; }
.step-card:hover .step-num   { color:var(--amber); }
.step-card:hover .step-title { color:var(--cream); }
.step-card:hover .step-desc  { color:rgba(212,232,204,0.7); }
.step-card:hover .step-icon-wrap { background:rgba(168,196,154,0.15); }
.step-num   { font-family:'DM Mono',monospace;font-size:0.72rem;letter-spacing:0.12em;color:var(--sage);margin-bottom:20px;transition:color .25s; }
.step-icon-wrap { width:54px;height:54px;background:var(--dew);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:18px;transition:background .25s; }
.step-title { font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:var(--soil);margin-bottom:9px;transition:color .25s; }
.step-desc  { font-size:0.87rem;color:var(--sage);line-height:1.7;transition:color .25s; }

/* ── FLOATING LEAVES ── */
.leaf-float { position:absolute;pointer-events:none;opacity:.07; }
.leaf-float svg { animation:float-anim var(--dur,7s) ease-in-out infinite;animation-delay:var(--delay,0s); }

/* ── ANIMATIONS ── */
@keyframes fadeUp    { from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)} }
@keyframes pulse     { 0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.8)} }
@keyframes breathe   { 0%,100%{transform:scale(1)}50%{transform:scale(1.03)} }
@keyframes spin-slow { from{transform:rotate(0deg)}to{transform:rotate(360deg)} }
@keyframes orbit     { from{transform:rotate(0deg) translateX(155px)}to{transform:rotate(360deg) translateX(155px)} }
@keyframes float-anim{ 0%,100%{transform:translateY(0) rotate(0deg)}33%{transform:translateY(-22px) rotate(6deg)}66%{transform:translateY(12px) rotate(-4deg)} }

@media (max-width:900px) {
  .hero { padding:50px 24px 50px; } .hero-inner { grid-template-columns:1fr; }
  .hero-right { display:none; }
  .stats-wrap { padding:0 20px; } .stats-band { flex-wrap:wrap;padding:28px 24px;border-radius:16px; }
  .stat-item::after { display:none; }
  .how { padding:70px 24px; } .steps-row { grid-template-columns:1fr 1fr; }
}
</style>
</head>
<body>
<!-- ═══ HERO ═══ -->
<section id="home-section" class="hero">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
  <div class="leaf-float" style="top:10%;left:3%;width:72px;--dur:7s;--delay:0s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1.2"/></svg></div>
  <div class="leaf-float" style="top:58%;left:1.5%;width:46px;--dur:9s;--delay:2s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div class="leaf-float" style="top:20%;right:3.5%;width:62px;--dur:8s;--delay:1.4s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div class="leaf-float" style="top:75%;right:8%;width:38px;--dur:11s;--delay:3s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>

  <div class="hero-inner">
    <div class="hero-left">
      <div class="hero-eyebrow"><span class="eyebrow-dot"></span>Plant Pathology AI · Est. 2024</div>
      <h1 class="hero-title">Diagnose<br><em>any leaf</em><span class="gradient-text">disease.</span></h1>
      <p class="hero-desc">Upload a photograph of your plant's leaf and receive an instant, expert-grade diagnosis — powered by computer vision trained on thousands of plant specimens.</p>
      <div class="hero-btns">
        <button class="btn-primary" onclick="goUpload()">Upload a Leaf Image →</button>
        <button class="btn-ghost"   onclick="goHow()">How It Works</button>
      </div>
    </div>
    <div class="hero-right">
      <div class="orb-wrap">
        <div class="orb-outer"></div>
        <div class="orb-mid"><div class="orbit-dot"></div><div class="orbit-dot"></div><div class="orbit-dot"></div></div>
        <div class="orb-inner"><div class="orb-leaf">🌱</div><div class="orb-label">Scan · Detect · Heal</div></div>
        <div class="rotate-ring">
          <svg viewBox="0 0 300 300" width="300" height="300" style="animation:spin-slow 22s linear infinite;position:absolute;">
            <defs><path id="circ" d="M 150,150 m -120,0 a 120,120 0 1,1 240,0 a 120,120 0 1,1 -240,0"/></defs>
            <text fill="#7a9b6f" font-size="11" font-family="'DM Mono',monospace" letter-spacing="3"><textPath href="#circ">AI POWERED · INSTANT DIAGNOSIS · PLANT HEALTH · LEAF SCAN ·</textPath></text>
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ═══ STATS ═══ -->
<div class="stats-wrap">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="leaf-float" style="bottom:10%;right:2%;width:52px;--dur:10s;--delay:1s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div class="leaf-float" style="top:5%;left:5%;width:40px;--dur:8s;--delay:0.5s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div style="padding:56px 0;">
    <div class="stats-band">
      <div class="stat-item"><div class="stat-num">156+</div><div class="stat-label">Diagnoses Made</div></div>
      <div class="stat-item"><div class="stat-num">89%</div><div class="stat-label">Accuracy Rate</div></div>
      <div class="stat-item"><div class="stat-num">100+</div><div class="stat-label">Active Users</div></div>
      <div class="stat-item"><div class="stat-num">38+</div><div class="stat-label">Plant Species</div></div>
    </div>
  </div>
</div>

<!-- ═══ HOW IT WORKS ═══ -->
<section class="how" id="how-section">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
  <div class="leaf-float" style="top:8%;left:2%;width:58px;--dur:9s;--delay:0.3s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1.2"/></svg></div>
  <div class="leaf-float" style="bottom:12%;left:4%;width:44px;--dur:7.5s;--delay:2.5s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div class="leaf-float" style="top:15%;right:2%;width:66px;--dur:8.5s;--delay:1.8s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>
  <div class="leaf-float" style="bottom:8%;right:5%;width:36px;--dur:12s;--delay:4s;"><svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg></div>

  <div style="max-width:1100px;margin:0 auto;position:relative;z-index:1;">
    <div class="section-label">Process</div>
    <div class="section-title">From photo to<br>diagnosis <em style="font-style:italic;color:#7a9b6f;">in seconds</em></div>
    <div class="steps-row">
      <div class="step-card"><div class="step-num">01</div><div class="step-icon-wrap">📸</div><div class="step-title">Capture</div><p class="step-desc">Photograph the affected leaf in natural light for best results</p></div>
      <div class="step-card"><div class="step-num">02</div><div class="step-icon-wrap">⬆️</div><div class="step-title">Upload</div><p class="step-desc">Drag and drop or browse to select your image below</p></div>
      <div class="step-card"><div class="step-num">03</div><div class="step-icon-wrap">🧬</div><div class="step-title">Analyse</div><p class="step-desc">AI scans for pathogens, fungi, and nutrient deficiencies</p></div>
      <div class="step-card"><div class="step-num">04</div><div class="step-icon-wrap">📋</div><div class="step-title">Report</div><p class="step-desc">Receive full diagnosis with actionable treatment steps</p></div>
    </div>
  </div>
</section>

<script>
/* ─── Navigation helpers (scroll the PARENT Streamlit page) ─── */
function getIframeOffsetInParent() {
  try {
    const frame = window.frameElement;
    if (!frame) return 0;
    const rect = frame.getBoundingClientRect();
    return rect.top + window.parent.scrollY;
  } catch(e) { return 0; }
}

function goHow() {
  try {
    const el = document.getElementById('how-section');
    const elTop = el.getBoundingClientRect().top;   // relative to iframe viewport
    const iframeOffset = getIframeOffsetInParent();
    window.parent.scrollTo({
      top: iframeOffset + elTop - 80,  // -80 to account for sticky nav height
      behavior: 'smooth'
    });
  } catch(e) {
    window.parent.scrollTo({ top: 900, behavior: 'smooth' });
  }
}

function goUpload() {
  try {
    // Tell the parent to scroll to the upload-anchor element in the Streamlit DOM
    window.parent.postMessage({ type: 'leafscan:scrollToUpload' }, '*');
  } catch(e) {}
}

/* ─── Report how-section absolute offset to parent on load ─── */
function reportHowOffset() {
  try {
    const el = document.getElementById('how-section');
    const elTop = el.getBoundingClientRect().top;
    const iframeOffset = getIframeOffsetInParent();
    window.parent.postMessage({
      type: 'leafscan:howOffset',
      offset: iframeOffset + elTop
    }, '*');
  } catch(e) {}
}

/* ─── Auto-resize iframe ─── */
function reportHeight() {
  const h = document.documentElement.scrollHeight || document.body.scrollHeight;
  window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: h }, '*');
}

/* ─── Listen for on-demand offset requests from nav iframe ─── */
window.addEventListener('message', function(e) {
  if (e.data && e.data.type === 'leafscan:requestHowOffset') {
    reportHowOffset();
  }
});

window.addEventListener('load', () => { reportHeight(); reportHowOffset(); });
window.addEventListener('resize', reportHeight);
setTimeout(() => { reportHeight(); reportHowOffset(); }, 400);
// Extra report after fonts/images settle
setTimeout(() => { reportHowOffset(); }, 1200);
</script>
</body>
</html>
"""

components.html(TOP_HTML, height=1480, scrolling=False)

# ─── Upload anchor ────────────────────────────────────────────────────────────
st.markdown('<div id="upload-anchor" style="height:1px;margin:0;padding:0;scroll-margin-top:80px;"></div>', unsafe_allow_html=True)

# ─── Shared CSS for file uploader + buttons ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400&display=swap');

[data-testid="stFileUploaderDropzone"] {
  background: rgba(250,247,240,0.7) !important;
  backdrop-filter: blur(6px) !important;
  border: 2px dashed rgba(74,103,65,0.4) !important;
  border-radius: 18px !important;
  padding: 48px 36px !important;
  transition: border-color .25s, background .25s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #4a6741 !important;
  background: rgba(212,232,204,0.25) !important;
}
[data-testid="stFileUploaderDropzone"] svg { color:#4a6741 !important;width:32px !important;height:32px !important; }
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span { color:#2d1f0e !important;font-size:.97rem !important;font-weight:500 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzoneInstructions"] em   { color:#7a9b6f !important;font-size:.82rem !important; }
[data-testid="stFileUploaderDropzone"] button[kind="secondary"] {
  background:transparent !important;border:1.5px solid #4a6741 !important;
  color:#4a6741 !important;border-radius:8px !important;font-weight:600 !important;
}
[data-testid="stFileUploaderDropzone"] button[kind="secondary"]:hover {
  background:#4a6741 !important;color:#faf7f0 !important;
}
.stButton>button {
  background:#1a1208 !important;color:#faf7f0 !important;
  border:none !important;border-radius:10px !important;
  padding:14px 26px !important;font-family:'DM Sans',sans-serif !important;
  font-weight:600 !important;font-size:.95rem !important;
  width:100% !important;cursor:pointer !important;
  transition:all .2s !important;
  box-shadow:0 6px 20px rgba(26,18,8,0.2) !important;
  margin-top:12px !important;
}
.stButton>button:hover { background:#3d4f2a !important;transform:translateY(-2px) !important; }
.stImage img { border-radius:14px !important;box-shadow:0 8px 32px rgba(26,18,8,0.12) !important; }
div[data-testid="stAlert"] {
  background:rgba(212,232,204,0.3) !important;
  border:1px solid rgba(74,103,65,0.25) !important;
  border-radius:10px !important;
  backdrop-filter:blur(6px) !important;
}
div[data-testid="stAlert"] p { color:#3d4f2a !important; }
</style>
""", unsafe_allow_html=True)

# ─── Upload Section Heading ────────────────────────────────────────────────────
st.markdown("""
<div style="position:relative;overflow:hidden;padding:72px 56px 32px;text-align:center;">
  <div style="position:absolute;width:500px;height:500px;border-radius:50%;
    background:radial-gradient(circle,rgba(74,103,65,0.08) 0%,transparent 68%);
    top:-180px;right:-80px;pointer-events:none;"></div>
  <div style="position:absolute;width:360px;height:360px;border-radius:50%;
    background:radial-gradient(circle,rgba(200,168,75,0.06) 0%,transparent 68%);
    bottom:-120px;left:-60px;pointer-events:none;"></div>
  <div style="position:absolute;top:12%;left:2%;width:54px;opacity:.07;pointer-events:none;animation:leafFloat 8s ease-in-out infinite;">
    <svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#3d4f2a"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1.2"/></svg>
  </div>
  <div style="position:absolute;bottom:10%;right:3%;width:40px;opacity:.07;pointer-events:none;animation:leafFloat 10s ease-in-out 2s infinite;">
    <svg viewBox="0 0 70 90" fill="none"><path d="M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z" fill="#4a6741"/><path d="M35 85V12" stroke="#7a9b6f" stroke-width="1"/></svg>
  </div>
  <style>
    @keyframes leafFloat {
      0%,100%{transform:translateY(0) rotate(0deg)}
      33%{transform:translateY(-18px) rotate(5deg)}
      66%{transform:translateY(10px) rotate(-3deg)}
    }
  </style>
  <div style="position:relative;z-index:1;">
    <div style="font-family:'DM Mono',monospace;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
                color:#7a9b6f;margin-bottom:14px;display:flex;align-items:center;justify-content:center;gap:14px;">
      <span style="display:block;width:32px;height:1px;background:#7a9b6f;"></span>Diagnosis
      <span style="display:block;width:32px;height:1px;background:#7a9b6f;"></span>
    </div>
    <div style="font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;
                color:#1a1208;line-height:1.15;margin-bottom:14px;">Upload your leaf image</div>
    <p style="font-size:1rem;color:#7a9b6f;line-height:1.8;max-width:480px;margin:0 auto 20px;">
      Our AI analyses texture, colour patterns and lesion morphology to identify
      38+ plant diseases with high accuracy.
    </p>
    <div style="display:flex;justify-content:center;gap:28px;flex-wrap:wrap;">
      <span style="display:flex;align-items:center;gap:7px;font-family:'DM Mono',monospace;font-size:.8rem;color:#4a6741;">
        <span style="width:6px;height:6px;border-radius:50%;background:#c8a84b;display:inline-block;"></span>JPG · JPEG · PNG
      </span>
      <span style="display:flex;align-items:center;gap:7px;font-family:'DM Mono',monospace;font-size:.8rem;color:#4a6741;">
        <span style="width:6px;height:6px;border-radius:50%;background:#c8a84b;display:inline-block;"></span>Natural daylight works best
      </span>
      <span style="display:flex;align-items:center;gap:7px;font-family:'DM Mono',monospace;font-size:.8rem;color:#4a6741;">
        <span style="width:6px;height:6px;border-radius:50%;background:#c8a84b;display:inline-block;"></span>Single leaf in frame
      </span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  UPLOAD ↔ RESULTS  state machine
# =============================================================================
col_l, col_c, col_r = st.columns([1, 2, 1])

with col_c:

    if st.session_state.analysis_result is None:
        uploaded_file = st.file_uploader(
            "upload",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key=f"uploader_{st.session_state.upload_key}",
        )

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Leaf Preview", use_column_width=True)
            st.success("✅  Image ready — click below to analyse")

            if st.button("🔬  Analyse Leaf", use_container_width=True):
                image_bytes = uploaded_file.getvalue()
                with st.spinner("Scanning your leaf…"):
                    try:
                        api_url  = "http://leaf-diseases-detect.vercel.app"
                        files    = {"file": (uploaded_file.name, image_bytes, uploaded_file.type)}
                        response = requests.post(f"{api_url}/disease-detection-file", files=files, timeout=30)
                        if response.status_code == 200:
                            st.session_state.analysis_result      = response.json()
                            st.session_state.analysed_image_bytes = image_bytes
                            st.session_state.analysed_image_type  = uploaded_file.type
                            st.rerun()
                        else:
                            st.error(f"❌ API Error {response.status_code}: {response.text}")
                    except requests.exceptions.Timeout:
                        st.error("❌ Request Timeout — the server took too long to respond.")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Connection Error — unable to reach the API server.")
                    except Exception as e:
                        st.error(f"❌ Unexpected Error: {e}")

    else:
        result = st.session_state.analysis_result

        if st.session_state.analysed_image_bytes:
            st.image(BytesIO(st.session_state.analysed_image_bytes),
                     caption="Analysed Leaf", use_column_width=True)

        disease_name = result.get("disease_name", result.get("disease", result.get("prediction", "Unknown")))
        disease_type = result.get("disease_type", "detected" if result.get("disease_detected") else "healthy")
        confidence   = result.get("confidence", "N/A")
        severity     = result.get("severity",   "N/A")

        if result.get("disease_detected") and disease_type != "invalid_image":
            st.markdown(f"""
            <div style="background:#1a1208;border-radius:18px;padding:32px 32px 24px;
                        margin:16px 0 8px;position:relative;overflow:hidden;
                        box-shadow:0 16px 48px rgba(26,18,8,0.22);">
              <div style="position:absolute;top:0;left:0;right:0;height:3px;
                background:linear-gradient(90deg,#c8a84b,#e8c56a,#a8c49a);"></div>
              <div style="font-family:'DM Mono',monospace;font-size:.68rem;
                letter-spacing:.14em;text-transform:uppercase;color:#a8c49a;margin-bottom:8px;">⚠ Disease Detected</div>
              <div style="font-family:'Playfair Display',serif;font-size:1.85rem;
                font-weight:900;color:#faf7f0;margin-bottom:18px;line-height:1.15;">{disease_name}</div>
              <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <span style="background:rgba(168,196,154,0.12);border:1px solid rgba(168,196,154,0.22);
                  color:#a8c49a;border-radius:6px;padding:5px 13px;font-family:'DM Mono',monospace;font-size:.76rem;">Type: {disease_type}</span>
                <span style="background:rgba(168,196,154,0.12);border:1px solid rgba(168,196,154,0.22);
                  color:#a8c49a;border-radius:6px;padding:5px 13px;font-family:'DM Mono',monospace;font-size:.76rem;">Severity: {severity}</span>
                <span style="background:rgba(168,196,154,0.12);border:1px solid rgba(168,196,154,0.22);
                  color:#a8c49a;border-radius:6px;padding:5px 13px;font-family:'DM Mono',monospace;font-size:.76rem;">Confidence: {confidence}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

            def list_rows(items, accent="#7a9b6f"):
                return "".join(
                    f'<div style="font-size:.9rem;color:rgba(250,247,240,0.8);padding:5px 0 5px 20px;'
                    f'position:relative;line-height:1.6;border-bottom:1px solid rgba(255,255,255,0.05);">'
                    f'<span style="position:absolute;left:0;color:{accent};">→</span>{item}</div>'
                    for item in items)

            def section_block(label, icon, html, accent="#7a9b6f"):
                return (f'<div style="margin-bottom:20px;">'
                        f'<div style="font-family:\'DM Mono\',monospace;font-size:.68rem;letter-spacing:.14em;'
                        f'text-transform:uppercase;color:{accent};margin-bottom:10px;padding-bottom:6px;'
                        f'border-bottom:1px solid rgba(168,196,154,0.12);">{icon} {label}</div>{html}</div>')

            details = ""
            if result.get("symptoms"):        details += section_block("Symptoms",        "🔬", list_rows(result["symptoms"]))
            if result.get("possible_causes"): details += section_block("Possible Causes", "⚠",  list_rows(result["possible_causes"]))
            if result.get("treatment"):       details += section_block("Treatment",       "💊", list_rows(result["treatment"], "#c8a84b"), "#c8a84b")

            if details:
                st.markdown(f'<div style="background:#1a1208;border-radius:18px;padding:28px 32px;'
                            f'margin:0 0 16px;box-shadow:0 8px 32px rgba(26,18,8,0.18);">{details}</div>',
                            unsafe_allow_html=True)

            ts = result.get("analysis_timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.markdown(f'<p style="font-family:DM Mono,monospace;font-size:.7rem;color:#7a9b6f;'
                        f'text-align:right;padding:0 4px;">🕒 Analysed at {ts}</p>', unsafe_allow_html=True)

        elif not result.get("disease_detected") and disease_type != "invalid_image":
            st.markdown(f"""
            <div style="background:#1a1208;border-radius:18px;padding:36px 32px;margin:16px 0;
                        position:relative;overflow:hidden;box-shadow:0 16px 48px rgba(26,18,8,0.22);">
              <div style="position:absolute;top:0;left:0;right:0;height:3px;
                background:linear-gradient(90deg,#a8c49a,#d4e8cc,#a8c49a);"></div>
              <div style="font-family:'DM Mono',monospace;font-size:.68rem;letter-spacing:.14em;
                text-transform:uppercase;color:#a8c49a;margin-bottom:10px;">✓ Diagnosis Complete</div>
              <div style="font-size:3rem;margin-bottom:10px;">🌱</div>
              <div style="font-family:'Playfair Display',serif;font-size:1.85rem;font-weight:900;
                color:#d4e8cc;margin-bottom:16px;">Healthy Leaf</div>
              <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;">
                <span style="background:rgba(168,196,154,0.12);border:1px solid rgba(168,196,154,0.22);
                  color:#a8c49a;border-radius:6px;padding:5px 13px;font-family:'DM Mono',monospace;font-size:.76rem;">Status: Healthy</span>
                <span style="background:rgba(168,196,154,0.12);border:1px solid rgba(168,196,154,0.22);
                  color:#a8c49a;border-radius:6px;padding:5px 13px;font-family:'DM Mono',monospace;font-size:.76rem;">Confidence: {confidence}%</span>
              </div>
              <p style="color:rgba(212,232,204,0.6);font-size:.9rem;line-height:1.7;">
                No disease detected. Your plant appears to be in good health. Continue regular care and monitoring.
              </p>
            </div>""", unsafe_allow_html=True)

        if disease_type == "invalid_image":
            st.markdown("""
            <div style="background:rgba(180,40,40,0.08);border:1px solid rgba(220,80,80,0.3);
                        border-radius:14px;padding:26px 28px;margin:16px 0;">
              <div style="font-size:1.05rem;font-weight:700;color:#ff6b6b;margin-bottom:6px;">⚠️ Invalid Image</div>
              <p style="color:rgba(255,120,120,0.8);font-size:.9rem;line-height:1.6;">
                Please upload a clear, well-lit photo of a single plant leaf.</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("🌿  Scan Another Leaf", use_container_width=True):
            st.session_state.analysis_result      = None
            st.session_state.analysed_image_bytes = None
            st.session_state.analysed_image_type  = None
            st.session_state.upload_key           += 1
            st.rerun()

# ─── Spacer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="position:relative;overflow:hidden;padding:20px 24px 40px;">
  <div style="position:absolute;width:400px;height:400px;border-radius:50%;
    background:radial-gradient(circle,rgba(74,103,65,0.07) 0%,transparent 68%);
    top:-160px;left:-80px;pointer-events:none;"></div>
  <div style="position:absolute;width:340px;height:340px;border-radius:50%;
    background:radial-gradient(circle,rgba(200,168,75,0.05) 0%,transparent 68%);
    bottom:-120px;right:-60px;pointer-events:none;"></div>
  <div style="position:absolute;top:15%;left:3%;width:44px;opacity:.06;pointer-events:none;animation:leafFloat 9s ease-in-out infinite;">
    <svg viewBox='0 0 70 90' fill='none'><path d='M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z' fill='#3d4f2a'/><path d='M35 85V12' stroke='#7a9b6f' stroke-width='1.2'/></svg>
  </div>
  <div style="position:absolute;bottom:10%;right:4%;width:36px;opacity:.06;pointer-events:none;animation:leafFloat 11s ease-in-out 3s infinite;">
    <svg viewBox='0 0 70 90' fill='none'><path d='M35 85C8 62 4 36 18 12c9-8 26-8 34 0C67 36 62 62 35 85z' fill='#4a6741'/><path d='M35 85V12' stroke='#7a9b6f' stroke-width='1'/></svg>
  </div>
  <div style="background:#2d1f0e;border-radius:20px;padding:36px 24px;text-align:center;
    color:rgba(212,232,204,0.5);font-family:'DM Mono',monospace;font-size:.75rem;letter-spacing:.06em;
    max-width:800px;margin:0 auto;position:relative;z-index:1;box-shadow:0 16px 48px rgba(26,18,8,0.15);
    background-image:linear-gradient(rgba(168,196,154,0.04) 1px,transparent 1px),
      linear-gradient(90deg,rgba(168,196,154,0.04) 1px,transparent 1px);
    background-size:60px 60px;background-color:#2d1f0e;">
    <div style="font-size:1.4rem;margin-bottom:12px;">🌿</div>
    <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;
      color:rgba(212,232,204,0.7);margin-bottom:8px;">LeafScan AI</div>
    <div style="margin-bottom:10px;">Plant Pathology Intelligence</div>
    <div>Built with care ·
      <a href="https://github.com/Deepraj91/LeafScan-AI" target="_blank"
         style="color:#a8c49a;text-decoration:none;">View on GitHub</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)