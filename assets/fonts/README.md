# Bundled typefaces

`tools/build_image.py` loads these three bundled TrueType fonts. It never looks
up system fonts or requests them over the network. Nunito is a variable font;
the renderer explicitly selects weight 750 for its rounded labels.

| File | Family | Weight and style | Development use |
| --- | --- | --- | --- |
| `Inter-Regular.ttf` | Inter | 400, regular | Supporting lines and short briefs |
| `Inter-Bold.ttf` | Inter | 700, regular | Date and all story headlines |
| `Nunito.ttf` | Nunito | Variable, weight 750 selected | Rounded region labels and map title |

Inter comes from the [official 4.1 release archive](https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip),
under `extras/ttf/`. Its internal version string is
`Version 4.001;git-9221beed3`. The license is included as `Inter-OFL.txt`.

Nunito comes from the [official Google Fonts repository](https://github.com/google/fonts/tree/main/ofl/nunito),
file `Nunito[wght].ttf`, stored without modification as `Nunito.ttf`.
Its SIL OFL 1.1 license is included as `Nunito-OFL.txt`.

Both families use the SIL Open Font License 1.1, separately from the repository's
own MIT license. The contest entry point, `main.py`, copies the finished image
and does not load these fonts or any rendering library.

## SHA-256 of bundled binaries

```text
40d692fce188e4471e2b3cba937be967878f631ad3ebbbdcd587687c7ebe0c82  Inter-Regular.ttf
288316099b1e0a47a4716d159098005eef7c0066921f34e3200393dbdb01947f  Inter-Bold.ttf
bb55a5ca5c2042335b3991af27c4d0705d0ef41cac6164ac737fd8f2a1e85207  Nunito.ttf
```
