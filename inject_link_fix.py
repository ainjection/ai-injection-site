"""Inject a lightweight lightbox + click-interceptor into pages that still leak
aishotstudio.com links. Clicks on those links open an in-page image viewer
instead of navigating away.

Idempotent: detects an existing marker comment and replaces the block.
"""
import re, sys
from pathlib import Path

PAGES_DIR = Path(__file__).parent / "pages"
MARKER_BEGIN = "<!-- AI-INJECTION-LINK-FIX-BEGIN -->"
MARKER_END = "<!-- AI-INJECTION-LINK-FIX-END -->"

INJECT_BLOCK = MARKER_BEGIN + """
<style>
  #ai-lightbox{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:99999;display:none;align-items:center;justify-content:center;cursor:zoom-out;padding:60px}
  #ai-lightbox.show{display:flex;animation:ailb-fade .18s ease-out}
  #ai-lightbox-body{max-width:min(720px,75vw);max-height:80vh;display:flex;align-items:center;justify-content:center}
  #ai-lightbox img,#ai-lightbox video{max-width:100%;max-height:80vh;width:auto;height:auto;object-fit:contain;box-shadow:0 24px 96px rgba(0,0,0,.6);border-radius:8px;cursor:default}
  #ai-lightbox-close{position:absolute;top:18px;right:24px;font-size:42px;color:#fff;background:rgba(255,255,255,.12);border:0;width:56px;height:56px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1}
  #ai-lightbox-close:hover{background:rgba(255,255,255,.25)}
  @keyframes ailb-fade{from{opacity:0}to{opacity:1}}
</style>
<div id="ai-lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button id="ai-lightbox-close" aria-label="Close">&times;</button>
  <div id="ai-lightbox-body"></div>
</div>
<script>
(function(){
  var IMG_EXT = /\\.(jpe?g|png|webp|gif|svg)(\\?|$)/i;
  var lb = document.getElementById('ai-lightbox');
  var body = document.getElementById('ai-lightbox-body');
  var closeBtn = document.getElementById('ai-lightbox-close');
  function open(src){
    body.innerHTML = '<img src="' + src + '" alt="">';
    lb.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function close(){
    lb.classList.remove('show');
    body.innerHTML = '';
    document.body.style.overflow = '';
  }
  closeBtn.addEventListener('click', close);
  lb.addEventListener('click', function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });

  // Intercept clicks on aishotstudio.com links AND clicks directly on images
  document.addEventListener('click', function(e){
    var a = e.target.closest('a');
    if (a) {
      var href = a.getAttribute('href') || '';
      // Only intercept legacy external links to ai-shot-studio
      if (href.indexOf('aishotstudio.com') !== -1) {
        e.preventDefault();
        // If link has an inline image, prefer that for the lightbox
        var inner = a.querySelector('img');
        if (inner && inner.src) { open(inner.src); return; }
        // Else if href itself is an image, open it
        if (IMG_EXT.test(href)) { open(href); return; }
        // Otherwise open the link's image-equivalent if recognizable, else swallow click silently
        return;
      }
      return; // let other links navigate normally
    }
    // Direct click on an image (no surrounding link) — open in lightbox
    var img = e.target.closest('img');
    if (img && img.src && !img.closest('header') && !img.closest('nav') && !img.closest('.fusion-menu') && !img.closest('.aii-sticky-cta')) {
      // Skip tiny logos / icons
      if (img.naturalWidth >= 200 || img.width >= 200) {
        e.preventDefault();
        open(img.src);
      }
    }
  });
})();
</script>
""" + MARKER_END

def already_injected(html):
    return MARKER_BEGIN in html

def inject(html):
    if already_injected(html):
        # Replace existing block to support iteration
        pat = re.compile(re.escape(MARKER_BEGIN) + r".*?" + re.escape(MARKER_END), re.DOTALL)
        return pat.sub(INJECT_BLOCK, html)
    # Insert before </body>
    if "</body>" in html:
        return html.replace("</body>", INJECT_BLOCK + "\n</body>", 1)
    # Fallback: append
    return html + "\n" + INJECT_BLOCK

def process(path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if "aishotstudio.com" not in txt and "<img" not in txt:
        return False
    new = inject(txt)
    if new != txt:
        path.write_text(new, encoding="utf-8")
        return True
    return False

if __name__ == "__main__":
    targets = list(PAGES_DIR.rglob("raw.html")) + [PAGES_DIR.parent / "index.html"]
    n_changed = 0
    for p in targets:
        if not p.exists(): continue
        if process(p):
            n_changed += 1
            print(f"✓ injected: {p.relative_to(PAGES_DIR.parent)}")
    print(f"\nDone. {n_changed} files updated.")
