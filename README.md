Extremely simple HTML file to display any Surfline cam efficiently. Using water.css and bootstrap libraries for styling and structure. Also using video.js for a better/more effective display of the stream. It offers more customization, too. 

Ways to use: 
- Download template file and open it locally in any browser.
- Use an online HTML viewer like https://html.onlineviewer.net/ by simply copying over all the template code
- Host your own server for free.  

To change the spot: 
- Change source line (24) from https://cams.cdn-surfline.com/cdn-wc/wc-lowers/playlist.m3u8. Use cdn-ec for east coast, etc and change the following field for spots. For spot names that are not listed below, go to their site and use inspect element on the cam previews to get the formal spot name. Or just open the preview image in a new tab.
- If you want to update the "poster" or cover photo: Change poster line (23): us-west-2/wc-lowers

[WC] List of spot names

hi-pipelineov

wc-lowers

wc-pleasureptov

wc-blacks

wc-oldmansanonofre

wc-thepointsanonofre

wc-church

wc-upperstrestles

wc-sanclementesb

wc-tstreet

wc-scpiernorth

wc-dohenysb

wc-strands

wc-saltcreekpoint

wc-alisocreekbeach

wc-malibufirstpt

wc-malibuclose

wc-malibusurfrider

wc-venturapoint

wc-venturapointnorth

wc-venturapointov

[EC] List of spot names

ec-pointjudith

ec-narragansett

ec-secondbeachsurfers

ec-secondbeachpav

ec-eastons

ec-matunuck

ec-misquamicut

ec-goodharbor

ec-nahant

ec-seabrooknh

ec-hampton

[INT] List of spot names

id-uluwatu

id-uluwatufront

id-uluwatucloseup

za-supertubes

## Southeastern NC cams added ✅

Added a small dataset and view for Southeastern North Carolina cams:

- Wrightsville Beach (Wrightsville Beach Pier) — Wilmington
- Carolina Beach (Boardwalk)
- Kure Beach (Pier)
- Atlantic Beach (Fort Macon)
- Surf City (Topsail Island)
- Morehead City (shore / harbor)
- Oak Island (pier)

Files added:

- `data/cameras.json` — list of camera metadata (id, name, lat/lon, provider, website_url, embed_url)
- `cams.html` — simple static UI to browse cams and open provider pages or play inline when `embed_url` is set

How to use:

1. Open `cams.html` (serve the folder with a static server to avoid file:// CORS issues, e.g. `python3 -m http.server 8000`)  
2. Edit `data/cameras.json` and set `embed_url` to a playable stream (m3u8 or iframe) to enable inline playback.
3. Check Surfchex for local cam pages (e.g., Wrightsville: <https://surfchex.com/wrightsville-beach/>, Carolina Beach: <https://surfchex.com/carolina-beach/>) — many cams appear with embedded players there.

To-do:

- Replace placeholder `embed_url` fields with real stream URLs.
- Optionally integrate this into a FastAPI/LLM pipeline for metadata enrichment, OCR, or automated archiving.

New: Local API + tracing ✅

- Run the FastAPI dev server: `make serve` (requires packages in `server/requirements.txt`)
- Endpoints:
  - `GET /api/cameras` — returns `data/cameras.json`
  - `GET /health` — basic health check
- Tracing: OpenTelemetry is configured with the Console exporter for local development. To send traces to OTLP/Jaeger, set the appropriate environment variables and exporter.

CI: A basic GitHub Actions workflow runs tests on push/PR to `main`.
