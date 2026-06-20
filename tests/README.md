# Tests

## Strategy
Unit tests on pipeline logic (transform, aggregation). Integration test for Socrata fetch (can be skipped offline). No tests on generated site/ output.

## Coverage target
Aim for >80% on core logic. All public interfaces in transform.py must have at least one test.

## Running
```bash
python3 -m pytest tests/ -v
```

## What to test
- All aggregation and transformation functions in transform.py
- Edge cases: days with zero complaints, neighbourhoods missing from dataset, null lat/lon values
- JSON output schema validation (does generate.py produce files matching the expected contract?)
- Any function that touches the Socrata API (mock the HTTP call)
