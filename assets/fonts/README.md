# Bundled typefaces

`tools/build_image.py` loads these three local, static TrueType fonts. It does
not look up system fonts or request fonts over the network. The files are
unmodified upstream binaries without variable-font axes.

| File | Family | Weight and style | Development use |
| --- | --- | --- | --- |
| `Inter-Regular.ttf` | Inter | 400, regular | Supporting lines and source footer |
| `Inter-Bold.ttf` | Inter | 700, regular | Weekday and section labels |
| `LibreCaslonText-Bold.ttf` | Libre Caslon Text | 700, regular | Date, masthead and broadsheet headlines |

Inter comes from the [official 4.1 release archive](https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip),
under `extras/ttf/`. Its internal version string is
`Version 4.001;git-9221beed3`. The license is included as `Inter-OFL.txt`.

Libre Caslon Text comes from the [upstream static-font directory](https://github.com/thundernixon/Libre-Caslon/tree/master/fonts/static).
Its internal version is `2.000`. The license is included as
`LibreCaslonText-OFL.txt`.

Both families use the SIL Open Font License 1.1, separately from the repository's
own MIT license. The contest entry point, `main.py`, copies the finished image
and does not load these fonts or any rendering library.

## SHA-256 of bundled binaries

```text
40d692fce188e4471e2b3cba937be967878f631ad3ebbbdcd587687c7ebe0c82  Inter-Regular.ttf
288316099b1e0a47a4716d159098005eef7c0066921f34e3200393dbdb01947f  Inter-Bold.ttf
1e36d897da5db786d2e59e9d4ef968913742764878a5dd83acb12789e1d64dd5  LibreCaslonText-Bold.ttf
```
