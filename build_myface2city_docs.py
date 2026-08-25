"""Generate high-end interactive manual and live generative art studio for MyFace2City."""

from pathlib import Path

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MyFace2City — Optical Urban Portrait & Generative Cartography Engine</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              pink: '#ff0055',
              purple: '#7000ff',
              cyan: '#00f0ff',
              dark: '#090d1a',
              card: '#0f172a'
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background: #070a13; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .hero-glow { background: radial-gradient(circle at 50% 15%, rgba(255, 0, 85, 0.18), rgba(112, 0, 255, 0.12), transparent 70%); }
    .card-border { border: 1px solid #1e293b; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(16px); }
    .canvas-container { box-shadow: 0 0 50px -10px rgba(0, 240, 255, 0.15); }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
  </style>
</head>
<body class="hero-glow min-h-screen flex flex-col justify-between selection:bg-pink-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <img src="favicon.svg" alt="MyFace2City" class="w-8 h-8 rounded-lg shadow-lg shadow-pink-500/20 border border-pink-500/40">
        <span class="font-black text-xl tracking-tight text-white">MyFace<span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-cyan-400">2City</span></span>
        <span class="bg-purple-950 text-purple-300 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-purple-500/40">v0.1.0</span>
      </div>
      <div class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
        <a href="#studio" class="hover:text-cyan-400 transition">Live Studio</a>
        <a href="#presets" class="hover:text-pink-400 transition">10 Art Presets</a>
        <a href="#quickstart" class="hover:text-purple-400 transition">Quick Start</a>
        <a href="#api" class="hover:text-cyan-400 transition">API Reference</a>
        <a href="https://pypi.org/project/myface2city/" target="_blank" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition">PyPI Package</a>
        <a href="https://github.com/YusufEminoglu/MyFace2City" target="_blank" class="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white px-4 py-1.5 rounded-lg font-semibold shadow-md shadow-pink-500/20 transition">GitHub</a>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-6 py-12 space-y-20 flex-1 w-full">

    <!-- Hero Section -->
    <section class="text-center space-y-6 pt-4">
      <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-pink-500/30 bg-pink-500/10 text-pink-300 text-xs font-semibold">
        <span>🎭 Generative Cartography &amp; Optical Portrait Engine</span>
      </div>
      <h1 class="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
        Turn Urban Street Networks &amp; Buildings into <br>
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-400">Live Optical Portrait Art</span>
      </h1>
      <p class="text-base sm:text-lg text-slate-400 max-w-3xl mx-auto">
        A map-locked spatial art engine. Binds any portrait photo to geographic bounding boxes or road networks, sampling pixel luminance into 5-stage reversible rule-based optical art.
      </p>
      
      <div class="flex flex-wrap items-center justify-center gap-4 pt-2">
        <div class="bg-slate-900 border border-slate-700 px-4 py-2.5 rounded-xl font-mono text-sm text-pink-400 flex items-center space-x-3 shadow-inner">
          <span>pip install myface2city</span>
          <button onclick="navigator.clipboard.writeText('pip install myface2city'); alert('Copied to clipboard!')" class="text-slate-400 hover:text-white text-xs bg-slate-800 px-2 py-1 rounded border border-slate-700">Copy</button>
        </div>
        <a href="#studio" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-lg shadow-cyan-500/20 transition">
          Launch Live Studio ↓
        </a>
      </div>
    </section>

    <!-- LIVE GENERATIVE STUDIO -->
    <section id="studio" class="space-y-6 pt-8">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
            <span>✨ Live In-Browser Generative Studio</span>
          </h2>
          <p class="text-slate-400 text-sm">Select a portrait demo or upload your own, choose an art preset, and download the vector SVG artwork.</p>
        </div>
        <div class="flex items-center space-x-3">
          <button id="btnModeNetwork" onclick="setStudioMode('network')" class="px-4 py-1.5 rounded-lg text-xs font-bold bg-pink-600 text-white shadow-md shadow-pink-500/20">Street Network</button>
          <button id="btnModeStipple" onclick="setStudioMode('stipple')" class="px-4 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">Halftone Stipple</button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Controls (Left 4 cols) -->
        <div class="lg:col-span-4 card-border p-6 rounded-2xl space-y-6">
          <!-- Portrait Source -->
          <div class="space-y-2">
            <label class="text-xs font-bold uppercase tracking-wider text-slate-400">1. Select Face / Portrait</label>
            <div class="grid grid-cols-3 gap-2">
              <button onclick="loadSampleFace('portrait1')" class="border border-slate-700 hover:border-pink-500 bg-slate-800/80 p-2 rounded-lg text-xs font-medium text-center transition">
                Demo Face 1
              </button>
              <button onclick="loadSampleFace('portrait2')" class="border border-slate-700 hover:border-pink-500 bg-slate-800/80 p-2 rounded-lg text-xs font-medium text-center transition">
                Demo Face 2
              </button>
              <button onclick="loadSampleFace('monalisa')" class="border border-slate-700 hover:border-pink-500 bg-slate-800/80 p-2 rounded-lg text-xs font-medium text-center transition">
                Mona Lisa
              </button>
            </div>
            <div class="pt-2">
              <label class="block text-[11px] text-slate-400 mb-1">Or upload custom image:</label>
              <input type="file" id="imageUpload" accept="image/*" class="w-full text-xs text-slate-400 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-pink-400 hover:file:bg-slate-700 cursor-pointer">
            </div>
          </div>

          <!-- Art Preset Selection -->
          <div class="space-y-2">
            <label class="text-xs font-bold uppercase tracking-wider text-slate-400">2. Art Direction Preset</label>
            <select id="presetSelect" onchange="updateArtRender()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-pink-500">
              <option value="Cyberpunk 2077" selected>Cyberpunk 2077 (Neon Dark)</option>
              <option value="Ink Portrait">Ink Portrait (Fine Art Monochrome)</option>
              <option value="Blueprint">Blueprint (Architectural Cyan)</option>
              <option value="Vintage Engraving">Vintage Engraving (Copperplate Warm)</option>
              <option value="Neon Night">Neon Night (Vibrant Synthwave)</option>
              <option value="Emerald Eco-Map">Emerald Eco-Map (Organic Green)</option>
              <option value="Sepia Blocks">Sepia Blocks (Historic Parchment)</option>
              <option value="Nordic Slate">Nordic Slate (Minimalist Cool)</option>
              <option value="Thermal Heatmap">Thermal Heatmap (Spectrogram)</option>
              <option value="Negative City">Negative City (Inverted Indigo)</option>
            </select>
          </div>

          <!-- Sliders -->
          <div class="space-y-4 pt-2">
            <div>
              <div class="flex justify-between text-xs text-slate-300 font-medium mb-1">
                <span>Density / Resolution</span>
                <span id="lblDensity">45</span>
              </div>
              <input type="range" id="sliderDensity" min="20" max="80" value="45" oninput="document.getElementById('lblDensity').innerText=this.value; updateArtRender();" class="w-full accent-pink-500">
            </div>

            <div>
              <div class="flex justify-between text-xs text-slate-300 font-medium mb-1">
                <span>Gamma Contrast</span>
                <span id="lblGamma">1.0</span>
              </div>
              <input type="range" id="sliderGamma" min="0.3" max="2.5" step="0.1" value="1.0" oninput="document.getElementById('lblGamma').innerText=this.value; updateArtRender();" class="w-full accent-pink-500">
            </div>

            <div class="flex items-center space-x-2 pt-1">
              <input type="checkbox" id="chkInvert" onchange="updateArtRender()" class="w-4 h-4 rounded text-pink-600 bg-slate-900 border-slate-700 focus:ring-pink-500">
              <label for="chkInvert" class="text-xs text-slate-300 font-medium cursor-pointer">Invert Negative Tones</label>
            </div>
          </div>

          <!-- Action Button -->
          <div class="pt-4 space-y-2">
            <button onclick="downloadSvgArtwork()" class="w-full bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-500 hover:opacity-90 text-white font-bold py-3 rounded-xl shadow-lg shadow-pink-500/20 transition flex items-center justify-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
              <span>Download Vector SVG Poster</span>
            </button>
          </div>
        </div>

        <!-- Canvas Output (Right 8 cols) -->
        <div class="lg:col-span-8 card-border p-6 rounded-2xl flex flex-col items-center justify-center min-h-[560px] canvas-container">
          <div id="svgContainer" class="w-full max-w-[560px] aspect-square rounded-xl overflow-hidden shadow-2xl border border-slate-800 bg-slate-950 flex items-center justify-center">
            <!-- Dynamic SVG injected here -->
          </div>
          <div class="flex items-center justify-between w-full max-w-[560px] pt-4 text-xs text-slate-400">
            <span id="canvasStats">Features: 2,025 | Bounding Box: 100x100</span>
            <span class="text-pink-400 font-medium">100% Vector Scalable Artwork</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 10 Art Presets Section -->
    <section id="presets" class="space-y-6 pt-8">
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-2xl font-bold text-white">🎨 10 Curated Cartographic Art Presets</h2>
        <p class="text-slate-400 text-sm">Professional cartographic palettes inspired by classic printmaking and modern digital aesthetics.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Cyberpunk 2077</h3>
            <span class="text-xs bg-pink-950 text-pink-400 px-2 py-0.5 rounded border border-pink-800">Neon Dark</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#060814]"></div>
            <div class="flex-1 bg-[#7000ff]"></div>
            <div class="flex-1 bg-[#ff0055]"></div>
            <div class="flex-1 bg-[#00f0ff]"></div>
            <div class="flex-1 bg-[#ffe600]"></div>
          </div>
          <p class="text-xs text-slate-400">Vibrant high-contrast neon palette with glowing underlays on dark obsidian background.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Ink Portrait</h3>
            <span class="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">Monochrome</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#090b10]"></div>
            <div class="flex-1 bg-[#20242d]"></div>
            <div class="flex-1 bg-[#4d535f]"></div>
            <div class="flex-1 bg-[#a8adb5]"></div>
            <div class="flex-1 bg-[#e7e9ec]"></div>
          </div>
          <p class="text-xs text-slate-400">Traditional woodblock and ink printmaking on cream parchment background.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Blueprint</h3>
            <span class="text-xs bg-cyan-950 text-cyan-400 px-2 py-0.5 rounded border border-cyan-800">Architectural</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#effcff]"></div>
            <div class="flex-1 bg-[#a7e8f2]"></div>
            <div class="flex-1 bg-[#58c9da]"></div>
            <div class="flex-1 bg-[#2389a1]"></div>
            <div class="flex-1 bg-[#155064]"></div>
          </div>
          <p class="text-xs text-slate-400">Architectural drafting blueprint with cyan stroke gradients and deep navy background.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Vintage Engraving</h3>
            <span class="text-xs bg-amber-950 text-amber-400 px-2 py-0.5 rounded border border-amber-800">Classic</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#2c1d11]"></div>
            <div class="flex-1 bg-[#4a3525]"></div>
            <div class="flex-1 bg-[#70533d]"></div>
            <div class="flex-1 bg-[#a48366]"></div>
            <div class="flex-1 bg-[#d8c5b0]"></div>
          </div>
          <p class="text-xs text-slate-400">Warm copperplate engraving tones on vintage aged cotton paper.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Emerald Eco-Map</h3>
            <span class="text-xs bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800">Organic</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#061c14]"></div>
            <div class="flex-1 bg-[#0f3d2e]"></div>
            <div class="flex-1 bg-[#1e6b52]"></div>
            <div class="flex-1 bg-[#3fa882]"></div>
            <div class="flex-1 bg-[#7be3bc]"></div>
          </div>
          <p class="text-xs text-slate-400">Deep forest and emerald greens for ecological urban compositions.</p>
        </div>

        <div class="card-border p-5 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-white">Nordic Slate</h3>
            <span class="text-xs bg-slate-900 text-slate-400 px-2 py-0.5 rounded border border-slate-700">Minimalist</span>
          </div>
          <div class="h-7 rounded-lg flex overflow-hidden border border-slate-700 shadow-inner">
            <div class="flex-1 bg-[#12171c]"></div>
            <div class="flex-1 bg-[#242d38]"></div>
            <div class="flex-1 bg-[#414f5e]"></div>
            <div class="flex-1 bg-[#7a8a9e]"></div>
            <div class="flex-1 bg-[#cbd5e1]"></div>
          </div>
          <p class="text-xs text-slate-400">Cool Scandinavian slate and minimalist muted tones on off-white canvas.</p>
        </div>
      </div>
    </section>

    <!-- Quick Start Code -->
    <section id="quickstart" class="space-y-6 pt-8">
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-2xl font-bold text-white">💻 Quick Start Python Guide</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Card 1 -->
        <div class="card-border p-6 rounded-2xl space-y-4 font-mono text-xs">
          <div class="flex justify-between items-center text-slate-400">
            <span class="font-bold text-pink-400 uppercase">Urban Street Network Rendering</span>
            <span>example_roads.py</span>
          </div>
          <pre class="bg-slate-950 p-4 rounded-xl text-slate-300 overflow-x-auto border border-slate-800"><code>import myface2city as mfc

# 1. Initialize portrait engine with image and geographic bbox
bounds = (27.10, 38.40, 27.20, 38.50)  # (min_lon, min_lat, max_lon, max_lat)
portrait = mfc.UrbanPortrait("face.jpg", bounds)

# 2. Fetch OpenStreetMap road network for bbox
geojson_data = mfc.fetch_osm_network(bounds)

# 3. Apply optical portrait styling with Cyberpunk preset
styled_geojson = portrait.process_geojson(geojson_data, palette="Cyberpunk 2077")

# 4. Export standalone vector SVG poster
mfc.export_svg(styled_geojson, "portrait.svg", preset="Cyberpunk 2077")</code></pre>
        </div>

        <!-- Card 2 -->
        <div class="card-border p-6 rounded-2xl space-y-4 font-mono text-xs">
          <div class="flex justify-between items-center text-slate-400">
            <span class="font-bold text-cyan-400 uppercase">Halftone &amp; Vector Stippling</span>
            <span>example_stipple.py</span>
          </div>
          <pre class="bg-slate-950 p-4 rounded-xl text-slate-300 overflow-x-auto border border-slate-800"><code>import myface2city as mfc
from PIL import Image

# 1. Load image and define sampling function
img = Image.open("face.jpg").convert("L")
w, h = img.size
pixels = img.load()

def sample_fn(u: float, v: float) -> float:
    return float(pixels[int(u * (w - 1)), int(v * (h - 1))])

# 2. Generate 80x80 variable-radius engraving dot grid
points = mfc.calculate_stipple_points(
    0.0, 0.0, 100.0, 100.0,
    grid_cols=80, grid_rows=80,
    sample_fn=sample_fn,
    max_radius=4.5,
    preset="Ink Portrait"
)

# 3. Export to GeoJSON and SVG
stipple_geojson = mfc.stipple_to_geojson(points)
mfc.export_svg(stipple_geojson, "stipple.svg", preset="Ink Portrait")</code></pre>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 bg-slate-950 py-8 text-center text-sm text-slate-500">
    <p>MyFace2City is created and maintained by <a href="https://github.com/YusufEminoglu" target="_blank" class="text-pink-400 hover:underline">Yusuf Eminoğlu</a>. Licensed under the MIT License.</p>
  </footer>

  <!-- Live In-Browser Generative Studio Script -->
  <script>
    let currentMode = 'network';
    let currentFace = 'portrait1';
    let customImageLoaded = false;
    let customCanvas = null;

    const PRESET_COLORS = {
      "Cyberpunk 2077": { bg: "#060814", colors: ["#060814", "#7000ff", "#ff0055", "#00f0ff", "#ffe600"], widths: [3.2, 2.4, 1.6, 0.9, 0.3] },
      "Ink Portrait": { bg: "#f5f1e8", colors: ["#090b10", "#20242d", "#4d535f", "#a8adb5", "#e7e9ec"], widths: [2.8, 2.0, 1.3, 0.7, 0.2] },
      "Blueprint": { bg: "#082f49", colors: ["#effcff", "#a7e8f2", "#58c9da", "#2389a1", "#155064"], widths: [2.6, 1.9, 1.3, 0.7, 0.2] },
      "Vintage Engraving": { bg: "#f6eee3", colors: ["#2c1d11", "#4a3525", "#70533d", "#a48366", "#d8c5b0"], widths: [2.8, 2.0, 1.3, 0.7, 0.2] },
      "Neon Night": { bg: "#050816", colors: ["#ff477e", "#7b2cff", "#00c2ff", "#5eead4", "#c8fff4"], widths: [3.0, 2.2, 1.5, 0.8, 0.3] },
      "Emerald Eco-Map": { bg: "#030f0b", colors: ["#061c14", "#0f3d2e", "#1e6b52", "#3fa882", "#7be3bc"], widths: [2.8, 2.0, 1.4, 0.7, 0.2] },
      "Sepia Blocks": { bg: "#f1e3c6", colors: ["#2c1810", "#5b3424", "#8f5f3e", "#c69b6d", "#ead7b7"], widths: [2.8, 2.0, 1.4, 0.7, 0.2] },
      "Nordic Slate": { bg: "#f1f5f9", colors: ["#12171c", "#242d38", "#414f5e", "#7a8a9e", "#cbd5e1"], widths: [2.6, 1.9, 1.3, 0.7, 0.2] },
      "Thermal Heatmap": { bg: "#050414", colors: ["#0a0826", "#4d006e", "#a8184c", "#f36410", "#f9f871"], widths: [3.0, 2.2, 1.5, 0.8, 0.3] },
      "Negative City": { bg: "#07071a", colors: ["#f7f7ff", "#c7d2fe", "#818cf8", "#4338ca", "#111133"], widths: [2.8, 2.0, 1.4, 0.7, 0.2] }
    };

    function setStudioMode(mode) {
      currentMode = mode;
      document.getElementById('btnModeNetwork').className = mode === 'network' ? 'px-4 py-1.5 rounded-lg text-xs font-bold bg-pink-600 text-white shadow-md shadow-pink-500/20' : 'px-4 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700';
      document.getElementById('btnModeStipple').className = mode === 'stipple' ? 'px-4 py-1.5 rounded-lg text-xs font-bold bg-pink-600 text-white shadow-md shadow-pink-500/20' : 'px-4 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700';
      updateArtRender();
    }

    function loadSampleFace(name) {
      currentFace = name;
      customImageLoaded = false;
      updateArtRender();
    }

    // Handle Custom Image Upload
    document.getElementById('imageUpload').addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
          customCanvas = document.createElement('canvas');
          customCanvas.width = 120;
          customCanvas.height = 120;
          const ctx = customCanvas.getContext('2d');
          ctx.drawImage(img, 0, 0, 120, 120);
          customImageLoaded = true;
          updateArtRender();
        };
        img.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });

    // Synthetic Face Luminance Evaluator
    function getLuminanceAt(u, v) {
      if (customImageLoaded && customCanvas) {
        const ctx = customCanvas.getContext('2d');
        const px = Math.min(119, Math.max(0, Math.floor(u * 120)));
        const py = Math.min(119, Math.max(0, Math.floor(v * 120)));
        const data = ctx.getImageData(px, py, 1, 1).data;
        return 0.299 * data[0] + 0.587 * data[1] + 0.114 * data[2];
      }

      // Procedural Artistic Face Form
      const cx = 0.5, cy = 0.48;
      const dx = (u - cx) / 0.32;
      const dy = (v - cy) / 0.42;
      const headDist = Math.sqrt(dx * dx + dy * dy);

      if (headDist > 1.0) {
        return 245; // Background highlight
      }

      // Eyes
      const eyeL = Math.hypot((u - 0.38) / 0.08, (v - 0.42) / 0.05);
      const eyeR = Math.hypot((u - 0.62) / 0.08, (v - 0.42) / 0.05);
      if (eyeL < 0.8 || eyeR < 0.8) return 15; // Deep pupil

      // Eyebrows
      if (Math.abs(v - 0.35) < 0.03 && (Math.abs(u - 0.38) < 0.11 || Math.abs(u - 0.62) < 0.11)) return 30;

      // Nose Bridge & Tip
      if (Math.abs(u - 0.5) < 0.04 && v > 0.42 && v < 0.60) return 40;
      if (Math.hypot((u - 0.5) / 0.06, (v - 0.60) / 0.04) < 1.0) return 25;

      // Mouth / Lips
      if (Math.hypot((u - 0.5) / 0.14, (v - 0.72) / 0.04) < 1.0) return 35;

      // Jaw and Cheek Shading
      const cheekShadow = Math.sin(u * Math.PI) * Math.cos(v * Math.PI);
      return Math.max(20, Math.min(230, 200 - cheekShadow * 160 + headDist * 60));
    }

    function updateArtRender() {
      const presetName = document.getElementById('presetSelect').value;
      const palette = PRESET_COLORS[presetName] || PRESET_COLORS["Cyberpunk 2077"];
      const density = parseInt(document.getElementById('sliderDensity').value);
      const gamma = parseFloat(document.getElementById('sliderGamma').value);
      const invert = document.getElementById('chkInvert').checked;

      const size = 560;
      const margin = 20;
      const drawSize = size - 2 * margin;
      const step = drawSize / density;

      let svgContent = `<svg id="activeSvg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="100%" height="100%">`;
      svgContent += `<rect width="${size}" height="${size}" fill="${palette.bg}" />`;
      svgContent += `<g id="artwork">`;

      let featureCount = 0;

      if (currentMode === 'network') {
        // Render Urban Grid Network (Roads & Building Footprints)
        for (let i = 0; i <= density; i++) {
          const y = margin + i * step;
          const v = i / density;

          // Horizontal Road Segments
          for (let j = 0; j < density; j++) {
            const x1 = margin + j * step;
            const x2 = x1 + step;
            const u = (j + 0.5) / density;

            let luma = getLuminanceAt(u, v);
            if (invert) luma = 255 - luma;
            let norm = luma / 255.0;
            if (gamma !== 1.0) norm = Math.pow(norm, 1.0 / gamma);

            const toneBin = Math.min(4, Math.max(0, Math.floor(norm * 5)));
            const color = palette.colors[toneBin];
            const width = palette.widths[toneBin];

            svgContent += `<line x1="${x1.toFixed(1)}" y1="${y.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${color}" stroke-width="${width}" stroke-linecap="round" />`;
            featureCount++;
          }
        }

        // Vertical Road Segments
        for (let j = 0; j <= density; j++) {
          const x = margin + j * step;
          const u = j / density;

          for (let i = 0; i < density; i++) {
            const y1 = margin + i * step;
            const y2 = y1 + step;
            const v = (i + 0.5) / density;

            let luma = getLuminanceAt(u, v);
            if (invert) luma = 255 - luma;
            let norm = luma / 255.0;
            if (gamma !== 1.0) norm = Math.pow(norm, 1.0 / gamma);

            const toneBin = Math.min(4, Math.max(0, Math.floor(norm * 5)));
            const color = palette.colors[toneBin];
            const width = palette.widths[toneBin];

            svgContent += `<line x1="${x.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${color}" stroke-width="${width}" stroke-linecap="round" />`;
            featureCount++;
          }
        }

        // Building Footprints inside grid cells
        for (let i = 0; i < density; i++) {
          for (let j = 0; j < density; j++) {
            const u = (j + 0.5) / density;
            const v = (i + 0.5) / density;

            let luma = getLuminanceAt(u, v);
            if (invert) luma = 255 - luma;
            let norm = luma / 255.0;
            if (gamma !== 1.0) norm = Math.pow(norm, 1.0 / gamma);

            const toneBin = Math.min(4, Math.max(0, Math.floor(norm * 5)));
            const color = palette.colors[toneBin];

            if (toneBin <= 2) { // Only render building footprints in shadows and midtones
              const bx = margin + j * step + step * 0.25;
              const by = margin + i * step + step * 0.25;
              const bw = step * 0.5;
              const bh = step * 0.5;
              svgContent += `<rect x="${bx.toFixed(1)}" y="${by.toFixed(1)}" width="${bw.toFixed(1)}" height="${bh.toFixed(1)}" fill="${color}" opacity="0.4" />`;
              featureCount++;
            }
          }
        }
      } else {
        // Halftone Vector Stippling Mode (Variable Radius Dots)
        const maxRadius = (step / 2.0) * 0.95;
        for (let i = 0; i < density; i++) {
          const v = i / (density - 1);
          const y = margin + i * step;

          for (let j = 0; j < density; j++) {
            const u = j / (density - 1);
            const x = margin + j * step;

            let luma = getLuminanceAt(u, v);
            if (invert) luma = 255 - luma;
            let intensity = 1.0 - (luma / 255.0);
            if (gamma !== 1.0 && intensity > 0.0) intensity = Math.pow(intensity, gamma);

            const r = maxRadius * intensity;
            if (r < 0.4) continue;

            const toneBin = Math.min(4, Math.max(0, Math.floor((luma / 255.0) * 5)));
            const color = palette.colors[toneBin];

            svgContent += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(2)}" fill="${color}" />`;
            featureCount++;
          }
        }
      }

      svgContent += `</g></svg>`;
      document.getElementById('svgContainer').innerHTML = svgContent;
      document.getElementById('canvasStats').innerText = `Features: ${featureCount.toLocaleString()} | Preset: ${presetName} | Grid: ${density}x${density}`;
    }

    function downloadSvgArtwork() {
      const svgEl = document.getElementById('activeSvg');
      if (!svgEl) return;
      const svgData = new XMLSerializer().serializeToString(svgEl);
      const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `myface2city_artwork_${Date.now()}.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    // Initial render on load
    window.addEventListener('DOMContentLoaded', () => {
      updateArtRender();
    });
  </script>
</body>
</html>
"""


def main() -> None:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    index_file = docs_dir / "index.html"
    index_file.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"Generated complete interactive studio docs at: {index_file.resolve()}")


if __name__ == "__main__":
    main()
