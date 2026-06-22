# Trishula-AestheticFilter

A sovereign, zero-dependency Python utility for auditing, scoring, and calibrating prose and codebase syntax to enforce linguistic clarity and front-end design standards.

It acts as the **fourth and final pillar** (Calibrates) of the **Trishula Workspace** sovereign tooling suite, replacing the global `stop-slop` and `taste-skill` check routines with a single local utility.

---

## Features

### 1. Linguistic Engine (`stop-slop` compliance)
Audits markdown and prose files for:
* **AI Writing Tells & Fillers**: Throat-clearing openers, meta-announcements, performative emphasis, and sweeps of false authority.
* **Jargon & Adverbs**: Automatically flags marketing/business jargon and removes `-ly` adverbs to keep style active and direct.
* **Structural Weaknesses**: Identifies binary contrast crutches, negative listing patterns, Socratic posturing, and passive voice.
* **Rhythm Auditing**: Enforces sentence starter variance and flags banned em-dashes (`—`).

### 2. Visual Engine (`taste-skill` compliance)
Audits CSS, HTML, JS/TS, and React codebases for:
* **LLM Default Tells**: Centered hero components, default Inter font imports, and excessive cards.
* **Palette Clichés**: Flags the AI-purple/indigo gradient and the overused DTC craft (cream/brass/espresso) color pairings.
* **Accessibility & Layout**: Enforces `prefers-reduced-motion` media checks for animations and limits wide-tracking uppercase eyebrows to a maximum of 1 per 3 sections.
* **UX Safety**: Detects duplicate CTA button intent (e.g. having both "Get in touch" and "Contact us" on the same page).

---

## Installation & Requirements
* Runs on **standard library Python 3.10+**.
* Zero external pip dependencies.

---

## Usage

### Scan a File or Directory
Run a diagnostic audit to list violations and calculate a score out of 100:
```bash
python trishula_aesthetic_filter.py scan path/to/file_or_directory
```

### Apply Safe Corrections
Automatically clean simple tells (such as stripping common filler words, throat-clearing starters, and replacing em-dashes):
```bash
python trishula_aesthetic_filter.py fix path/to/file_or_directory
```

---

## Verification
Run unit tests to verify rules:
```bash
python test_trishula_aesthetic_filter.py
```
