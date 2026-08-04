# Manuscript Build

The checked PDFs are generated with Tectonic 0.16.9. The release path does not
fall back to another TeX engine. Poppler supplies PDF metadata, text, and
bounding-box checks.

```bash
python scripts/build_pdf.py
python scripts/build_pdf.py --only-cached
python verification/preflight_pdf_text.py
python verification/preflight_rb003_pdf_text.py
python verification/preflight_fixed_gadget_pdf_text.py
```

The fixed-gadget scenario-cover manuscript is an integrated technical synopsis
with companion proofs under `research/fixed_gadget_scenario_cover/`. Its PDF
build and layout checks do not independently verify every proof.

The toolchain lock is `verification/document-toolchain.json`. The first command
may populate Tectonic's cache from the locked v33 bundle URL; the second command
proves that the complete build works with network access disabled at the TeX
resource layer.
