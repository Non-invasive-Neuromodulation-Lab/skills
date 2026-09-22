#!/usr/bin/env python3
"""
check_sibling_consistency.py — baseline-free sibling-copy & shared/ drift checker
for the ARS skills repository (academic-paper / academic-paper-reviewer /
academic-pipeline / deep-research).

Two invariants, both computable WITHOUT any baseline manifest:

  Rule 1 (nested sibling copies). This repository keeps git-tracked NESTED copies
  of files from one skill tree inside another skill tree:
      <tree>/<other-skill>/<rest>   must be byte-identical to the canonical
      <other-skill>/<rest>          at the repository root.
  (Self-nesting counts: academic-paper/academic-paper/<rest> mirrors
  academic-paper/<rest>.) A nested copy whose canonical file is MISSING is an
  ORPHAN — an error, because the copy set is then not self-describing. A
  canonical file with no nested copy is fine: not every file is copied.

  Rule 2 (shared/ x4). Every skill tree carries its own REAL copy of shared/
  (separate inodes, not junctions). The four copies must have identical path
  sets and identical bytes per path.

Usage:
    python scripts/check_sibling_consistency.py [--root <repo-root>]

Exit 0 = consistent; exit 1 = drift reported on stdout. Stdlib only; no writes.
Introduced with the Tool Paper route hardening (v3.4.1); see
academic-paper/docs/tool-paper-route.md and the Phase 3/4 working records for
the duplication topology this script guards.
"""

import argparse
import hashlib
import os
import sys

SKILLS = ["academic-paper", "academic-paper-reviewer", "academic-pipeline", "deep-research"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_files(top):
    for dp, _dns, fns in os.walk(top):
        if ".git" in dp.split(os.sep):
            continue
        for fn in fns:
            p = os.path.join(dp, fn)
            yield p, os.path.relpath(p, top).replace("\\", "/")


def main():
    default_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    ap = argparse.ArgumentParser(description="Sibling-copy & shared/ consistency checker")
    ap.add_argument("--root", default=default_root, help="repository root (default: parent of this script)")
    args = ap.parse_args()
    root = args.root

    for s in SKILLS:
        if not os.path.isdir(os.path.join(root, s)):
            print(f"FATAL: expected skill tree missing: {os.path.join(root, s)}")
            sys.exit(2)

    errors = []
    pairs_checked = 0
    files_scanned = 0

    # Rule 1: nested sibling copies must equal their canonical file
    for tree in SKILLS:
        tdir = os.path.join(root, tree)
        for other in SKILLS:
            nested = os.path.join(tdir, other)
            if not os.path.isdir(nested):
                continue
            for p, rel in walk_files(nested):
                files_scanned += 1
                # rel is relative to <tree>/<other>; canonical lives at root/<other>/<rest>
                canonical = os.path.join(root, other, rel)
                trel = f"{tree}/{other}/{rel}"
                if not os.path.isfile(canonical):
                    errors.append(f"ORPHAN nested copy (no canonical file): {trel}")
                    continue
                pairs_checked += 1
                if sha(p) != sha(canonical):
                    errors.append(f"DIVERGED nested copy: {trel} != {rel} (canonical)")

    # Rule 2: shared/ identical across the four trees (academic-paper is the reference)
    ref_dir = os.path.join(root, "academic-paper", "shared")
    ref = {rel: sha(p) for p, rel in walk_files(ref_dir)}
    files_scanned += len(ref)
    shared_compared = 0
    for tree in SKILLS[1:]:
        sdir = os.path.join(root, tree, "shared")
        cur = {rel: sha(p) for p, rel in walk_files(sdir)}
        files_scanned += len(cur)
        for rel, h in cur.items():
            if rel not in ref:
                errors.append(f"shared/ EXTRA file (absent from academic-paper/shared): {tree}/shared/{rel}")
                continue
            shared_compared += 1
            if ref[rel] != h:
                errors.append(f"shared/ DIVERGED: {tree}/shared/{rel} != academic-paper/shared/{rel}")
        for rel in ref:
            if rel not in cur:
                errors.append(f"shared/ MISSING copy: {tree}/shared/{rel} (present in academic-paper/shared)")

    print("=== sibling-copy & shared/ consistency check ===")
    print(f"  files scanned: {files_scanned}")
    print(f"  nested-copy pairs compared against canonical: {pairs_checked}")
    print(f"  shared/ files compared across trees: {shared_compared} (+ path-set checks)")
    if errors:
        print(f"\nFAILURES ({len(errors)}):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("\nALL CHECKS PASSED: nested sibling copies match canonicals; shared/ identical across 4 trees.")


if __name__ == "__main__":
    main()
