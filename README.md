# ⚜️ Trishula-AestheticFilter
> **Sovereign Linguistic Auditer & Visual Quality Calibrator**

A lightweight, zero-dependency, pure-Python quality-assurance engine built entirely within the Python standard library. It represents the **fourth and final pillar** (Calibrates) of the Trishula Workspace sovereign tooling suite, localizing and replacing the global `stop-slop` and `taste-skill` frameworks into a single local utility.

Designed to scan prose, markdown, HTML, CSS, and JS/TS codebases to calculate quality index scores and apply automatic stylistic fixes under zero-network, air-gapped constraints.

---

## █ Strategic Alignment & Features
* **Zero Dependencies**: Pure standard library implementation (`re`, `sys`, `pathlib`, `json`). Safe from supply-chain risks.
* **Linguistic Calibration (`stop-slop`)**:
  * **AI Tells**: Identifies throat-clearing openers, performative emphasis, false authority, and meta-announcements.
  * **Jargon & Adverbs**: Detects business/marketing clichés and flags excessive `-ly` adverbs to keep prose active.
  * **Structural Weakness Check**: Identifies binary contrast structures, Socratic question posturing, and passive voice.
  * **Typographic Hygiene**: Flags banned em-dashes (`--` or `—`), enforcing proper commas or periods.
* **Visual Verification (`taste-skill`)**:
  * **AI Layout Clichés**: Flags centered hero sections, generic Inter font default imports, and card grid layouts.
  * **Color Palette Auditing**: Detects overused AI color schemes (indigo/purple gradients, generic DTC cream/brass/espresso pairings).
  * **UX & Accessibility**: Verifies `prefers-reduced-motion` declarations for CSS transitions and blocks duplicate CTA buttons.

---

## █ Installation & Requirements
* **Runtime Environment**: Python 3.10, 3.11, or 3.12 (standard library).
* **Installation**: Drop `trishula_aesthetic_filter.py` directly into your project root.

---

## █ Usage Reference

### Audit a File or Directory
Run a diagnostic audit to list violations and calculate a quality score out of 100:
```bash
python trishula_aesthetic_filter.py scan path/to/target
```

### Apply Style Fixes In-Place
Automatically correct simple tells (throat-clearing phrases, filler words, em-dashes, sentence starts) in-place:
```bash
python trishula_aesthetic_filter.py fix path/to/target
```

---

## █ Proof of Work (Verified Console Output)

The calibrator has been verified against mock prose files containing stop-slop tells and visual CSS styles:

```
> python test_trishula_aesthetic_filter.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.028s

OK
[FIXED] Applied 5 safe corrections to: mock_fix.md
```

---

## █ CI/CD Integration
This repository is configured with a GitHub Actions workflow (`.github/workflows/ci.yml`) validating style parsing and corrections against Python versions `3.10`, `3.11`, and `3.12` on every push to the `main` branch.
