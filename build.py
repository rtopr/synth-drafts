"""Build the Nolan view page: one section per synth (spin clip, then lit / power off / top / low stills)."""
import base64, io, os
from PIL import Image

SRC = r"D:\synth-media\designs\cloud"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
D = [
    ("01-light-valley", "Light Valley", "Pale plaster land. Light runs down carved valleys from the screen to the controls."),
    ("02-caldera", "Caldera", "A flat basalt volcano. Lava paths branch from the screen to the pads; the main dial rises from a sharp ridge."),
    ("03-live-edge", "Live Edge", "A lobed wood-fibre slab with layered edges. The dial sits in a knot ringed by growth rings that fill with light."),
    ("04-kelly-planes", "Kelly Planes", "Stacked white plates. Shadows show the zones; light comes out of the gaps between plates."),
    ("05-ben-day-stone", "Ben-Day Stone", "Pale stone with pop-art dots only where they do a job: speaker, hand zone, dotted light paths."),
    ("06-scope-gray", "Scope Gray", "A thin gray instrument with one orange dial and an oscilloscope grid over the screen."),
    ("07-muted-yellow", "Muted Yellow", "One ochre color all through. A white sail dial fills with light; straight white lines run to each control."),
    ("08-skyspace-tunnel", "Skyspace Tunnel", "The screen sits at the bottom of a stepped well. Turn the ring around it; the steps light as you go deeper."),
    ("09-two-and-three", "Two and Three", "Chord pads in two rows, the back ones grouped 2 + 3 like a piano's black keys, plus a dotted strum strip."),
    ("10-open-cube-field", "Open Cube Field", "A graph-paper grid. An open cube marks where your hand plays in the air."),
]
VIEWS = [("hero", "Lit"), ("unlit", "Power off"), ("top", "Top"), ("low", "Low")]

def jpg(path):
    im = Image.open(path).convert("RGB"); im.thumbnail((1200, 1200))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

parts = []
for slug, name, line in D:
    n = slug[:2]; folder = os.path.join(SRC, slug)
    s = [f'<section id="d{n}"><h2>{n} {name}</h2><p>{line}</p>']
    mp4 = os.path.join(folder, f"{slug}_turntable.mp4")
    if os.path.exists(mp4):
        v = base64.b64encode(open(mp4, "rb").read()).decode()
        s.append(f'<video autoplay loop muted playsinline src="data:video/mp4;base64,{v}"></video>')
    for key, label in VIEWS:
        p = os.path.join(folder, f"{slug}_{key}.png")
        if os.path.exists(p):
            s.append(f'<figure><img loading="lazy" src="{jpg(p)}" alt="{name}, {label}"><figcaption>{label}</figcaption></figure>')
    parts.append("".join(s) + "</section>")

nav = "".join(f'<a href="#d{s[:2]}">{s[:2]} {n}</a>' for s, n, _ in D)
html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Synth: 10 design directions</title><style>
body{{margin:0;background:#111;color:#eee;font:16px -apple-system,system-ui,sans-serif}}
nav{{position:sticky;top:0;z-index:2;display:flex;gap:6px;overflow-x:auto;padding:8px;background:#111e;backdrop-filter:blur(6px)}}
nav a{{flex:none;color:#eee;text-decoration:none;font-size:13px;padding:6px 10px;border:1px solid #444;border-radius:16px}}
h1{{font-size:20px;margin:16px 12px 4px}} .note{{margin:0 12px 8px;color:#999;font-size:14px}}
section{{padding:20px 0 8px;border-top:1px solid #2a2a2a;scroll-margin-top:48px}}
h2{{font-size:18px;margin:0 12px 4px}} p{{margin:0 12px 10px;color:#bbb;line-height:1.4}}
video,img{{display:block;width:100%;height:auto;background:#ddd}} figure{{margin:6px 0 0}}
figcaption{{font-size:12px;color:#888;padding:4px 12px}}
</style></head><body><h1>Synth: 10 design directions</h1><p class="note">Rough drafts, 2026-11-13</p><nav>{nav}</nav>{''.join(parts)}</body></html>"""
open(OUT, "w", encoding="utf-8").write(html)
print(OUT, round(len(html) / 1e6, 1), "MB")
