#!/usr/bin/env python3
"""Build the System Design Interview Guide PDF.

questions/*.md  ->  book.md (cover + TOC + all chapters)
                ->  book.html (pandoc, syntax highlighting)
                ->  System_Design_Interview_Guide.pdf (Chromium via playwright-cli)
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(ROOT, "questions")
OUT_MD = os.path.join(ROOT, "book.md")
OUT_HTML = os.path.join(ROOT, "book.html")
OUT_PDF = os.path.join(ROOT, "System_Design_Interview_Guide.pdf")
CSS = os.path.join(ROOT, "book.css")

# Icon names the writers used that do not exist in the Iconify "logos" set
# (checked against https://api.iconify.design/collection?prefix=logos).
ICON_FIXES = {
    "logos:aws-elastic-load-balancing": "logos:aws-elb",
    "logos:aws-opensearch": "logos:aws-open-search",
    "logos:aws-emr": "logos:apache-spark",
    "logos:aws-sagemaker": "mdi:brain",
    "logos:flink": "logos:apache-flink-icon",
}

def fix_icon_names(text):
    for bad, good in ICON_FIXES.items():
        text = text.replace(bad, good)
    return text

# The Mermaid "architecture-beta" renderer draws tiny icons and breaks layout on
# PDF pages. Redraw each deployment map as a flowchart: groups -> nested
# subgraphs (cloud boxes), services -> icon nodes, edges -> plain arrows.
ARCH_RE = re.compile(r"```mermaid\n\s*architecture-beta\n(.*?)```", re.S)

GROUP_STYLE = {
    "internet": "fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,stroke-dasharray:5 4",
    "edge":     "fill:#fff7ed,stroke:#ec7211,stroke-width:1.5px",
    "vpc":      "fill:#faf5ff,stroke:#8c4fff,stroke-width:2px",
    "app":      "fill:#f0fdf4,stroke:#1d8102,stroke-width:1.5px",
    "data":     "fill:#eff6ff,stroke:#147eba,stroke-width:1.5px",
    "ext":      "fill:#f1f5f9,stroke:#475569,stroke-width:1.5px,stroke-dasharray:5 4",
}
GROUP_TITLE = {"vpc": "AWS VPC", "app": "Service subnet", "data": "Data subnet"}

def arch_to_flowchart(src):
    groups, order, services, edges = {}, [], {}, []
    for raw in src.splitlines():
        s = raw.strip()
        m = re.match(r"group (\w+)\(([^)]*)\)\[([^\]]*)\](?: in (\w+))?$", s)
        if m:
            groups[m[1]] = (m[2], m[3], m[4]); order.append(m[1]); continue
        m = re.match(r"service (\w+)\(([^)]*)\)\[([^\]]*)\](?: in (\w+))?$", s)
        if m:
            services[m[1]] = (m[2], m[3], m[4]); continue
        m = re.match(r"(\w+):[LRTB] (<--|-->|--) [LRTB]:(\w+)$", s)
        if m:
            a, kind, b = m[1], m[2], m[3]
            edges.append((b, a, "-->") if kind == "<--" else (a, b, "-->" if kind == "-->" else "---"))
    children = {g: [] for g in groups}
    roots = []
    for g in order:
        parent = groups[g][2]
        (children[parent] if parent in children else roots).append(g)
    svc_in = {g: [] for g in groups}
    loose = []
    for sid, (_, _, g) in services.items():
        (svc_in[g] if g in svc_in else loose).append(sid)

    def node(sid):
        icon, title, _ = services[sid]
        form = "square" if icon.startswith("logos:") else "rounded"
        return f'{sid}@{{ icon: "{icon}", form: "{form}", label: "{title}", pos: "b", h: 48 }}'

    out = ["flowchart LR"]

    def emit(g, depth):
        ind = "    " * depth
        title = GROUP_TITLE.get(g, groups[g][1])
        out.append(f'{ind}subgraph {g}["{title}"]')
        out.append(f"{ind}    direction TB")
        for sid in svc_in[g]:
            out.append(ind + "    " + node(sid))
        for c in children[g]:
            emit(c, depth + 1)
        out.append(f"{ind}end")

    for g in roots:
        emit(g, 1)
    for sid in loose:
        out.append("    " + node(sid))
    for a, b, arrow in edges:
        if a in services and b in services:
            out.append(f"    {a} {arrow} {b}")
    for g in groups:
        out.append(f"    style {g} {GROUP_STYLE.get(g, 'fill:#f8fafc,stroke:#94a3b8')}")
    return "\n".join(out)

files = sorted(glob.glob(os.path.join(Q_DIR, "[0-9][0-9]-*.md")))
if not files:
    sys.exit("no question files")

chapters = []
for f in files:
    text = open(f, encoding="utf-8").read().strip()
    m = re.match(r"^#\s+(.+?)\s*$", text, re.M)
    title = m.group(1) if m else os.path.basename(f)
    # anchor id: pandoc auto-ids from the H1 text; we force our own.
    slug = os.path.basename(f)[:-3]
    text = re.sub(r"^#\s+(.+?)\s*$", rf"# \1 {{#{slug}}}", text, count=1, flags=re.M)
    diff = "Hard" if "(Hard)" in title else "Medium" if "(Medium)" in title else "Easy"
    text = fix_icon_names(text)
    text = ARCH_RE.sub(lambda m: "```mermaid\n" + arch_to_flowchart(m.group(1)) + "\n```", text)
    # Readability: writers used 48-56 px icons, which read as specks next to
    # the tier boxes. Scale every icon node up at build time.
    text = re.sub(r"\bh:\s*(4[0-9]|5[0-9])\s*\}", "h: 76 }", text)
    chapters.append((slug, title, diff, text))

def toc_rows(level):
    rows = []
    for slug, title, diff, _ in chapters:
        if diff != level:
            continue
        name = re.sub(r"^\d+\.\s*", "", title)
        name = re.sub(r"\s*\((Easy|Medium|Hard)\)\s*$", "", name)
        rows.append(f"| [{name}](#{slug}) | {level} |")
    return rows

cover = f"""---
title: "System Design Interview Guide"
subtitle: "36 questions, requirements to final architecture"
lang: en
---

<div class="cover">

# System Design Interview Guide {{.unnumbered .cover-title}}

## 36 questions, from requirements to final architecture {{.unnumbered}}

Every chapter follows the same ten steps, so you can drill the method, not just the answer:

1. Functional requirements
2. Non-functional requirements
3. Back-of-the-envelope estimates
4. Core entities
5. API design
6. High-level design (how will users do X?)
7. Deep dives (how do we make it fast, correct, and scalable?)
8. Final architecture
9. Common mistakes and follow-ups
10. One-page cheat sheet

Plain words, real numbers, and code where code is clearer than prose.

</div>

<div class="toc-page">

# Contents {{.unnumbered}}

## Easy {{.unnumbered}}

| Question | Level |
|---|---|
{chr(10).join(toc_rows("Easy"))}

## Medium {{.unnumbered}}

| Question | Level |
|---|---|
{chr(10).join(toc_rows("Medium"))}

## Hard {{.unnumbered}}

| Question | Level |
|---|---|
{chr(10).join(toc_rows("Hard"))}

</div>

"""

body = "\n\n<div class=\"page-break\"></div>\n\n".join(c[3] for c in chapters)
open(OUT_MD, "w", encoding="utf-8").write(cover + body + "\n")

HEADER = os.path.join(ROOT, "mermaid_header.html")
open(HEADER, "w", encoding="utf-8").write("""
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
// Real component icons: product logos (Postgres, Redis, Kafka, S3 ...) and Material icons.
mermaid.registerIconPacks([
  { name: "logos", loader: () => fetch("https://unpkg.com/@iconify-json/logos@1/icons.json").then(r => r.json()) },
  { name: "mdi",   loader: () => fetch("https://unpkg.com/@iconify-json/mdi@1/icons.json").then(r => r.json()) },
]);
mermaid.initialize({ startOnLoad: false, theme: "base",
  themeVariables: {
    primaryColor: "#dbeafe", primaryBorderColor: "#1d4ed8", primaryTextColor: "#0f172a",
    actorBkg: "#dbeafe", actorBorder: "#1d4ed8", actorTextColor: "#0f172a",
    actorLineColor: "#94a3b8", signalColor: "#1e40af", signalTextColor: "#0f172a",
    labelBoxBkgColor: "#fef3c7", labelBoxBorderColor: "#d97706", labelTextColor: "#0f172a",
    loopTextColor: "#92400e", noteBkgColor: "#fef9c3", noteBorderColor: "#ca8a04",
    activationBkgColor: "#bfdbfe", activationBorderColor: "#1d4ed8",
    sequenceNumberColor: "#ffffff", lineColor: "#1e293b",
    edgeLabelBackground: "#ffffff", fontSize: "15px",
    clusterBkg: "#f8fafc", clusterBorder: "#94a3b8",
    secondaryColor: "#ecfdf5", tertiaryColor: "#f8fafc"
  },
  // Wider gaps so icons, their labels and the arrow labels never touch, and
  // each tier box has room around its icons.
  flowchart: { htmlLabels: false, useMaxWidth: true, curve: "basis",
               padding: 24, nodeSpacing: 70, rankSpacing: 90, subGraphTitleMargin: { top: 8, bottom: 8 } },
  sequence: { useMaxWidth: true, actorMargin: 60, messageMargin: 44, boxMargin: 12 } });
// pandoc emits <pre class="mermaid"><code>src</code></pre>; mermaid wants the raw text.
for (const pre of document.querySelectorAll("pre.mermaid")) {
  const code = pre.querySelector("code");
  if (code) pre.textContent = code.textContent;
}
await mermaid.run({ querySelector: "pre.mermaid" });
window.__mermaidDone = true;
document.title = "MERMAID_DONE " + document.querySelectorAll("pre.mermaid > svg").length;
</script>
""")

subprocess.run(
    ["pandoc", OUT_MD, "-f", "markdown+pipe_tables+fenced_code_attributes",
     "-t", "html5", "-s", "--highlight-style", "tango",
     "-c", "book.css", "-H", HEADER,
     "--metadata", "pagetitle=System Design Interview Guide",
     "-o", OUT_HTML],
    check=True,
)

# Web edition: same book, arrows flow and icons breathe. Open it in a browser.
OUT_WEB = os.path.join(ROOT, "System_Design_Interview_Guide_web.html")
TOOLBAR = """
<div class="anim-bar">
  <span>System Design Interview Guide, web edition</span>
  <button type="button" onclick="document.body.classList.toggle('anim');
    this.textContent = document.body.classList.contains('anim') ? 'Pause motion' : 'Play motion'">Pause motion</button>
</div>
"""
html = open(OUT_HTML, encoding="utf-8").read()
html = html.replace("<body>", "<body class=\"anim web\">" + TOOLBAR, 1)
open(OUT_WEB, "w", encoding="utf-8").write(html)

# Chromium print via playwright-cli. file: URLs are blocked, so serve on localhost.
PORT = 8765
server = subprocess.Popen(
    [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1",
     "--directory", ROOT],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
try:
    import time
    time.sleep(1.0)
    subprocess.run(["playwright-cli", "close"], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["playwright-cli", "open", f"http://127.0.0.1:{PORT}/book.html"],
                   check=True)
    time.sleep(45.0)  # icon packs download (~3 MB) + ~100 Mermaid diagrams render
    subprocess.run(["playwright-cli", "pdf", "--filename", OUT_PDF], check=True)
    subprocess.run(["playwright-cli", "close"], check=False)
finally:
    server.terminate()

size = os.path.getsize(OUT_PDF) / 1e6
print(f"{len(chapters)} chapters -> {OUT_PDF} ({size:.1f} MB)")
