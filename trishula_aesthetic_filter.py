#!/usr/bin/env python3
"""
trishula_aesthetic_filter.py
Trishula Sports Intelligence — Aesthetic & Linguistic Calibrator

Complete fourth pillar of the Trishula Workspace. Audits prose and frontend
codebases for AI tells, filler, design clichés, and styling violations.
Runs locally on standard library Python 3.10+ with zero external dependencies.
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Enforce UTF-8 console output for Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() in ('cp1252', 'cp850', 'ascii'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Linguistic Patterns (Stop-Slop Rules) ────────────────────────────────────

# Adverbs ending in -ly, excluding common non-adverbs
LY_PATTERN = re.compile(r"\b\w+ly\b", re.IGNORECASE)
EXCLUDED_LY = {
    "only", "family", "early", "likely", "daily", "friendly", "lovely",
    "holy", "silly", "ugly", "jolly", "lonely", "apply", "reply", "comply",
    "multiply", "fly", "rely", "ally", "bully", "monopoly", "supply"
}

BANNED_ADVERBS = {
    "really", "just", "literally", "genuinely", "honestly", "simply",
    "actually", "deeply", "truly", "fundamentally", "inherently",
    "inevitably", "interestingly", "importantly", "crucially"
}

THROAT_CLEARING = [
    "here's the thing:", "here's what ", "here's this ", "here's that ",
    "here's why ", "the uncomfortable truth is", "it turns out",
    "the real ", "let me be clear", "the truth is,", "i'll say it again:",
    "i'm going to be honest", "can we talk about", "here's what i find interesting",
    "here's the problem though"
]

EMPHASIS_CRUTCHES = [
    "full stop.", "let that sink in.", "this matters because",
    "make no mistake", "here's why that matters"
]

BUSINESS_JARGON = [
    r"\bnavigate\b", r"\bunpack\b", r"\blean into\b", r"\blandscape\b",
    r"\bgame-changer\b", r"\bdouble down\b", r"\bdeep dive\b",
    r"\btake a step back\b", r"\bmoving forward\b", r"\bcircle back\b",
    r"\bon the same page\b"
]

META_COMMENTARY = [
    r"\bhint:\b", r"\bplot twist:\b", r"\bspoiler:\b",
    "you already know this, but", "but that's another post",
    "feature, not a bug", "dressed up as", "the rest of this essay",
    "let me walk you through", "in this section, we'll", "as we'll see",
    "i want to explore"
]

PERFORMATIVE_EMPHASIS = [
    "creeps in", "i promise", "they exist, i promise", "actually matters"
]

VAGUE_DECLARATIVES = [
    "the reasons are structural", "the implications are significant",
    "this is the deepest problem", "the stakes are high",
    "the consequences are real"
]

# Structural patterns (binary contrasts, negative listing, etc.)
STRUCT_PATTERNS = {
    "binary_contrast_1": re.compile(r"\b(not|isn't|is not)\b.*?\b(but|it's|is|because)\b", re.IGNORECASE),
    "binary_contrast_2": re.compile(r"\bnot\s+because\b.*?\b(because|but)\b", re.IGNORECASE),
    "binary_contrast_3": re.compile(r"\bisn't\s+the\s+problem\b.*?\bis\b", re.IGNORECASE),
    "binary_contrast_4": re.compile(r"\b(the\s+answer\s+isn't|question\s+isn't)\b.*?\b(it's|is)\b", re.IGNORECASE),
    "negative_listing_1": re.compile(r"\bnot\s+a\s+\w+.*?\bnot\s+a\s+\w+\b", re.IGNORECASE),
    "negative_listing_2": re.compile(r"\bit\s+wasn't\s+\w+.*?\bit\s+wasn't\s+\w+\b", re.IGNORECASE),
    "dramatic_fragment": re.compile(r"\b[a-z0-9]+\.\s+that's\s+it\b", re.IGNORECASE),
    "rhetorical_posturing": re.compile(r"\b(what\s+if|think\s+about\s+it:|here's\s+what\s+i\s+mean:)\b", re.IGNORECASE)
}

# ── Visual Patterns (Taste-Skill Rules) ──────────────────────────────────────

AI_PURPLE_GLOW = re.compile(r"\b(from|to|via)-(purple|indigo|violet|fuchsia|pink)\b", re.IGNORECASE)

DTC_BG = {"#f5f1ea", "#f7f5f1", "#fbf8f1", "#efeae0", "#ece6db", "#faf7f1", "#e8dfcb"}
DTC_ACC = {"#b08947", "#b6553a", "#9a2436", "#9c6e2a", "#bc7c3a", "#7d5621"}
DTC_TXT = {"#1a1714", "#1a1814", "#1b1814"}

INTER_FONT = re.compile(r"\binter\b", re.IGNORECASE)
CENTERED_HERO = re.compile(r"\b(text-center\b.*?\bhero|hero\b.*?\btext-center)\b", re.IGNORECASE)

GSAP_ANIMATION = re.compile(r"\bgsap\b|ScrollTrigger\.create", re.IGNORECASE)
REDUCED_MOTION = re.compile(r"prefers-reduced-motion|useReducedMotion", re.IGNORECASE)

EYEBROW_FREQUENCY = re.compile(r"\b(tracking-\[0\.\d+em\]|uppercase|font-mono)\b", re.IGNORECASE)

# CTA Intent synonyms
CTA_CONTACT = {"contact", "get in touch", "let's talk", "start a project", "reach out"}
CTA_SIGNUP = {"signup", "sign up", "get started", "try free", "try for free"}

# ── Diagnostic Engine ─────────────────────────────────────────────────────────

class Violation:
    def __init__(self, line_num, text, rule, message, score_deduction):
        self.line_num = line_num
        self.text = text
        self.rule = rule
        self.message = message
        self.score_deduction = score_deduction

def scan_file(filepath: Path) -> dict:
    results = {
        "filepath": filepath,
        "type": "unknown",
        "violations": [],
        "linguistic_score": 50,
        "visual_score": 50,
        "total_lines": 0
    }
    
    ext = filepath.suffix.lower()
    if ext in [".md", ".txt"]:
        results["type"] = "prose"
    elif ext in [".css", ".scss"]:
        results["type"] = "style"
    elif ext in [".js", ".jsx", ".ts", ".tsx", ".html"]:
        results["type"] = "code"
    else:
        results["type"] = "prose"

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return results

    results["total_lines"] = len(lines)
    content_lower = "".join(lines).lower()

    # ── Linguistic Scanning (all file types, primary focus on prose) ────────
    for idx, line in enumerate(lines):
        line_num = idx + 1
        line_lower = line.lower()

        # 1. Banned adverbs (Stop-Slop)
        for adv in BANNED_ADVERBS:
            if adv in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "adverb",
                    f"Banned AI adverb tell: '{adv}'", 2
                ))

        # 2. General adverbs ending in -ly
        ly_matches = LY_PATTERN.findall(line_lower)
        for match in ly_matches:
            if match not in EXCLUDED_LY and match not in BANNED_ADVERBS:
                results["violations"].append(Violation(
                    line_num, line.strip(), "adverb",
                    f"Adverb detected: '{match}'. Prefer active verb-driven description.", 1
                ))

        # 3. Throat-clearing
        for tc in THROAT_CLEARING:
            if tc in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "throat-clearing",
                    f"Filler opener: '{tc}'", 3
                ))

        # 4. Emphasis crutches
        for crutch in EMPHASIS_CRUTCHES:
            if crutch in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "crutch",
                    f"Performative emphasis crutch: '{crutch}'", 2
                ))

        # 5. Jargon
        for jg in BUSINESS_JARGON:
            if re.search(jg, line_lower):
                results["violations"].append(Violation(
                    line_num, line.strip(), "jargon",
                    f"Business/marketing jargon tell: '{jg.replace(r'\\b', '')}'", 2
                ))

        # 6. Meta-commentary
        for meta in META_COMMENTARY:
            if meta in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "meta-commentary",
                    f"Meta-announcement/throat-clearing: '{meta}'", 3
                ))

        # 7. Performative intensity
        for perf in PERFORMATIVE_EMPHASIS:
            if perf in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "performative",
                    f"Manufactured sincerity tell: '{perf}'", 2
                ))

        # 8. Vague declaratives
        for vague in VAGUE_DECLARATIVES:
            if vague in line_lower:
                results["violations"].append(Violation(
                    line_num, line.strip(), "vague",
                    f"Vague announcement without specific detail: '{vague}'", 3
                ))

        # 9. Wh- starters (at sentence level inside lines)
        if results["type"] == "prose":
            stripped = line.strip()
            if stripped.startswith(("What ", "When ", "Where ", "Which ", "Who ", "Why ", "How ")):
                results["violations"].append(Violation(
                    line_num, stripped, "sentence-starter",
                    "Wh- sentence opener crutch. Lead with the subject or verb.", 1
                ))
            if stripped.startswith("So "):
                results["violations"].append(Violation(
                    line_num, stripped, "sentence-starter",
                    "Paragraph/sentence starts with 'So '. Start directly with content.", 1
                ))
            if stripped.startswith("Look,"):
                results["violations"].append(Violation(
                    line_num, stripped, "sentence-starter",
                    "Throat-clearing opener 'Look,'. Remove.", 2
                ))

        # 10. Em-dashes
        if "—" in line or "--" in line:
            if results["type"] == "prose" or ext in [".md", ".txt"]:
                results["violations"].append(Violation(
                    line_num, line.strip(), "rhythm",
                    "Banned em-dash usage. Stop-Slop requires commas or periods.", 2
                ))

        # 11. Passive voice heuristics (simple matches)
        if results["type"] == "prose" and re.search(r"\b(is|was|were|been|be)\s+\w+ed\b", line_lower):
            results["violations"].append(Violation(
                line_num, line.strip(), "passive-voice",
                "Potential passive voice construction detected.", 2
            ))

    # 12. Structural patterns (binary contrast / rhetorical setups)
    for rule_name, pattern in STRUCT_PATTERNS.items():
        matches = pattern.finditer(content_lower)
        for m in matches:
            char_pos = m.start()
            line_num = content_lower[:char_pos].count("\n") + 1
            results["violations"].append(Violation(
                line_num, m.group().strip().replace("\n", " "), f"structure-{rule_name}",
                f"Formulaic/binary contrast structural tell: '{rule_name}'", 3
            ))

    # ── Visual Scanning (only code/style files) ──────────────────────────────
    if results["type"] in ["code", "style"]:
        # 1. AI-purple gradient check
        purple_matches = AI_PURPLE_GLOW.findall(content_lower)
        if purple_matches:
            for idx, line in enumerate(lines):
                if AI_PURPLE_GLOW.search(line):
                    results["violations"].append(Violation(
                        idx+1, line.strip(), "visual-lila",
                        "AI Lila Purple/Indigo gradient tell detected.", 4
                    ))

        # 2. DTC craft palette checks
        has_bg = any(bg in content_lower for bg in DTC_BG)
        has_acc = any(acc in content_lower for acc in DTC_ACC)
        has_txt = any(txt in content_lower for txt in DTC_TXT)
        if has_bg and has_acc and has_txt:
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-dtc-palette",
                "Overused DTC Craft/Beige/Brass palette combination detected (banned default).", 5
            ))

        # 3. Overused Inter font tell
        if INTER_FONT.search(content_lower):
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-font",
                "Discouraged default font choice (Inter). Select Outfit, Cabinet Grotesk, or Satoshi instead.", 2
            ))

        # 4. Centered hero tells
        if CENTERED_HERO.search(content_lower):
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-layout",
                "Centered hero text alignment tell (anti-center bias rule).", 3
            ))

        # 5. GSAP without reduced motion query check
        if GSAP_ANIMATION.search(content_lower) and not REDUCED_MOTION.search(content_lower):
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-a11y-motion",
                "Animations present without reduced-motion query checks (Accessibility Fail).", 5
            ))

        # 6. Eyebrow limit check
        eyebrow_count = len(EYEBROW_FREQUENCY.findall(content_lower))
        if eyebrow_count > 4:
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-layout-eyebrows",
                f"Excessive uppercase wide-tracking eyebrow elements ({eyebrow_count} found). Max 1 per 3 sections.", 3
            ))

        # 7. Duplicate CTA Intent check
        btn_labels = []
        button_pattern = re.compile(r"<button[^>]*>(.*?)</button>|label=[\"'](.*?)[\"']|cta=[\"'](.*?)[\"']", re.IGNORECASE)
        for line in lines:
            matches = button_pattern.findall(line)
            for m in matches:
                lbl = next((g for g in m if g), "").strip().lower()
                if lbl:
                    btn_labels.append(lbl)
        
        contact_ct = sum(1 for l in btn_labels if any(syn in l for syn in CTA_CONTACT))
        signup_ct = sum(1 for l in btn_labels if any(syn in l for syn in CTA_SIGNUP))
        if contact_ct > 1 or signup_ct > 1:
            results["violations"].append(Violation(
                1, "[Entire File Scope]", "visual-duplicate-cta",
                f"Duplicate CTA intent detected (CTAs: {btn_labels}). Keep exactly one label per intent.", 3
            ))

    ling_deduct = sum(v.score_deduction for v in results["violations"] if not v.rule.startswith("visual"))
    vis_deduct = sum(v.score_deduction for v in results["violations"] if v.rule.startswith("visual"))
    
    results["linguistic_score"] = max(0, 50 - ling_deduct)
    results["visual_score"] = max(0, 50 - vis_deduct)

    return results

# ── Fixer Logic ───────────────────────────────────────────────────────────────

def fix_content(filepath: Path) -> int:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file for fixes: {e}")
        return 0

    fixed_count = 0
    original = content

    if "—" in content:
        content = content.replace("—", ", ")
        fixed_count += 1
    if "--" in content and filepath.suffix.lower() in [".md", ".txt"]:
        content = content.replace("--", ", ")
        fixed_count += 1

    throat_replaces = {
        r"(?i)\bHere's the thing:\s*": "",
        r"(?i)\bLet me be clear,\s*": "",
        r"(?i)\bLet me be clear:\s*": "",
        r"(?i)\bThe truth is,\s*": "",
        r"(?i)\bI'll say it again:\s*": "",
        r"(?i)\bI'm going to be honest,\s*": "",
        r"(?i)\bLook,\s*": ""
    }
    for pat, rep in throat_replaces.items():
        modified, count = re.subn(pat, rep, content)
        if count > 0:
            content = modified
            fixed_count += count

    filler_words = ["really", "literally", "genuinely", "honestly", "simply"]
    for word in filler_words:
        modified, count = re.subn(rf"\b{word}\s+", "", content, flags=re.IGNORECASE)
        if count > 0:
            content = modified
            fixed_count += count

    if content != original:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[FIXED] Applied {fixed_count} safe corrections to: {filepath.name}")
        except Exception as e:
            print(f"Error writing fixes: {e}")
            return 0
    else:
        print(f"[CLEAN] No simple fixes needed for: {filepath.name}")

    return fixed_count

# ── Main Entry ────────────────────────────────────────────────────────────────

def print_scorecard(res: dict):
    print("=" * 70)
    print(f"🔱 TRISHULA AESTHETIC AUDIT SCORECARD")
    print(f"File: {res['filepath'].name} ({res['type'].upper()})")
    print("=" * 70)
    
    violations = res["violations"]
    if not violations:
        print("\n✨ Clean! No linguistic or visual design violations detected.")
    else:
        print(f"\nFound {len(violations)} stylistic violations:")
        print("-" * 70)
        for v in violations:
            print(f"  Line {v.line_num:<4} | [{v.rule:<15}] {v.message}")
            if v.text and len(v.text) < 120:
                print(f"            > \"{v.text}\"")
                
    print("-" * 70)
    total_score = res["linguistic_score"] + res["visual_score"]
    print(f"Linguistic Score : {res['linguistic_score']}/50")
    print(f"Visual Score      : {res['visual_score']}/50")
    print(f"TOTAL SCORE       : {total_score}/100")
    print("=" * 70)
    
    if total_score < 70:
        print("🔱 VERDICT: WEAKNESSES DETECTED. Calibrate code or text output.")
    else:
        print("🔱 VERDICT: AESTHETIC PASSED. Sovereign standards met.")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Trishula Workspace Aesthetic & Linguistic Filter")
    parser.add_argument("action", choices=["scan", "fix"], help="Audit or calibrate file")
    parser.add_argument("path", help="Path to file or directory to process")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    if not target_path.exists():
        print(f"[ERROR] Path does not exist: {target_path}")
        sys.exit(1)

    targets = []
    if target_path.is_file():
        targets.append(target_path)
    else:
        for root, _, files in os.walk(target_path):
            for file in files:
                p = Path(root) / file
                if p.suffix.lower() in [".md", ".txt", ".css", ".js", ".jsx", ".ts", ".tsx", ".html"]:
                    if "pycache" not in str(p) and "logs" not in str(p) and "backups" not in str(p):
                        targets.append(p)

    if not targets:
        print("[-] No scan targets found.")
        sys.exit(0)

    if args.action == "scan":
        for t in targets:
            res = scan_file(t)
            print_scorecard(res)
    elif args.action == "fix":
        total_fixes = 0
        for t in targets:
            total_fixes += fix_content(t)
        print(f"\n[COMPLETE] Applied total of {total_fixes} corrections across files.")

if __name__ == "__main__":
    main()
