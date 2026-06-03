"""Generate health reports: CLI, JSON, and HTML dashboard."""
import json
import sys
from pathlib import Path


def _print(*args, **kwargs):
    """Print with UTF-8 fallback for Windows terminals with limited codepages."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        safe = text.encode("ascii", errors="replace").decode("ascii")
        print(safe, **{k: v for k, v in kwargs.items() if k != "end"})


def cli_report(results: dict) -> None:
    summary = results.get("summary", {})
    score = summary.get("health_score", 0)
    icon = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"

    _print(f"\n[Health] Harness Health Report -- {results.get('timestamp', '?')}")
    _print(f"{icon} Health Score: {score}/100")
    _print(f"[i] Checks Run:  {summary.get('total_checks', 0)}")
    alerts = results.get("alerts", [])
    errors = [a for a in alerts if a.get("severity") == "error"]
    warns  = [a for a in alerts if a.get("severity") == "warning"]
    _print(f"[!] Alerts:      {len(errors)} errors, {len(warns)} warnings")

    if alerts:
        _print("\n[ALERTS]:")
        for a in alerts:
            e = "[ERR]" if a["severity"] == "error" else "[WARN]"
            _print(f"  {e} [{a['check']}] {a['message']}")

    # File size
    fs = results.get("checks", {}).get("file_size", {})
    if fs.get("warnings"):
        _print("\n[File Size Warnings (top 3)]:")
        for w in fs["warnings"][:3]:
            _print(f"   - {w.split(chr(10))[0]}")

    # Context
    ctx = results.get("checks", {}).get("context_coverage", {})
    if ctx.get("total_calls", 0) > 0:
        _print("\n[Context Efficiency]:")
        _print(f"   - Avg Coverage:  {ctx['avg_coverage']:.1%}")
        _print(f"   - Avg Waste:     {ctx['avg_waste_percent']:.1f}%")
        if ctx.get("missing_context_incidents"):
            _print(f"   - Missing Ctx:   {len(ctx['missing_context_incidents'])} incidents")

    # Recommendations
    recs = results.get("recommendations", [])
    if recs:
        _print("\n[Recommendations]:")
        for i, r in enumerate(recs, 1):
            _print(f"   {i}. {r}")
    _print()


def json_report(results: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )
    _print(f"[Saved] JSON report saved: {output_path}")


def html_dashboard(results: dict, output_path: Path) -> None:
    summary = results.get("summary", {})
    score = summary.get("health_score", 0)
    color_cls = "good" if score >= 80 else "warn" if score >= 50 else "crit"
    alerts = results.get("alerts", [])

    alert_html = "".join(
        f"<div class='alert {a['severity']}'>"
        f"<strong>[{a['check']}]</strong> {a['message']}</div>"
        for a in alerts
    ) or "<p>✅ No alerts</p>"

    ctx = results.get("checks", {}).get("context_coverage", {})
    tok = results.get("checks", {}).get("token_efficiency", {})
    rb  = results.get("checks", {}).get("role_boundary_audit", {})
    ov  = results.get("checks", {}).get("human_override_rate", {})

    def _fmt(v, pct: bool = False) -> str:
        if v in (None, "no_logs", "N/A", ""):
            return "N/A"
        if pct and isinstance(v, float):
            return f"{v:.1%}"
        return str(v)

    details_json = json.dumps(results.get("checks", {}), indent=2, default=str)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Harness Health Dashboard</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 0.2rem; }}
  .score {{ font-size: 3rem; font-weight: 800; margin: 0.5rem 0; }}
  .score.good {{ color: #16a34a; }}
  .score.warn {{ color: #d97706; }}
  .score.crit {{ color: #dc2626; }}
  .alert {{ padding: 0.4rem 1rem; margin: 0.3rem 0; border-left: 4px solid; border-radius: 2px; }}
  .alert.error   {{ border-color: #dc2626; background: #fef2f2; }}
  .alert.warning {{ border-color: #d97706; background: #fffbeb; }}
  .metrics {{ display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0; }}
  .metric {{ border: 1px solid #e5e7eb; border-radius: 6px; padding: 0.8rem 1.2rem; min-width: 160px; }}
  .metric strong {{ display: block; font-size: 0.75rem; color: #6b7280; text-transform: uppercase; }}
  .metric span {{ font-size: 1.3rem; font-weight: 600; }}
  pre {{ background: #f8fafc; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.8rem; }}
</style>
</head>
<body>
<h1>🩺 Harness Health Dashboard</h1>
<p style="color:#6b7280">Generated: {results.get('timestamp', '?')}</p>

<div class="score {color_cls}">{score}/100</div>

<h2>🚨 Alerts ({len(alerts)})</h2>
{alert_html}

<h2>📊 Key Metrics</h2>
<div class="metrics">
  <div class="metric"><strong>Context Coverage</strong><span>{_fmt(ctx.get('avg_coverage'), pct=True)}</span></div>
  <div class="metric"><strong>Context Waste</strong><span>{_fmt(ctx.get('avg_waste_percent'))}%</span></div>
  <div class="metric"><strong>Token / Success</strong><span>{_fmt(tok.get('avg_tokens_per_success'))}</span></div>
  <div class="metric"><strong>Role Violations</strong><span>{_fmt(rb.get('violation_rate'), pct=True)}</span></div>
  <div class="metric"><strong>Human Override</strong><span>{_fmt(ov.get('override_rate'), pct=True)}</span></div>
</div>

<h2>🔍 Full Results</h2>
<pre>{details_json}</pre>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"🌐 Dashboard saved: {output_path}")
