# Design de l'interface (CSS isole)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #f6f8fc; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1250px; }

/* Header */
.hdr {
    background:#fff; border:1px solid #eceff5; border-radius:16px;
    padding:16px 22px; display:flex; align-items:center; gap:14px; margin-bottom:20px;
}
.hdr-icon {
    width:44px; height:44px; background:#2E6FED; border-radius:12px;
    display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;
}
.hdr-title { font-size:18px; font-weight:600; color:#0f172a; line-height:1.2; }
.hdr-sub { font-size:12.5px; color:#64748b; }
.hdr-badge {
    margin-left:auto; background:#ecfdf3; border:1px solid #bbf7d0; color:#15803d;
    border-radius:999px; padding:5px 14px; font-size:12px; font-weight:500;
}

/* Cards */
.card {
    background:#fff; border:1px solid #eceff5; border-radius:16px; padding:22px;
}
.card-title { font-size:16px; font-weight:600; color:#0f172a; display:flex; align-items:center; gap:8px; }
.card-sub { font-size:12.5px; color:#64748b; margin-top:2px; }

/* Metric cards */
.metric {
    background:#fff; border:1px solid #eceff5; border-radius:16px; padding:18px 20px;
}
.metric-ic {
    width:38px; height:38px; border-radius:11px; display:flex; align-items:center;
    justify-content:center; font-size:18px; margin-bottom:14px;
}
.metric-n { font-size:30px; font-weight:700; color:#0f172a; line-height:1; }
.metric-l { font-size:14px; font-weight:600; color:#0f172a; margin-top:6px; }
.metric-t { font-size:12px; color:#94a3b8; margin-top:2px; }

/* Tags */
.tag {
    display:inline-block; background:#eef3fd; color:#1e3a6e; border-radius:999px;
    padding:3px 12px; font-size:12px; font-weight:500; margin:3px 3px 0 0;
}
.badge-tg {
    background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; border-radius:8px;
    padding:5px 12px; font-size:12px; font-weight:500; white-space:nowrap;
}

/* Task rows */
.task {
    display:flex; gap:11px; padding:12px 14px; border:1px solid #eef1f6;
    border-radius:12px; margin-bottom:9px; background:#fff;
}
.dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; margin-top:6px; background:#2E6FED; }
.task-id { font-size:11px; color:#94a3b8; font-weight:500; }
.task-title { font-size:13.5px; font-weight:500; color:#0f172a; margin:3px 0; }
.task-meta { font-size:12px; color:#64748b; }
.avatar {
    width:20px; height:20px; border-radius:50%; background:#dbeafe; color:#2E6FED;
    font-size:9px; font-weight:700; display:inline-flex; align-items:center;
    justify-content:center; vertical-align:middle; margin-right:5px;
}
.pill-open {
    display:inline-block; background:#dcfce7; color:#166534; border-radius:6px;
    padding:1px 9px; font-size:11px; font-weight:500;
}

/* Divider */
.hr { height:1px; background:#eef1f6; margin:14px 0; }

/* Buttons */
.stButton > button {
    background:#2E6FED !important; color:#fff !important; border:none !important;
    border-radius:10px !important; padding:9px 20px !important; font-weight:500 !important;
    font-size:14px !important;
}
.stButton > button:hover { background:#1d5cd6 !important; }
.stDownloadButton > button {
    background:#eef3fd !important; color:#2E6FED !important; border:1px solid #cfe0fb !important;
    border-radius:10px !important; font-weight:500 !important;
}

/* Chat */
.bubble-a {
    background:#f1f5f9; color:#0f172a; border-radius:14px 14px 14px 4px;
    padding:11px 15px; font-size:13.5px; line-height:1.6; max-width:82%; margin-bottom:12px;
}
.bubble-u {
    background:#2E6FED; color:#fff; border-radius:14px 14px 4px 14px;
    padding:11px 15px; font-size:13.5px; line-height:1.6; max-width:82%;
    margin-left:auto; margin-bottom:12px;
}
</style>
"""