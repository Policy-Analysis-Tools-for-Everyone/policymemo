#!/usr/bin/env python3
"""Build the set-up guides that go out with beta invites: one per AI tool, as HTML and PDF.

The beta is private, so set-up steps are not published on policymemo.ai. Instead each
invite carries the guide for the tool that person uses. The guides are built from the
same hand-written source the install page used, site/install/body.html, so there is
still only one copy of the steps.

    python3 tools/build-guides.py            # HTML and PDF into guides/
    python3 tools/build-guides.py --html     # HTML only (no browser needed)

Writes guides/policymemo-ai-setup-<tool>.html and .pdf. guides/ is gitignored: the
repository is public, so the guides are never committed. Share them by hand.

Needs the markdown package (for build-site.py) and, for PDFs, Playwright with Chromium
(pip install markdown playwright && playwright install chromium). To use a Chromium
you already have, set CHROMIUM=/path/to/chrome.
"""
import importlib.util
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "guides"
SRC = ROOT / "site" / "install"

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build-site.py")
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)

TOOLS = {
    "claude": ("Claude", "Claude, in a browser or the desktop app. About 2 minutes on a paid plan, 10 on the free plan."),
    "chatgpt": ("ChatGPT", "ChatGPT with plugins. About 2 minutes."),
    "copilot": ("Microsoft 365 Copilot", "Copilot Chat on a work or university Microsoft account. About 10 minutes."),
    "gemini": ("Google Gemini", "Gemini with skills switched on. About 5 minutes."),
}

GUIDE_CSS = """
  /* Set-up guides: one tool per file, no tabs. */
  .guide-meta { color: var(--muted); font-size: 14px; margin-top: 10px; }
  .route-h { font: 500 15px/1.3 var(--sans) !important; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 30px 0 4px !important; }
  .sub + .sub { margin-top: 40px !important; }
  .private { margin-top: 18px; padding: 12px 16px; border-left: 3px solid var(--accent); color: var(--muted); font-size: 14.5px; max-width: 720px; }
  @media print {
    @page { size: A4; margin: 16mm 14mm; }
    html, body { background: #fff !important; }
    header.top nav, footer nav, .copy { display: none !important; }
    header.top { position: static !important; }
    .install-hero { padding-top: 8px; }
    details > div { display: block !important; }
    summary::after { content: none !important; }
    .steps > li, details, .worked, .get, .val { break-inside: avoid; }
    h2, h3, h4 { break-after: avoid; }
    .sub { break-before: auto; }
    .faq { margin-top: 40px; }
    a { color: inherit; }
  }
"""

COPY_JS = """<script>
document.querySelectorAll('.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var t = b.getAttribute('data-copy');
    function done() { b.textContent = 'Copied'; b.classList.add('done'); setTimeout(function () { b.textContent = 'Copy'; b.classList.remove('done'); }, 1600); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () {});
  });
});
window.addEventListener('beforeprint', function () { document.querySelectorAll('details').forEach(function (d) { d.open = true; }); });
</script>"""


def section(src, start_marker, end_marker):
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:j]


def panel(src, tool):
    s = section(src, f'<section class="panel" id="{tool}"', "</section>") + "</section>"
    s = s.replace(' role="tabpanel"', "")
    s = re.sub(r' aria-labelledby="tab-[\w-]+"', "", s)
    if tool == "claude":
        # The paid/free switch becomes two labelled parts, so both survive in a PDF.
        s = re.sub(r'\s*<div class="route".*?</div>', "", s, count=1, flags=re.S)
        s = s.replace('<div class="sub" id="claude-paid">',
                      '<div class="sub" id="claude-paid">\n    <h4 class="route-h">On a paid plan (Pro, Max, Team or Enterprise)</h4>')
        s = s.replace('<div class="sub" id="claude-free">',
                      '<div class="sub" id="claude-free">\n    <h4 class="route-h">On the free plan</h4>')
        s = s.replace('<p style="margin-top:22px">', "<p>")
    return s


def build(tool, src, css):
    label, meta = TOOLS[tool]
    faq = section(src, '<section class="faq"', "</section>") + "</section>"
    report = section(src, '<section class="report"', "</section>") + "</section>"
    body = f"""<section class="wrap install-hero">
  <p class="eyebrow">Set-up guide · beta {site.VERSION}</p>
  <h1>Set up policymemo.ai in {label}</h1>
  <p class="lede">You set it up once, on a computer.</p>
  <p class="guide-meta">{meta}</p>
  <p class="private">This guide is for people invited to the private beta. Please don't post it publicly. If someone else would like to try policymemo.ai, point them to <a href="https://policymemo.ai/beta/">policymemo.ai/beta</a>.</p>
</section>
<div class="wrap install-layout" style="display:block">
{panel(src, tool)}
{faq}
{report}
</div>
{COPY_JS}"""
    html_ = site.page(f"Set up policymemo.ai in {label}",
                      f"How to set up policymemo.ai in {label}. For people invited to the private beta.",
                      body, css, "https://policymemo.ai/", current=None)
    # Private guides: keep them out of search engines if one is ever put online by mistake.
    html_ = html_.replace("<head>\n", '<head>\n<meta name="robots" content="noindex, nofollow">\n', 1)
    html_ = html_.replace(site.GENERATED, "<!-- generated by tools/build-guides.py from site/install/body.html -->")
    return html_


def pdfs(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        # CHROMIUM=/path/to/chrome uses a browser Playwright did not install itself.
        exe = os.environ.get("CHROMIUM")
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = browser.new_page()
        for path in paths:
            pg.goto(path.resolve().as_uri(), wait_until="networkidle")
            pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            pg.emulate_media(media="print")
            pg.pdf(path=str(path.with_suffix(".pdf")), format="A4", print_background=True,
                   margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
            print(f"  {path.with_suffix('.pdf').relative_to(ROOT)}")
        browser.close()


def main():
    src = (SRC / "body.html").read_text(encoding="utf-8")
    css = site.CSS.read_text(encoding="utf-8") + "\n" + (SRC / "install.css").read_text(encoding="utf-8") + GUIDE_CSS
    OUT.mkdir(exist_ok=True)
    written = []
    for tool in TOOLS:
        path = OUT / f"policymemo-ai-setup-{tool}.html"
        path.write_text(build(tool, src, css), encoding="utf-8")
        written.append(path)
        print(f"  {path.relative_to(ROOT)}")
    if "--html" not in sys.argv:
        pdfs(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
