"""Portfolio adaptation of a QA transcript-distillation workflow. Standard library only."""
import argparse
from datetime import date
import json
from pathlib import Path
import re

# Pattern-based defense in depth, not a guarantee of complete secret or PII removal.
TOKEN = re.compile(r'(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,}|xox[abprs]-[A-Za-z0-9-]{10,})')
ASSIGNMENT = re.compile(r'\b([A-Za-z_]*(?:KEY|TOKEN|SECRET|PASSWORD))\s*[:=]\s*(?:"[^"\n]*"|\x27[^\x27\n]*\x27|[^\s,;]+)', re.IGNORECASE)
BEARER = re.compile(r'\bBearer\s+\S+', re.IGNORECASE)


def redact(text):
    """Mask selected credential shapes; always review outputs before sharing."""
    text = TOKEN.sub('<redacted>', text)
    text = ASSIGNMENT.sub(lambda m: m.group(1) + '=<redacted>', text)
    return BEARER.sub('Bearer <redacted>', text)


def parts(record):
    """Retain visible conversation text; omit tool payloads and reasoning blocks."""
    if not isinstance(record, dict) or record.get('isMeta'):
        return
    message = record.get('message')
    if not isinstance(message, dict) or message.get('role') not in ('user', 'assistant'):
        return
    content = message.get('content')
    if isinstance(content, str):
        if not content.startswith('<local-command-caveat>'):
            yield f"[{message['role']}] {content}"
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text' and isinstance(block.get('text'), str):
                yield f"[{message['role']}] {block['text']}"


def split_parts(text, max_chars=2000):
    """Prefer line boundaries, while still bounding unusually long single lines."""
    if max_chars < 1:
        raise ValueError('max_chars must be positive')
    remaining = text
    while len(remaining) > max_chars:
        cut = remaining.rfind('\n', 0, max_chars + 1)
        if cut <= 0:
            cut = max_chars
        yield remaining[:cut]
        remaining = remaining[cut:].lstrip('\n')
    if remaining:
        yield remaining


def distill(lines):
    """Group valid dated records. Report rejected lines instead of hiding them."""
    days = {}
    rejected = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError('not an object')
            stamp = record.get('timestamp')
            if not isinstance(stamp, str) or not re.match(r'^\d{4}-\d{2}-\d{2}(?:T|$)', stamp):
                raise ValueError('invalid date')
            day = date.fromisoformat(stamp[:10]).isoformat()
            visible = list(parts(record))
        except (ValueError, TypeError):
            rejected += 1
            continue
        if visible:
            days.setdefault(day, []).extend(visible)
    return {day: redact('\n'.join(text)) for day, text in sorted(days.items())}, rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='A new directory; existing output is never overwritten')
    args = parser.parse_args()
    days, rejected = distill(args.input.read_text(encoding='utf-8').splitlines())
    if not days:
        raise SystemExit('No visible dated content found. No output created.')
    args.output.mkdir(parents=True, exist_ok=False)
    count = 0
    for day, text in days.items():
        for index, part in enumerate(split_parts(text), 1):
            (args.output / f'{day}-p{index}.txt').write_text(part + '\n', encoding='utf-8')
            count += 1
    print(f'Wrote {count} file(s); rejected {rejected} malformed record(s). Review outputs before sharing.')


if __name__ == '__main__':
    main()
