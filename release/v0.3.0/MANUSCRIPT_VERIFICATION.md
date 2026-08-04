# Manuscript build and PDF verification

- Status: `PASS`
- Date: `2026-08-04`
- TeX source: `paper/ssuf_fixed_gadget_scenario_cover_synopsis.tex`
- Publication PDF: `paper/ssuf_fixed_gadget_scenario_cover_synopsis.pdf`
- Pages: `12`
- Standard locked-toolchain build return code: `0`
- Cache-only locked-toolchain build return code: `0`
- Rendered pages: `12`
- Byte-identical standard and cache-only rebuilds: `True`
- Byte-identical to the supplied prepublication RC1 PDF: `False` (expected;
  the final author, date, release-status, and rights text changed)
- Visual inspection of every rendered page: `PASS`
- Overfull boxes reported: `0`
- Synopsis PDF SHA-256: `d165339ed4fa34cbe0f7e614778f96fd0a5e5f2bfcad54adfee7e785e6ba3165`
- Tectonic: `0.16.9`
- Locked bundle content SHA-256: `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`

All three checked repository manuscripts rebuilt byte-identically in standard
and cache-only modes. The synopsis passed its source/PDF text preflight and
Poppler media-box geometry check. Full-resolution inspection of all 12 final
pages found no clipping, overlap, missing glyph, or other visible layout
defect. Build logs are retained in the private publication handoff; temporary
inspection renders were discarded after review.
