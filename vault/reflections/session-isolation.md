---
title: Keep authentication state separate for each test role
type: reflection
created: 2026-01-15
status: synthetic-example
tags: [automation, authentication, session-isolation]
---

## What

In this fictional example, two browser contexts reused the same saved authentication state. An account-switching test therefore exercised the wrong role.

## Evidence

- Synthetic transcript: `fixtures/session.jsonl`, 2026-01-15.
- This page is a hand-written demo fixture, not a captured production finding or model-generated conclusion.

## How to apply

Use separate authentication state for each role. Verify the signed-in identity before checking permissions. Do not assume a new browser tab creates an independent session.

## Limits

The example demonstrates how to record a lesson. It does not establish the cause of a failure in any real product.
