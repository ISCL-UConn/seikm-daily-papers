#!/usr/bin/env python3
"""Write the pre-first-issue site.

Run once at setup so the Pages URL is live and presentable before the first
scheduled harvest lands. Touches nothing in data/ — the first real run still
publishes as issue #1.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seikm import render  # noqa: E402
from seikm.config import load_config  # noqa: E402

config = load_config(ROOT / "config")
site = config.site
e = __import__("html").escape

rows = "\n".join(
    f"<tr><td><code>{e(t.code)}</code></td><td><b>{e(t.title)}</b>"
    f'<span class="scope">{e(t.scope)}</span></td></tr>'
    for t in config.all_topics()
)

body = f"""<section class="issue-head">
<h2>The first issue is on its way</h2>
<p class="issue-meta">Scheduled for 06:30 Eastern, weekday mornings.</p>
</section>

<div class="callout">
Every weekday this page is rebuilt with new arXiv preprints relevant to the
{e(site['committee'])} technical committee, sorted into the topic areas below.
<b>Inclusion is not endorsement</b> — these are unreviewed preprints selected by
keyword matching, not by a person.
</div>

<section class="topic"><div class="topic-head"><h3>Topic areas</h3>
<p>Following the SEIKM 2027 track proposal. The phrase lists behind each one live in
<a href="{e(site['repo_url'])}/blob/main/config/topics.yaml">config/topics.yaml</a>
and are a one-line pull request to change.</p></div>
<div class="table-scroll"><table class="topic-table">
<tbody>{rows}</tbody></table></div>
</section>

<section class="topic"><div class="topic-head"><h3>Follow along</h3></div>
<p style="color:var(--text-dim)">
Subscribe by <a href="feed.xml">RSS</a>, or watch
<a href="{e(site['repo_url'])}">the repository</a> on GitHub for a notification
each morning. Past issues collect in the <a href="archive/">archive</a>.</p>
</section>"""

docs = ROOT / "docs"
(docs / "archive").mkdir(parents=True, exist_ok=True)
(docs / ".nojekyll").touch()
(docs / "index.html").write_text(
    render._page(config, title=site["name"], rel="", body=body), encoding="utf-8")
(docs / "archive" / "index.html").write_text(
    render.render_archive_html(config, []), encoding="utf-8")
(docs / "feed.xml").write_text(render.render_feed(config, [], []), encoding="utf-8")
print("Initial site written to docs/ — the first scheduled run replaces it.")
