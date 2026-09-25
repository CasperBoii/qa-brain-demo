"""Run a deterministic example using only the committed synthetic fixture."""
from pathlib import Path
from src.distill import distill, split_parts

ROOT = Path(__file__).resolve().parent

def main():
    days, rejected = distill((ROOT / 'fixtures/session.jsonl').read_text().splitlines())
    print('# QA Brain — synthetic capture demo\n')
    for day, text in days.items():
        print(f'## Distilled conversation: {day}\n')
        for part in split_parts(text):
            print(part + '\n')
    print(f'Rejected malformed records: {rejected}\n')
    print('## Retrieve a reusable lesson\n')
    query = 'session isolation'
    # A transparent local keyword lookup, not GBrain or semantic search.
    terms = query.lower().split()
    for page in sorted((ROOT / 'vault').rglob('*.md')):
        content = page.read_text()
        if all(term in content.lower() for term in terms):
            print(f'Query: {query}')
            print(f'Citation: {page.relative_to(ROOT).as_posix()}')
            print('Status: synthetic-example; review before applying to real work.')
    print('\nCapture is automated; promotion into a trusted lesson requires review. No LLM or external service was called.')

if __name__ == '__main__':
    main()
