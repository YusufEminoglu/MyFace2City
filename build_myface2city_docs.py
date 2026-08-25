# -*- coding: utf-8 -*-
"""Generate interactive manual and documentation site for MyFace2City."""

from pathlib import Path

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MyFace2City — Optical Urban Portrait & Generative Cartography Engine</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #0b0f19; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .hero-glow { background: radial-gradient(circle at 50% 20%, rgba(255, 0, 85, 0.15), rgba(112, 0, 255, 0.1), transparent 70%); }
    .card-border { border: 1px solid #1e293b; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px); }
  </style>
</head>
<body class="hero-glow min-h-screen flex flex-col justify-between">
  <header class="border-b border-slate-800 bg-slate-950/80 sticky top-0 z-50 backdrop-blur">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <img src="favicon.svg" alt="MyFace2City" class="w-8 h-8 rounded-lg border border-pink-500/40">
        <span class="font-extrabold text-xl tracking-tight text-white">MyFace<span class="text-pink-500">2City</span></span>
        <span class="bg-purple-900/50 text-purple-300 text-xs px-2.5 py-0.5 rounded-full border border-purple-500/30">v0.1.0</span>
      </div>
      <div class="flex items-center space-x-6 text-sm font-medium text-slate-300">
        <a href="#quickstart" class="hover:text-pink-400 transition">Quick Start</a>
        <a href="#presets" class="hover:text-pink-400 transition">10 Art Presets</a>
        <a href="#stippling" class="hover:text-pink-400 transition">Halftone &amp; Stippling</a>
        <a href="https://github.com/YusufEminoglu/MyFace2City" target="_blank" class="bg-pink-600 hover:bg-pink-500 text-white px-4 py-1.5 rounded-lg transition font-semibold">GitHub</a>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-6 py-12 space-y-16 flex-1">
    <!-- Hero Section -->
    <section class="text-center space-y-6 pt-6">
      <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-pink-500/30 bg-pink-500/10 text-pink-300 text-xs font-semibold">
        <span>🎭 Standalone Python SDK &amp; QGIS 02Urban Portrait Engine</span>
      </div>
      <h1 class="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
        Turn Urban Street Networks &amp; Buildings into <br>
        <span class="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-400 bg-clip-text text-transparent">Live Optical Portrait Art</span>
      </h1>
      <p class="text-lg text-slate-400 max-w-3xl mx-auto">
        A map-locked generative cartography engine. Binds any portrait photo to geographic bounding boxes or road networks, sampling luminance into 5-stage reversible rule-based optical art.
      </p>
      <div class="flex items-center justify-center space-x-4 pt-4">
        <div class="bg-slate-900 border border-slate-700 px-4 py-2 rounded-lg font-mono text-sm text-pink-400">
          pip install myface2city
        </div>
      </div>
    </section>

    <!-- 10 Art Presets Gallery -->
    <section id="presets" class="space-y-6">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 class="text-2xl font-bold text-white">🎨 10 Curated Art Presets</h2>
          <p class="text-slate-400 text-sm">Professional cartographic palettes inspired by classic printmaking and modern digital aesthetics.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Cyberpunk 2077</h3>
            <span class="text-xs bg-pink-950 text-pink-400 px-2 py-0.5 rounded border border-pink-800">Neon Dark</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#060814]"></div>
            <div class="flex-1 bg-[#7000ff]"></div>
            <div class="flex-1 bg-[#ff0055]"></div>
            <div class="flex-1 bg-[#00f0ff]"></div>
            <div class="flex-1 bg-[#ffe600]"></div>
          </div>
          <p class="text-xs text-slate-400">Vibrant high-contrast neon palette with glowing line underlays.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Ink Portrait</h3>
            <span class="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">Monochrome</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#090b10]"></div>
            <div class="flex-1 bg-[#20242d]"></div>
            <div class="flex-1 bg-[#4d535f]"></div>
            <div class="flex-1 bg-[#a8adb5]"></div>
            <div class="flex-1 bg-[#e7e9ec]"></div>
          </div>
          <p class="text-xs text-slate-400">Traditional ink printmaking with cream parchment background.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Blueprint</h3>
            <span class="text-xs bg-cyan-950 text-cyan-400 px-2 py-0.5 rounded border border-cyan-800">Architectural</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#effcff]"></div>
            <div class="flex-1 bg-[#a7e8f2]"></div>
            <div class="flex-1 bg-[#58c9da]"></div>
            <div class="flex-1 bg-[#2389a1]"></div>
            <div class="flex-1 bg-[#155064]"></div>
          </div>
          <p class="text-xs text-slate-400">Architectural drafting blueprint with cyan stroke gradients.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Vintage Engraving</h3>
            <span class="text-xs bg-amber-950 text-amber-400 px-2 py-0.5 rounded border border-amber-800">Classic</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#2c1d11]"></div>
            <div class="flex-1 bg-[#4a3525]"></div>
            <div class="flex-1 bg-[#70533d]"></div>
            <div class="flex-1 bg-[#a48366]"></div>
            <div class="flex-1 bg-[#d8c5b0]"></div>
          </div>
          <p class="text-xs text-slate-400">Warm copperplate engraving tones on vintage rag paper.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Emerald Eco-Map</h3>
            <span class="text-xs bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800">Organic</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#061c14]"></div>
            <div class="flex-1 bg-[#0f3d2e]"></div>
            <div class="flex-1 bg-[#1e6b52]"></div>
            <div class="flex-1 bg-[#3fa882]"></div>
            <div class="flex-1 bg-[#7be3bc]"></div>
          </div>
          <p class="text-xs text-slate-400">Deep forest and emerald greens for ecological compositions.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Nordic Slate</h3>
            <span class="text-xs bg-slate-900 text-slate-400 px-2 py-0.5 rounded border border-slate-700">Minimalist</span>
          </div>
          <div class="h-6 rounded flex overflow-hidden border border-slate-700">
            <div class="flex-1 bg-[#12171c]"></div>
            <div class="flex-1 bg-[#242d38]"></div>
            <div class="flex-1 bg-[#414f5e]"></div>
            <div class="flex-1 bg-[#7a8a9e]"></div>
            <div class="flex-1 bg-[#cbd5e1]"></div>
          </div>
          <p class="text-xs text-slate-400">Cool Scandinavian slate and minimalist muted tones.</p>
        </div>
      </div>
    </section>

    <!-- Quickstart Code Section -->
    <section id="quickstart" class="space-y-6">
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-2xl font-bold text-white">💻 Quick Start Code Examples</h2>
      </div>

      <div class="card-border rounded-xl p-6 space-y-4 font-mono text-sm">
        <p class="text-slate-400">// Render a face onto urban roads &amp; export vector SVG artwork</p>
        <pre class="text-pink-300 overflow-x-auto"><code>import myface2city as mfc

# 1. Initialize portrait engine with image and geographic bounds
bounds = (27.10, 38.40, 27.20, 38.50)  # (min_lon, min_lat, max_lon, max_lat)
portrait = mfc.UrbanPortrait("face.jpg", bounds)

# 2. Fetch OSM vector roads & buildings or load local GeoJSON
geojson = mfc.fetch_osm_network(bounds)

# 3. Apply optical portrait styling with Cyberpunk preset
styled_geojson = portrait.process_geojson(geojson, palette="Cyberpunk 2077")

# 4. Export high-resolution standalone vector SVG poster
mfc.export_svg(styled_geojson, "urban_portrait.svg", preset="Cyberpunk 2077")</code></pre>
      </div>
    </section>
  </main>

  <footer class="border-t border-slate-800 bg-slate-950 py-8 text-center text-sm text-slate-500">
    <p>MyFace2City is created by <a href="https://github.com/YusufEminoglu" class="text-pink-400 hover:underline">Yusuf Eminoğlu</a>. Licensed under the MIT License.</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    index_file = docs_dir / "index.html"
    index_file.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"Generated docs at: {index_file.resolve()}")


if __name__ == "__main__":
    main()
