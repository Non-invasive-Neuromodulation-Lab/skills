#!/usr/bin/env python3
"""Deterministic reference list validator for skill testing.

Usage:
  python check_references.py --file <path> --mode <basic|standard|strict>
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Dict
from urllib import request, error


REFERENCE_HEADINGS = (
    "references",
    "bibliography",
    "works cited",
)

YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")
URL_RE = re.compile(r"\bhttps?://\S+\b")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6}\s+.+|[A-Z][A-Za-z0-9\s]{2,40}:?)\s*$")


@dataclass
class Finding:
    entry_index: int
    severity: str
    code: str
    message: str


@dataclass
class Report:
    file: str
    mode: str
    entries: int
    errors: int
    warnings: int
    infos: int
    duplicates: int
    doi_checked: int
    doi_resolved: int
    doi_unresolved: int
    findings: List[Dict]


def detect_reference_block(lines: List[str]) -> Tuple[int, int]:
    start = -1
    for i, raw in enumerate(lines):
        line = raw.strip().lower()
        if any(h == line or line.startswith(h) for h in REFERENCE_HEADINGS):
            start = i + 1
            break
    if start < 0:
        return 0, len(lines)

    end = len(lines)
    for i in range(start, len(lines)):
        if HEADING_RE.match(lines[i]) and lines[i].strip().lower() not in REFERENCE_HEADINGS:
            end = i
            break
    return start, end


def extract_entries(lines: List[str]) -> List[str]:
    entries: List[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if len(line) < 12:
            continue
        if re.match(r"^\d+[.)]\s+", line):
            line = re.sub(r"^\d+[.)]\s+", "", line)
        if line.startswith("- ") or line.startswith("* "):
            line = line[2:].strip()
        entries.append(line)
    return entries


def normalize_entry(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def normalize_doi(doi: str) -> str:
    return doi.strip().rstrip(".,;)")


def verify_dois_online(dois: List[str], timeout_s: int = 4) -> Dict[str, str]:
    """Return DOI resolution status.

    Status values:
    - resolved
    - unresolved
    - unavailable (network or service issues)
    """
    out: Dict[str, str] = {}
    seen = set()

    for raw in dois:
        doi = normalize_doi(raw)
        if not doi or doi in seen:
            continue
        seen.add(doi)

        url = f"https://doi.org/{doi}"
        req = request.Request(
            url=url,
            method="GET",
            headers={"User-Agent": "reference-list-validity-checker/1.0"},
        )
        try:
            with request.urlopen(req, timeout=timeout_s) as resp:
                status = getattr(resp, "status", 200)
                if 200 <= int(status) < 400:
                    out[doi] = "resolved"
                else:
                    out[doi] = "unresolved"
        except error.HTTPError as exc:
            if 400 <= exc.code < 500:
                out[doi] = "unresolved"
            else:
                out[doi] = "unavailable"
        except Exception:
            out[doi] = "unavailable"

    return out


def check_entry(entry: str, idx: int, mode: str) -> List[Finding]:
    findings: List[Finding] = []

    year_match = YEAR_RE.search(entry)
    if not year_match:
        findings.append(Finding(idx, "error", "missing_year", "No publication year detected."))
        year_pos = -1
    else:
        year_pos = year_match.start()

    if year_pos <= 1:
        findings.append(Finding(idx, "warning", "author_segment_short", "Author-like segment before year looks too short."))

    if year_pos >= 0:
        before = entry[:year_pos].strip(" .,-;")
        after = entry[year_match.end():].strip(" .,-;") if year_match else ""
        if len(before.split()) < 1:
            findings.append(Finding(idx, "error", "missing_author_like", "No author-like text before year."))
        if len(after.split()) < 2:
            findings.append(Finding(idx, "warning", "weak_title_like", "Text after year may be incomplete."))

    if mode in ("standard", "strict"):
        has_doi_token = "doi" in entry.lower() or DOI_RE.search(entry)
        if has_doi_token and not DOI_RE.search(entry):
            findings.append(Finding(idx, "warning", "malformed_doi", "DOI token present but DOI format looks invalid."))

        for url in URL_RE.findall(entry):
            if not (url.startswith("http://") or url.startswith("https://")):
                findings.append(Finding(idx, "warning", "malformed_url", "URL found but scheme is invalid."))

    return findings


def strict_consistency_checks(entries: List[str]) -> List[Finding]:
    findings: List[Finding] = []
    if not entries:
        return findings

    year_positions = []
    for i, e in enumerate(entries, start=1):
        m = YEAR_RE.search(e)
        if m:
            year_positions.append(m.start() / max(1, len(e)))

    if year_positions:
        avg = sum(year_positions) / len(year_positions)
        far = [p for p in year_positions if abs(p - avg) > 0.35]
        if len(far) > max(1, int(0.3 * len(year_positions))):
            findings.append(Finding(0, "info", "year_position_inconsistent", "Year position appears inconsistent across entries."))

    # Check whether entries consistently use (YYYY) format.
    year_parenthesized = 0
    year_plain = 0
    for e in entries:
        if re.search(r"\((?:19\d{2}|20\d{2})\)", e):
            year_parenthesized += 1
        elif YEAR_RE.search(e):
            year_plain += 1
    mixed_year_style = min(year_parenthesized, year_plain)
    if mixed_year_style > max(1, int(0.3 * len(entries))):
        findings.append(Finding(0, "warning", "year_token_style_mixed", "Year token formatting appears mixed across entries."))

    # Check terminal punctuation consistency.
    ending_period = sum(1 for e in entries if e.strip().endswith("."))
    ending_no_period = len(entries) - ending_period
    mixed_punctuation = min(ending_period, ending_no_period)
    if mixed_punctuation > max(1, int(0.3 * len(entries))):
        findings.append(Finding(0, "info", "terminal_punctuation_mixed", "Entry-ending punctuation is inconsistent."))

    return findings


def build_report(path: Path, mode: str, doi_web_check: bool = False) -> Report:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start, end = detect_reference_block(lines)
    entries = extract_entries(lines[start:end])

    findings: List[Finding] = []
    doi_candidates: List[str] = []

    seen: Dict[str, int] = {}
    duplicates = 0
    for i, entry in enumerate(entries, start=1):
        findings.extend(check_entry(entry, i, mode))
        doi_candidates.extend(DOI_RE.findall(entry))
        key = normalize_entry(entry)
        if key in seen:
            duplicates += 1
            findings.append(Finding(i, "warning", "duplicate_entry", f"Possible duplicate of entry {seen[key]}."))
        else:
            seen[key] = i

    if mode == "strict":
        findings.extend(strict_consistency_checks(entries))

    doi_status: Dict[str, str] = {}
    if doi_web_check and mode in ("standard", "strict") and doi_candidates:
        doi_status = verify_dois_online(doi_candidates)
        for doi, status in doi_status.items():
            if status == "unresolved":
                findings.append(Finding(0, "warning", "doi_unresolved", f"DOI could not be resolved: {doi}"))
            elif status == "unavailable":
                findings.append(Finding(0, "info", "doi_verification_unavailable", f"DOI verification unavailable for: {doi}"))

    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    doi_checked = len(doi_status)
    doi_resolved = sum(1 for v in doi_status.values() if v == "resolved")
    doi_unresolved = sum(1 for v in doi_status.values() if v == "unresolved")

    return Report(
        file=str(path),
        mode=mode,
        entries=len(entries),
        errors=errors,
        warnings=warnings,
        infos=infos,
        duplicates=duplicates,
        doi_checked=doi_checked,
        doi_resolved=doi_resolved,
        doi_unresolved=doi_unresolved,
        findings=[asdict(f) for f in findings],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reference list validity checker")
    parser.add_argument("--file", required=True, help="Document path to validate")
    parser.add_argument("--mode", default="standard", choices=["basic", "standard", "strict"])
    parser.add_argument("--doi-web-check", action="store_true", help="Check DOI resolvability online via doi.org")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = Path(args.file)
    if not target.exists() or not target.is_file():
        print(json.dumps({"error": f"File not found: {target}"}, indent=2))
        return 2

    report = build_report(target, args.mode, doi_web_check=args.doi_web_check)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
        return 0

    print(f"File: {report.file}")
    print(f"Mode: {report.mode}")
    print(f"Entries: {report.entries}")
    print(f"Errors: {report.errors} | Warnings: {report.warnings} | Info: {report.infos} | Duplicates: {report.duplicates}")
    print(f"DOI checked: {report.doi_checked} | DOI resolved: {report.doi_resolved} | DOI unresolved: {report.doi_unresolved}")

    if report.findings:
        print("Findings:")
        for f in report.findings:
            prefix = f"[entry {f['entry_index']}]" if f["entry_index"] else "[global]"
            print(f"- {f['severity'].upper()} {prefix} {f['code']}: {f['message']}")
    else:
        print("Findings: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
