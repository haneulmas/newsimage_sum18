# newsimage_sum18

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/haneulmas/newsimage_sum18/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/haneulmas/newsimage_sum18/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One illustrated news atlas for **Wednesday 18 November 2026**. Three leads cover the Shenzhen greetings, Iran's widening Gulf attacks, and Voyager 1's first light-day from Earth. Eight illustrated cards and sixteen short briefs extend the regional and subject coverage. A date-check strip separates earlier events and later scheduled developments.

<img src="assets/entry.png" width="1024" height="1024" alt="Wednesday 18 November 2026: Trump meets Xi and Putin in Shenzhen; Iran widens Gulf attacks; Voyager 1 reaches one light-day. Eight illustrated secondary stories, sixteen short briefs, a dot map and a date-check strip follow.">

## Run offline

The contest runtime is **Python 3.13, standard library only**:

```sh
python main.py
```

`main.py` creates `/output` if it is missing and copies the exact bytes of `assets/entry.png` to `/output/entry.png`. It does not render or install dependencies. It performs no network access, clock reads, randomness, or metadata generation. The asset is resolved relative to the script, so execution does not depend on the working directory.

For a local output folder in PowerShell:

```powershell
$env:MAKEFUN_OUTPUT_DIR = Join-Path $PWD 'local-output'
python main.py
Remove-Item Env:MAKEFUN_OUTPUT_DIR
```

An unset or empty `MAKEFUN_OUTPUT_DIR` selects `/output`.

## Rebuild and verify

Image development uses Pillow **11.1.0**, pinned in `tools/requirements.txt`. Pillow is needed only to rebuild the committed asset; it is not imported by the entrypoint.

```sh
python tools/build_image.py
python tools/verify.py
```

The renderer loads only bundled Inter and Nunito fonts and draws original rectangles, polygons, circles, lines and generic silhouettes at 2048 × 2048. It downsamples to 1024 × 1024 with Lanczos, then maps to a fixed 256-entry palette without dithering. The deterministic encoder writes only IHDR, PLTE, IDAT and IEND chunks. It does not embed timestamps, text, profiles or EXIF.

The verifier runs the entry twice in different, initially missing output folders using isolated Python and an audit hook denying network and subprocess activity inside the entry. Both outputs must equal the asset byte for byte. It checks dimensions, file size, palette references, scanline data, chunk order and CRCs. Temporary test outputs are removed automatically. The development target is below 400,000 bytes; the contest limit is 1,048,576 bytes.

## Editorial selection

| Level | Contents |
| --- | --- |
| Three leads | Trump, Xi and Putin in Shenzhen; Iran's attacks involving Kuwait and Bahrain; Voyager 1's one-light-day milestone. |
| Eight cards | Fed minutes; proposed EU Ukraine loan; Russian refinery disruptions; COP31; Prabowo at APEC; Cyclone Akvan; Amnesty's Sudan report; Anthropic IPO pricing. |
| Sixteen briefs | US congressional nomination, Gaza, Venezuela, Brazil, UK inflation, North Korea, Myanmar, Ethiopia/Eritrea, Yemen, South African health care, Vatican, Ecuador, Manila, Indonesian blue carbon, Canadian diplomacy, and ADNOC's vessel report. |
| Date check | Nvidia results and Qeshm strike: 17 Nov. Trilateral outcomes and Akvan landfall: still future on Wednesday. |

[The source ledger](tools/SOURCES.md) provides dates, original reports and qualifications for every item. Proposals are not approvals; forecasts are not observed outcomes. The refinery estimate is cumulative and attributed to sources. The Amnesty card is explicitly a new report about earlier civilian deaths. ADNOC's Wednesday statement explicitly concerns a 17 November attack. GTA VI's sale launch and the Ecuador fishermen's lawsuit were excluded as unconfirmed or already reported before Wednesday.

## Three reading sizes

The composition is an editorial atlas, with equal illustrated lead panels and narrower secondary columns. Its visual motif is the repeated regional color rule, which links labels, pictograms and map dots. Warm paper avoids a glaring background; navy provides the main text contrast. The colors distinguish Asia, Middle East, Europe, Americas, Space, Markets, Africa and climate/health. The map uses broad schematic silhouettes rather than administrative borders.

- **300 px:** the date and three lead headlines carry the main reading. Both date lines use 84 px Inter Bold with measured 61 px cap height. The one-line date caption uses 25 px; lead headlines use 44 px.
- **512 px:** all eight card headlines use 22 px, no more than seven words each, beside separate pictograms. Source-qualified support lines remain secondary.
- **1024 px:** sixteen briefs use 12.5 px, beside the dot map and date-check strip. The builder checks every text box against its column and against other text boxes. Main panels and columns use 12–16 px gutters.

No photos, real faces, textures, gradients, shadows or glows are used. The IPO illustration is a certificate and price tag, not a chart implying a trading gain. All illustrations are symbolic rather than reconstructions of particular incidents.

## Files

```text
main.py                 Standard-library entrypoint
assets/entry.png        The single contest PNG
assets/fonts/           Three fonts and their OFL notices
tools/build_image.py    Offline renderer and deterministic PNG encoder
tools/pictograms.py     Eleven original flat vector illustrations
tools/verify.py         PNG and isolated-runtime checks
tools/requirements.txt  Development-only Pillow version
tools/SOURCES.md        Dated reporting references
tools/VERIFICATION.md   Measured results and visual review
README.md
LICENSE
```

## Repository and transcripts

The public repository was created on **19 November 2026 at 00:17:51 UTC**, after the competition opened on **18 November 2026 at 00:00:00 UTC**. Its root LICENSE is MIT. Fonts retain their separate SIL OFL 1.1 licenses; see [font provenance](assets/fonts/README.md).

Native Codex logs are kept outside the public repository by the agent host. The original build, Python revision, and this later illustration revision began after the competition opened. Bundle the complete contributing parent and subagent families after the work finishes. Do not reconstruct transcripts from memory or include the archive in Git; `.gitignore` excludes transcript archives. A bundle from before this illustration revision does not cover the new work.

Local verification is not a published judge result and does not promise a reward or ranking. This README does not claim that this revision has been pushed, uploaded or submitted.

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards
