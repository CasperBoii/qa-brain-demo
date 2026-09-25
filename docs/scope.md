# Scope and operating model

## Capture is not verification

The original workflow separates a captured observation from a reusable lesson. Before trusting a page, check its evidence, status, and applicability. A memory store does not replace an issue tracker or a test result system.

The demonstration follows four steps:

1. Read the explicitly selected synthetic JSONL fixture.
2. Extract visible user/assistant text, redact selected credential patterns, and group by date.
3. Show a hand-written reflection with What, Evidence, How to apply, and Limits.
4. Find that reflection using a simple local keyword query and return its path as a citation.

Step 3 is intentionally manual. No automated reasoning, model call, or semantic retrieval is implied.

## Source relationship

The distillation implementation is an adapted, standalone example of the original Python transcript tool. It retains extraction/redaction/date grouping/chunking concepts, but does not copy machine-specific paths or the production synchronization process.

Changes for the demo include explicit input/output arguments, fail-on-existing-output behavior, date validation, strict bounds for long lines, and exclusion of tool/reasoning blocks. These demo changes are not claims about behavior deployed in the original system.

The synthetic fixture and reflection were written for this portfolio. The included tests demonstrate the sample's behavior, not the reliability of the entire original knowledge system.

## What remains private

Real lessons, real conversations, service configuration, credentials, internal source identifiers, sync schedules, operational logs, and original Git history are not included. Nothing installs a hook or starts, stops, or modifies a background service.
