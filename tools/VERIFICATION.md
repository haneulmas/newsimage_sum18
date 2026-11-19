# Verification: illustrated news atlas

Verified locally on 19 November 2026. This is a local engineering and editorial check, not a new contest ranking or reward claim.

## Output and runtime

| Requirement | Result and evidence |
| --- | --- |
| One image at the output contract | PASS: main.py creates the selected directory and writes exactly entry.png; default directory is /output. |
| Python 3.13 entrypoint | PASS: tested with official portable CPython 3.13.0, using only the standard library. |
| PNG size and dimensions | PASS: 1024 × 1024 indexed PNG, 114,092 bytes, below 400,000 bytes and the 1 MiB contest limit. |
| Determinism | PASS: two isolated runs in different initially missing directories equal each other and assets/entry.png byte for byte. |
| No runtime network | PASS: runtime imports are restricted to os/pathlib/shutil; both isolated runs use an audit hook denying socket, urllib, subprocess and shell activity. Zero forbidden operations. |
| No metadata | PASS: only IHDR, PLTE, IDAT, IEND; CRCs, zlib stream, scanlines and palette references validated. No text, EXIF, time or color-profile chunks. |
| Offline renderer | PASS: local Pillow 11.1.0, bundled Inter/Nunito, flat geometry at 2048 × 2048; Lanczos downsampling and fixed palette. No network in renderer or pictograms. |
| License and repository | PASS: root MIT license, bundled font OFL notices. GitHub API reports public repository created 19 Nov 2026 00:17:51 UTC, after opening 18 Nov 00:00 UTC. |
| Session window | PASS: this contributing native Codex family began 19 Nov 2026, after the opening. Native logs remain with the host for transcript bundling. |

SHA-256 of the asset and both runtime outputs:

```text
94df872e8fc0b1f306ef6477f6065002313201b5d1c13a1c7b6ea752dcccb66b
```

## Content and visual review

| Requirement | Result and evidence |
| --- | --- |
| Explicit edition date | PASS: WEDNESDAY and 18 NOVEMBER 2026 use 84 px Inter Bold, measured cap height 61 px. The exact requested one-line date caption is present at 25 px. |
| Three leads at 300 px | PASS: visually inspected the final PNG at 300 px; Trump/Xi/Putin, widening Gulf attacks and Voyager's light-day headline remain readable in separate color panels. Every lead has a flat pictogram and 44 px headline. |
| Eight cards at 512 px | PASS: visually inspected all eight headlines and their distinct pictograms at 512 px. Headlines use 22 px and no more than seven words; icons and text occupy separate columns. |
| Full-size detail | PASS: inspected at 1024 px. Sixteen one-line briefs use 12.5 px, with a schematic dot map, region legend and date-check strip. The builder checks 91 text boxes for column overflow and pairwise text collisions. |
| Regional structure | PASS: fixed Asia/Middle East/Europe/Americas/Space/Markets/Africa/climate colors are shared by labels, icons and map dots. Palette retains the exact base colors. |
| Faithful wording | PASS: source ledger has eleven main-story rows and sixteen brief rows. Loan remains proposed; rate hikes are expectations; IPO is pricing with trading scheduled 19 Nov; cyclone landfall remains a forecast. |
| Reports about earlier events | PASS: Sudan is labelled NEW REPORT with earlier civilian deaths; Russian refineries are cumulative November disruption attributed to sources; ADNOC line explicitly says 17 Nov attack reported on the edition date. |
| Date exclusions | PASS: Nvidia results and Qeshm strike identified as 17 Nov or earlier. Trilateral results and cyclone landfall are marked future on Wednesday. GTA VI sale launch and the already-announced Ecuador lawsuit omitted. |
| Original flat art | PASS: eleven code-drawn pictograms, no photos, likenesses, textures, gradients, shadows, glow or invented price plots. IPO symbol is a certificate/price tag; Gulf symbol is a shelter and drone alert. |
| Clean composition | PASS: no text overflow or detected text collisions; main panels/columns use 12 px gutters and lead-to-card break 16 px. Date, hierarchy and regional coding carry the thumbnail reading. |

Development previews were written outside the repository, inspected, then removed. The verifier removes its own temporary outputs. No temporary render folder or unused font remains in the repository. Existing transcript archives are preserved outside Git through .gitignore.

## Commands

```sh
python -B tools/build_image.py
python3.13 -I -S -B tools/verify.py
```

The renderer was regenerated twice and the SHA-256 compared; the runtime verifier was executed using the official portable Python 3.13 interpreter. A current transcript archive must include this illustration revision before submission; the earlier 23-session bundle alone does not.
