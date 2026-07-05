"""
Generate CSV and premium HTML reports for backtest runs.
"""
from __future__ import annotations

from pathlib import Path
import logging
import pandas as pd
from typing import Dict

logger = logging.getLogger(__name__)


def generate_svg_chart(values: list, title: str, color: str = "#10B981", height: int = 180, width: int = 700) -> str:
    if not values:
        return ""

    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val if max_val != min_val else 1.0

    padding_x = 55
    padding_y = 20
    chart_w = width - (2 * padding_x)
    chart_h = height - (2 * padding_y)

    points = []
    n = len(values)
    for i, v in enumerate(values):
        x = padding_x + (i / (n - 1) * chart_w) if n > 1 else padding_x
        y = padding_y + chart_h - ((v - min_val) / val_range * chart_h)
        points.append((x, y))

    path_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area_d = f"{path_d} L {points[-1][0]:.1f},{padding_y + chart_h} L {points[0][0]:.1f},{padding_y + chart_h} Z"
    gradient_id = f"grad_{abs(hash(title)) & 0xffffffff}"

    svg = f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="auto" style="display: block; overflow: visible;">
        <defs>
            <linearGradient id="{gradient_id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{color}" stop-opacity="0.2"/>
                <stop offset="100%" stop-color="{color}" stop-opacity="0.0"/>
            </linearGradient>
        </defs>
        <!-- Grid lines -->
        <line x1="{padding_x}" y1="{padding_y}" x2="{width - padding_x}" y2="{padding_y}" stroke="#1E293B" stroke-dasharray="3"/>
        <line x1="{padding_x}" y1="{padding_y + chart_h/2}" x2="{width - padding_x}" y2="{padding_y + chart_h/2}" stroke="#1E293B" stroke-dasharray="3"/>
        <line x1="{padding_x}" y1="{padding_y + chart_h}" x2="{width - padding_x}" y2="{padding_y + chart_h}" stroke="#334155"/>
        
        <!-- Y-axis Labels -->
        <text x="{padding_x - 8}" y="{padding_y + 3}" fill="#64748B" font-family="Plus Jakarta Sans, sans-serif" font-size="9" text-anchor="end">{max_val:,.1f}</text>
        <text x="{padding_x - 8}" y="{padding_y + chart_h/2 + 3}" fill="#64748B" font-family="Plus Jakarta Sans, sans-serif" font-size="9" text-anchor="end">{(min_val + max_val)/2:,.1f}</text>
        <text x="{padding_x - 8}" y="{padding_y + chart_h + 3}" fill="#64748B" font-family="Plus Jakarta Sans, sans-serif" font-size="9" text-anchor="end">{min_val:,.1f}</text>
        
        <!-- Area fill -->
        <path d="{area_d}" fill="url(#{gradient_id})" />
        <!-- Line -->
        <path d="{path_d}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <!-- Start/End markers -->
        <circle cx="{points[0][0]:.1f}" cy="{points[0][1]:.1f}" r="3" fill="{color}"/>
        <circle cx="{points[-1][0]:.1f}" cy="{points[-1][1]:.1f}" r="3" fill="{color}"/>
    </svg>
    """
    return svg


def generate_reports(
    metrics: dict,
    trades: pd.DataFrame,
    equity: pd.DataFrame,
    out_dir: str | Path = "journal",
) -> Dict[str, Path]:
    """Write `trades`, `equity` and `metrics` to CSV files and build a stunning HTML dashboard under `out_dir`."""

    out = Path(out_dir)
    if not out.is_absolute():
        repo_root = Path(__file__).resolve().parent.parent
        out = repo_root / out
    out.mkdir(parents=True, exist_ok=True)

    files: Dict[str, Path] = {}

    trades_path = out / "trades.csv"
    trades.to_csv(trades_path, index=False)
    files["trades"] = trades_path

    equity_path = out / "equity.csv"
    equity.to_csv(equity_path, index=False)
    files["equity"] = equity_path

    perf_path = out / "performance.csv"
    pd.DataFrame([metrics]).to_csv(perf_path, index=False)
    files["performance"] = perf_path

    # Generate Equity Curve Chart SVG
    equity_curve_svg = ""
    if not equity.empty:
        equity_vals = equity["equity"].tolist()
        equity_curve_svg = generate_svg_chart(equity_vals, "Equity Curve", color="#10B981")

    # Generate Drawdown Curve Chart SVG
    drawdown_curve_svg = ""
    if not equity.empty:
        # Calculate drawdown list
        eq_series = equity["equity"]
        roll_max = eq_series.cummax()
        dd_vals = ((eq_series - roll_max) / roll_max * 100).tolist()
        drawdown_curve_svg = generate_svg_chart(dd_vals, "Drawdown Curve", color="#EF4444")

    # Generate Trade Rows HTML
    trade_rows_html = ""
    if not trades.empty:
        for idx, row in trades.iterrows():
            side = str(row.get("side", "BUY")).upper()
            side_badge = f'<span class="badge badge-long">BUY</span>' if side == "BUY" else f'<span class="badge badge-short">SELL</span>'
            pnl_val = float(row.get("pnl", 0))
            pnl_class = "pnl-profit" if pnl_val >= 0 else "pnl-loss"
            pnl_sign = "+" if pnl_val > 0 else ""
            trade_rows_html += f"""
            <tr>
                <td>{row.get("order_id", idx+1)}</td>
                <td>{row.get("symbol", "BANKNIFTY")}</td>
                <td>{side_badge}</td>
                <td>{float(row.get("entry_price", 0)):,.2f}</td>
                <td>{float(row.get("exit_price", 0)):,.2f}</td>
                <td>{int(row.get("quantity", 0))}</td>
                <td>{float(row.get("stop_loss", 0)):,.2f}</td>
                <td>{float(row.get("target", 0)):,.2f}</td>
                <td class="{pnl_class} font-bold">{pnl_sign}{pnl_val:,.2f}</td>
                <td>{row.get("status", "EXITED")}</td>
                <td class="text-secondary">{row.get("entry_time", "")}</td>
                <td class="text-secondary">{row.get("exit_time", "")}</td>
                <td class="text-secondary">{row.get("remarks", "")}</td>
            </tr>
            """
    else:
        trade_rows_html = "<tr><td colspan='13' class='text-center text-secondary py-8'>No trades recorded.</td></tr>"

    # Generate Monthly Returns HTML
    monthly_rows_html = ""
    monthly_returns = metrics.get("monthly_returns", {})
    if monthly_returns:
        for month, ret in monthly_returns.items():
            ret_class = "pnl-profit" if ret >= 0 else "pnl-loss"
            ret_sign = "+" if ret > 0 else ""
            monthly_rows_html += f"""
            <div class="monthly-card">
                <span class="text-secondary font-bold">{month}</span>
                <span class="font-bold {ret_class}" style="font-size: 1.15rem;">{ret_sign}{ret:.2f}%</span>
            </div>
            """
    else:
        monthly_rows_html = "<span class='text-secondary'>No monthly return history.</span>"

    win_rate = metrics.get("win_rate", 0.0)
    profit_factor = metrics.get("profit_factor", 0.0)
    pf_display = f"{profit_factor:.2f}" if profit_factor != float("inf") else "∞"

    # HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦅 Project FALCON Performance Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #080C14;
            --card-bg: #0F1626;
            --card-border: #1E293B;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --primary: #3B82F6;
            --success: #10B981;
            --danger: #EF4444;
            --accent: #8B5CF6;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 2rem;
            line-height: 1.5;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1.5rem;
        }}
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60A5FA, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }}
        .kpi-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: #334155;
        }}
        .kpi-title {{
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
        }}
        .kpi-sub {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }}
        .section-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
        }}
        .card-header {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            color: var(--text-primary);
            border-left: 3px solid var(--primary);
            padding-left: 0.75rem;
        }}
        .monthly-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 0.75rem;
        }}
        .monthly-card {{
            background-color: #0b111e;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 0.75rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
        }}
        .chart-container {{
            margin-top: 0.5rem;
            background-color: #080c14;
            border-radius: 8px;
            padding: 0.75rem;
            border: 1px solid #1E293B;
        }}
        .table-container {{
            overflow-x: auto;
            border: 1px solid var(--card-border);
            border-radius: 12px;
            background-color: var(--card-bg);
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }}
        th, td {{
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--card-border);
        }}
        th {{
            background-color: #0c1220;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}
        tr:hover td {{
            background-color: #121b2d;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .badge-long {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--success);
        }}
        .badge-short {{
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger);
        }}
        .pnl-profit {{
            color: var(--success);
        }}
        .pnl-loss {{
            color: var(--danger);
        }}
        .font-bold {{
            font-weight: 600;
        }}
        .text-secondary {{
            color: var(--text-secondary);
        }}
        .text-center {{
            text-align: center;
        }}
        .py-8 {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo-section">
            <div style="font-size: 2.25rem;">🦅</div>
            <div>
                <h1>PROJECT FALCON</h1>
                <div class="subtitle">Modular Quantitative Strategy Performance Report</div>
            </div>
        </div>
        <div style="text-align: right;">
            <div class="subtitle">Generated At</div>
            <div class="font-bold">{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
    </header>

    <main>
        <section class="kpi-grid">
            <div class="kpi-card" style="border-top: 3px solid var(--primary);">
                <span class="kpi-title">Net Profit</span>
                <span class="kpi-value {'pnl-profit' if metrics.get('total_pnl', 0) >= 0 else 'pnl-loss'}">
                    {'+' if metrics.get('total_pnl', 0) > 0 else ''}{metrics.get('total_pnl', 0):,.2f}
                </span>
                <span class="kpi-sub">Return Pct: {metrics.get('return_pct', 0.0):.2f}%</span>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--success);">
                <span class="kpi-title">Win Rate</span>
                <span class="kpi-value text-success" style="color: var(--success);">{win_rate:.2f}%</span>
                <span class="kpi-sub">Wins: {metrics.get('winning_trades', 0)} / Losses: {metrics.get('losing_trades', 0)}</span>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--accent);">
                <span class="kpi-title">Profit Factor</span>
                <span class="kpi-value" style="color: #A78BFA;">{pf_display}</span>
                <span class="kpi-sub">Gross Win/Loss ratio</span>
            </div>
            <div class="kpi-card" style="border-top: 3px solid #F59E0B;">
                <span class="kpi-title">Sharpe Ratio</span>
                <span class="kpi-value" style="color: #FBBF24;">{metrics.get('sharpe_ratio', 0.0):.2f}</span>
                <span class="kpi-sub">Annualized risk-adjusted</span>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--danger);">
                <span class="kpi-title">Max Drawdown</span>
                <span class="kpi-value pnl-loss">{metrics.get('max_drawdown', 0.0):.2f}%</span>
                <span class="kpi-sub">Peak-to-trough decline</span>
            </div>
        </section>

        <section class="section-grid">
            <div class="card">
                <div class="card-header">Equity Curve</div>
                <div class="chart-container">
                    {equity_curve_svg}
                </div>
            </div>
            <div class="card">
                <div class="card-header">Drawdown Curve</div>
                <div class="chart-container">
                    {drawdown_curve_svg}
                </div>
            </div>
        </section>

        <section class="section-grid">
            <div class="card">
                <div class="card-header">Performance Breakdown</div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem;">
                    <div>
                        <div class="text-secondary font-bold" style="font-size: 0.85rem;">Expectancy</div>
                        <div class="font-bold {'pnl-profit' if metrics.get('expectancy', 0) >= 0 else 'pnl-loss'}" style="font-size: 1.25rem;">
                            {metrics.get('expectancy', 0.0):+,.2f}
                        </div>
                    </div>
                    <div>
                        <div class="text-secondary font-bold" style="font-size: 0.85rem;">Avg PnL per Trade</div>
                        <div class="font-bold {'pnl-profit' if metrics.get('avg_pnl', 0) >= 0 else 'pnl-loss'}" style="font-size: 1.25rem;">
                            {metrics.get('avg_pnl', 0.0):+,.2f}
                        </div>
                    </div>
                    <div>
                        <div class="text-secondary" style="font-size: 0.8rem;">Average Winner</div>
                        <div class="pnl-profit font-bold">{metrics.get('average_winner', 0.0):+,.2f}</div>
                    </div>
                    <div>
                        <div class="text-secondary" style="font-size: 0.8rem;">Average Loser</div>
                        <div class="pnl-loss font-bold">{metrics.get('average_loser', 0.0):+,.2f}</div>
                    </div>
                    <div>
                        <div class="text-secondary" style="font-size: 0.8rem;">Largest Winner</div>
                        <div class="pnl-profit font-bold">{metrics.get('largest_winner', 0.0):+,.2f}</div>
                    </div>
                    <div>
                        <div class="text-secondary" style="font-size: 0.8rem;">Largest Loser</div>
                        <div class="pnl-loss font-bold">{metrics.get('largest_loser', 0.0):+,.2f}</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header">Monthly Performance</div>
                <div class="monthly-grid">
                    {monthly_rows_html}
                </div>
            </div>
        </section>

        <section class="card" style="margin-bottom: 2rem; padding: 0;">
            <div class="card-header" style="margin: 1.5rem 1.5rem 0 1.5rem;">Closed Trade Journal</div>
            <div class="table-container" style="border: none; box-shadow: none; margin-bottom: 0;">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Symbol</th>
                            <th>Side</th>
                            <th>Entry Price</th>
                            <th>Exit Price</th>
                            <th>Quantity</th>
                            <th>Stop Loss</th>
                            <th>Target</th>
                            <th>PnL</th>
                            <th>Status</th>
                            <th>Entry Time</th>
                            <th>Exit Time</th>
                            <th>Remarks</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trade_rows_html}
                    </tbody>
                </table>
            </div>
        </section>
    </main>
</body>
</html>
"""

    html_path = out / "report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    files["html"] = html_path

    logger.info("Reports written to %s", out)
    return files

