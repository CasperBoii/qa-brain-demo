# QA Brain — Portfolio Demo

**Pornpavit Tantilavasute · QA Engineer**

A small example of the knowledge workflow I created for AI-assisted QA: capture a useful lesson, retain its evidence, and make it discoverable before the next task.

The original QA Brain is a Markdown vault and workflow built **on GBrain**. I created the QA integration and operating rules; I did not create the GBrain engine. This repository demonstrates selected parts locally with synthetic data.

## Start here — two minutes

1. Read the [sample output](docs/demo-output.md).
2. Open the [example lesson](vault/reflections/session-isolation.md).
3. Review the [capture code](src/distill.py), [tests](tests/test_distill.py), and [scope notes](docs/scope.md).

## Run locally

Requires Python 3.10 or later; tested with Python 3.14. Uses only the standard library. No API key, model, account, package installation, or GBrain server is needed.

```sh
python3 demo.py
python3 -m unittest discover -s tests -v
```

To export the committed fixture into a **new** directory:

```sh
python3 src/distill.py --input fixtures/session.jsonl --output output/example
```

The exporter refuses to overwrite an existing output directory. It never searches your home directory or automatically reads your agent sessions.

## What this demonstrates

| QA concern | Demonstrated approach |
| --- | --- |
| Repeated mistakes | Record a lesson with evidence and how to apply it |
| Noisy agent logs | Keep visible conversation text; omit tool payloads and reasoning blocks |
| Sensitive content | Mask selected credential patterns, then require review |
| Silent ingestion failure | Count rejected records and fail exports with no visible content |
| Unverifiable memory | Cite the original page and label synthetic examples explicitly |

## My contribution

I designed the QA knowledge structure, capture workflow, and rules for reusing verified lessons. The distillation example adapts selected concepts from my existing Python tool: extract relevant text, redact known credential shapes, group by date, and split large outputs. I use AI assistance for implementation and review.

This demo intentionally adds explicit input/output paths, rejects overwrites, omits reasoning blocks, and uses a small local keyword lookup. The sample lesson is **hand-written synthetic data**, not a claim that an LLM discovered it.

## Scope

There is no production vault, personal transcript, customer information, nightly job, live MCP connection, embedding model, or semantic search in this sample. The keyword lookup illustrates citation-based reuse only. Pattern-based redaction is incomplete by nature; it is not a universal secret or PII detector.

## Related work

- [QA Platform demo](https://github.com/CasperBoii/qa-platform-demo)
- [QA automation framework](https://github.com/CasperBoii/qa-automation-framework)

Private portfolio sample. Repository access is required to view the code and linked examples.
