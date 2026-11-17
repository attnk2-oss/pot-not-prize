#!/usr/bin/env python3
"""make.fun ai-judge-rich-01 entry.

The entry is one short plan. It lives beside this file as plan.txt and is
written to entry.txt byte for byte, because the judge reads exactly the bytes
that land in /output/entry.txt and nothing else.

The grader runs `python3 -P -s /bot/main.py` with /bot read-only and a working
directory of its own, so the plan is found from __file__ and never from the
cwd, and the output goes to /output or to MAKEFUN_OUTPUT_DIR when that is set.
"""

import hashlib
import os
import sys

MAX_PLAN_CHARS = 1000

PLAN_NAME = "plan.txt"
ENTRY_NAME = "entry.txt"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def plan_path():
    """Return the absolute path of plan.txt, anchored on this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, PLAN_NAME)


def output_dir():
    """Return the directory the entry is written to."""
    return os.environ.get(OUTPUT_ENV) or DEFAULT_OUTPUT_DIR


def check_plan(plan):
    """Refuse a plan the gate would reject, before writing anything.

    The gate counts Unicode code points, not bytes, so the length test decodes
    first: a plan of 1,000 accented characters is 1,000 code points and up to
    2,000 bytes, and only the code points are counted. It also needs at least
    one character that is not white space.
    """
    try:
        text = plan.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("plan.txt is not UTF-8: %s" % exc)
    if not text.strip():
        raise SystemExit("plan.txt is empty or only white space")
    if not 1 <= len(text) <= MAX_PLAN_CHARS:
        raise SystemExit(
            "plan.txt is %d code points, the gate takes 1 to %d"
            % (len(text), MAX_PLAN_CHARS)
        )
    return text


def report(plan, written):
    """Write the plan's size and digest to stderr, so two runs can be compared.

    Nothing here touches entry.txt: it is the record a run leaves behind. Two
    runs of this file must write the same bytes, and the digest is how that is
    checked from outside without diffing the file.
    """
    text = plan.decode("utf-8")
    sys.stderr.write(
        "entry.txt %d bytes, %d code points, %d lines, sha256 %s\n"
        % (
            len(plan),
            len(text),
            text.count("\n") + 1,
            hashlib.sha256(plan).hexdigest(),
        )
    )


def main():
    with open(plan_path(), "rb") as handle:
        plan = handle.read()
    check_plan(plan)

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    written = os.path.join(out_dir, ENTRY_NAME)
    with open(written, "wb") as handle:
        handle.write(plan)

    with open(written, "rb") as handle:
        if handle.read() != plan:
            raise SystemExit("entry.txt does not match plan.txt on read back")
    report(plan, written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
