"""Rendering: Markdown digests, the Pages site, and the RSS feed."""
from __future__ import annotations

import html
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .config import Config, Topic

TOPIC_VAR = {
    "SEIKM-GEN": "--t-gen", "SEIKM-01": "--t-01", "SEIKM-02": "--t-02",
    "SEIKM-03": "--t-03", "SEIKM-04": "--t-04", "SEIKM-05": "--t-05",
    "SEIKM-06": "--t-06", "SEIKM-07": "--t-07",
}
README_START = "<!-- SEIKM:LATEST:START -->"
README_END = "<!-- SEIKM:LATEST:END -->"


# --------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------

def group_by_topic(config: Config, papers: list[dict[str, Any]]) -> list[tuple[Topic, list[dict]]]:
    """Order papers into topic sections, named topics first, General last."""
    out: list[tuple[Topic, list[dict]]] = []
    cap = int(config.output["max_per_topic"])
    for topic in config.all_topics():
        rows = [p for p in papers if p.get("topic") == topic.code]
        rows.sort(key=lambda p: p.get("rank_score", p.get("score", 0)), reverse=True)
        if rows:
            out.append((topic, rows[:cap]))
    return out


def select_for_issue(config: Config, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply the display floor and the global cap, keeping topic balance."""
    floor = float(config.output["min_display_score"])
    eligible = [p for p in papers if p.get("rank_score", p.get("score", 0)) >= floor]
    per_topic = int(config.output["max_per_topic"])
    total_cap = int(config.output["max_total"])

    buckets: dict[str, list[dict]] = {}
    for p in eligible:
        buckets.setdefault(p["topic"], []).append(p)
    for rows in buckets.values():
        rows.sort(key=lambda p: p.get("rank_score", p.get("score", 0)), reverse=True)
        del rows[per_topic:]

    # Round-robin across topics so a single busy topic cannot eat the cap.
    order = [t.code for t in config.all_topics()]
    selected: list[dict] = []
    depth = 0
    while len(selected) < total_cap:
        added = False
        for code in order:
            rows = buckets.get(code, [])
            if depth < len(rows):
                selected.append(rows[depth])
                added = True
                if len(selected) >= total_cap:
                    break
        if not added:
            break
        depth += 1
    return selected


def _authors(paper: dict[str, Any], limit: int = 5) -> str:
    names = paper.get("authors") or []
    if not names:
        return ""
    if len(names) <= limit:
        return ", ".join(names)
    return ", ".join(names[:limit]) + f", +{len(names) - limit} more"


def _snippet(paper: dict[str, Any], chars: int) -> str:
    text = " ".join((paper.get("abstract") or "").split())
    if len(text) <= chars:
        return text
    cut = text[:chars]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,;:.") + "…"


def _pretty_date(iso: str) -> str:
    # Built by hand: "%-d" is glibc-only and "%#d" is Windows-only.
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.strftime('%B')} {d.day}, {d.year}"


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def render_markdown(config: Config, issue: dict[str, Any], papers: list[dict]) -> str:
    site = config.site
    chars = int(config.output["snippet_chars"])
    lines: list[str] = []
    a = lines.append

    a(f"# {site['name']} — {_pretty_date(issue['date'])}")
    a("")
    a(f"Issue #{issue['number']} · **{len(papers)}** new papers · "
      f"{issue['scanned']} scanned from arXiv")
    a("")
    a(f"Sorted into the {config.committee_topic_count} topic areas of the "
      f"{site['committee']} technical committee.")
    a("")
    a(f"[Browse on the web]({site['base_url']}/) · "
      f"[All issues]({site['base_url']}/archive/) · "
      f"[How this works]({site['repo_url']}#how-it-works)")
    a("")

    groups = group_by_topic(config, papers)
    if not groups:
        a("_No papers cleared the relevance threshold today._")
        a("")
        return "\n".join(lines)

    a("**In this issue**")
    a("")
    for topic, rows in groups:
        anchor = topic.slug
        a(f"- [{topic.title}](#{anchor}) ({len(rows)})")
    a("")
    a("---")
    a("")

    for topic, rows in groups:
        a(f'<a id="{topic.slug}"></a>')
        a("")
        a(f"## {topic.title}")
        a("")
        a(f"`{topic.code}` — {topic.scope}")
        a("")
        for p in rows:
            a(f"#### [{p['title']}]({p['abs_url']})")
            a("")
            authors = _authors(p)
            if authors:
                a(f"*{authors}*")
                a("")
            if p.get("why"):
                a(f"> **Why it matters:** {p['why']}")
                a("")
            a(_snippet(p, chars))
            a("")
            bits = [f"`{p.get('primary_category','')}`"]
            for code in p.get("secondary_topics", []):
                bits.append(f"also `{code}`")
            bits.append(f"[abs]({p['abs_url']})")
            bits.append(f"[pdf]({p['pdf_url']})")
            a(" · ".join(bits))
            a("")
        a("---")
        a("")

    a(f"<sub>Generated {issue['generated']} · "
      f"[{site['repo_url'].split('github.com/')[-1]}]({site['repo_url']})</sub>")
    a("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

def _page(config: Config, *, title: str, rel: str, body: str) -> str:
    site = config.site
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(site['tagline'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(site['tagline'])}">
<meta property="og:type" content="website">
<link rel="alternate" type="application/rss+xml" title="{e(site['name'])}" href="{rel}feed.xml">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<header class="masthead">
  <div class="wrap">
    <p class="eyebrow">{e(site['committee'])}</p>
    <h1><a href="{rel}">{e(site['name'])}</a></h1>
    <p class="tagline">{e(site['tagline'])}</p>
    <nav>
      <a href="{rel}">Latest issue</a>
      <a href="{rel}archive/">Archive</a>
      <a href="{rel}feed.xml">RSS</a>
      <a href="{e(site['repo_url'])}">Source &amp; topic config</a>
      <a href="{e(site['repo_url'])}#how-it-works">How it works</a>
    </nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer>
  <div class="wrap">
    <p><b>How papers get here.</b> Every weekday a job queries arXiv across the
    categories and phrases listed in <code>config/settings.yaml</code>, drops
    anything that fails an engineering-relevance gate, and sorts the rest into
    the SEIKM topic areas using the weighted phrase lists in
    <code>config/topics.yaml</code>. Nothing is hand-picked, and nothing is
    peer-reviewed by this site — inclusion is not endorsement.</p>
    <p>Topic definitions follow the SEIKM 2027 track proposal. To correct a
    mis-filed paper or widen a topic, edit <code>config/topics.yaml</code> and
    open a pull request — no code changes needed.</p>
    <p>Maintained for the {e(site['committee'])} technical committee ·
    <a href="mailto:{e(site['contact_email'])}">{e(site['contact_email'])}</a> ·
    <a href="{e(site['repo_url'])}">GitHub</a></p>
  </div>
</footer>
</body>
</html>
"""


def _paper_html(paper: dict[str, Any], chars: int) -> str:
    e = html.escape
    authors = _authors(paper)
    parts = ['<article class="paper">']
    parts.append(
        f'<h4><a href="{e(paper["abs_url"])}">{e(paper["title"])}</a></h4>'
    )
    if authors:
        parts.append(f'<p class="authors">{e(authors)}</p>')
    if paper.get("why"):
        parts.append(f'<p class="why"><b>Why it matters:</b> {e(paper["why"])}</p>')
    parts.append(f'<p class="snippet">{e(_snippet(paper, chars))}</p>')

    meta = ['<div class="meta">']
    if paper.get("primary_category"):
        meta.append(f'<span class="chip cat">{e(paper["primary_category"])}</span>')
    for code in paper.get("secondary_topics", []):
        meta.append(f'<span class="chip also">also {e(code)}</span>')
    for term in (paper.get("matched_terms") or [])[:4]:
        meta.append(f'<span class="chip">{e(term)}</span>')
    meta.append('<span class="sep">·</span>')
    meta.append(
        f'<span class="links"><a href="{e(paper["abs_url"])}">abstract</a> · '
        f'<a href="{e(paper["pdf_url"])}">pdf</a></span>'
    )
    meta.append("</div>")
    parts.append("".join(meta))
    parts.append("</article>")
    return "\n".join(parts)


def render_issue_html(
    config: Config,
    issue: dict[str, Any],
    papers: list[dict],
    *,
    rel: str,
    recent: Iterable[dict[str, Any]] = (),
    is_home: bool = False,
) -> str:
    e = html.escape
    chars = int(config.output["snippet_chars"])
    groups = group_by_topic(config, papers)

    body: list[str] = ['<section class="issue-head">']
    body.append(f"<h2>{e(_pretty_date(issue['date']))}</h2>")
    body.append(
        f'<p class="issue-meta">Issue #{issue["number"]} · '
        f'<strong>{len(papers)}</strong> new papers · '
        f'{issue["scanned"]} scanned · '
        f'{len(groups)} topic area{"s" if len(groups) != 1 else ""}</p>'
    )
    body.append("</section>")

    if is_home:
        body.append(
            '<div class="callout">A daily, automatically assembled scan of new '
            'arXiv preprints relevant to SEIKM. <b>Inclusion is not endorsement</b> '
            '— these are unreviewed preprints, filtered by keyword, not by a human. '
            'Spotted something mis-filed? The topic definitions live in one editable '
            f'file: <a href="{e(config.site["repo_url"])}/blob/main/config/topics.yaml">'
            "config/topics.yaml</a>.</div>"
        )

    if not groups:
        body.append(
            '<div class="empty">No papers cleared the relevance threshold for this '
            "date. Quiet days happen — arXiv volume drops sharply over weekends and "
            "holidays.</div>"
        )
    else:
        nav = ['<ul class="topicnav">']
        for topic, rows in groups:
            var = TOPIC_VAR.get(topic.code, "--t-gen")
            nav.append(
                f'<li><a href="#{topic.slug}" style="--tc:var({var})">'
                f'<span class="dot"></span>{e(topic.short)} '
                f'<span class="n">{len(rows)}</span></a></li>'
            )
        nav.append("</ul>")
        body.append("".join(nav))

        for topic, rows in groups:
            var = TOPIC_VAR.get(topic.code, "--t-gen")
            body.append(f'<section class="topic" id="{topic.slug}" style="--tc:var({var})">')
            body.append('<div class="topic-head">')
            body.append(f'<div class="topic-code">{e(topic.code)}</div>')
            body.append(f"<h3>{e(topic.title)}</h3>")
            if topic.scope:
                body.append(f"<p>{e(topic.scope)}</p>")
            body.append("</div>")
            for paper in rows:
                body.append(_paper_html(paper, chars))
            body.append("</section>")

    recent = list(recent)
    if is_home and recent:
        body.append('<section class="topic"><div class="topic-head">')
        body.append("<h3>Recent issues</h3></div>")
        body.append('<ul class="issue-list">')
        for item in recent:
            body.append(
                f'<li><span class="d"><a href="archive/{item["date"]}.html">'
                f'{e(_pretty_date(item["date"]))}</a></span>'
                f'<span class="c">{item["count"]} papers</span></li>'
            )
        body.append("</ul>")
        body.append(f'<p style="margin-top:14px"><a href="archive/">All issues →</a></p>')
        body.append("</section>")

    title = f"{config.site['name']} — {_pretty_date(issue['date'])}"
    return _page(config, title=title, rel=rel, body="\n".join(body))


def render_archive_html(config: Config, issues: list[dict[str, Any]]) -> str:
    e = html.escape
    body = ['<section class="issue-head"><h2>Archive</h2>']
    body.append(
        f'<p class="issue-meta">{len(issues)} issue{"s" if len(issues) != 1 else ""} · '
        f'{sum(i["count"] for i in issues)} papers indexed</p></section>'
    )
    if not issues:
        body.append('<div class="empty">No issues published yet.</div>')
    else:
        body.append('<ul class="issue-list">')
        for item in issues:
            body.append(
                f'<li><span class="d"><a href="{item["date"]}.html">'
                f'{e(_pretty_date(item["date"]))}</a></span>'
                f'<span class="c">issue #{item.get("number", "?")} · '
                f'{item["count"]} papers</span></li>'
            )
        body.append("</ul>")
    return _page(config, title=f"Archive — {config.site['name']}", rel="../",
                 body="\n".join(body))


# --------------------------------------------------------------------------
# RSS
# --------------------------------------------------------------------------

def render_feed(config: Config, issues: list[dict[str, Any]], latest: list[dict]) -> str:
    site = config.site
    e = html.escape
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items: list[str] = []
    for issue in issues[:20]:
        url = f"{site['base_url']}/archive/{issue['date']}.html"
        pub = datetime.strptime(issue["date"], "%Y-%m-%d").strftime(
            "%a, %d %b %Y 09:00:00 +0000"
        )
        desc = f"{issue['count']} new SEIKM-relevant arXiv papers."
        if issue["date"] == (issues[0]["date"] if issues else "") and latest:
            desc += " " + "; ".join(p["title"] for p in latest[:5])
        items.append(
            "<item>"
            f"<title>{e(site['name'])} — {e(_pretty_date(issue['date']))}</title>"
            f"<link>{e(url)}</link><guid isPermaLink=\"true\">{e(url)}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{e(desc)}</description>"
            "</item>"
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>{e(site['name'])}</title>
<link>{e(site['base_url'])}/</link>
<description>{e(site['tagline'])}</description>
<language>en-us</language>
<lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
</channel></rss>
"""


# --------------------------------------------------------------------------
# README
# --------------------------------------------------------------------------

def render_readme_block(config: Config, issue: dict[str, Any], papers: list[dict]) -> str:
    site = config.site
    groups = group_by_topic(config, papers)
    lines = [README_START, ""]
    lines.append(f"### Latest issue — {_pretty_date(issue['date'])}")
    lines.append("")
    lines.append(
        f"**{len(papers)}** new papers across **{len(groups)}** topic areas "
        f"· [read on the web]({site['base_url']}/) "
        f"· [markdown](digests/{issue['date']}.md)"
    )
    lines.append("")
    if not groups:
        lines.append("_No papers cleared the relevance threshold._")
    else:
        for topic, rows in groups:
            lines.append(f"**{topic.title}** ({len(rows)})")
            lines.append("")
            for p in rows[:3]:
                lines.append(f"- [{p['title']}]({p['abs_url']})")
            if len(rows) > 3:
                lines.append(f"- _…{len(rows) - 3} more_")
            lines.append("")
    lines.append(README_END)
    return "\n".join(lines)


def splice_readme(readme: str, block: str) -> str:
    if README_START in readme and README_END in readme:
        head = readme.split(README_START)[0]
        tail = readme.split(README_END, 1)[1]
        return head + block + tail
    return readme.rstrip() + "\n\n" + block + "\n"
