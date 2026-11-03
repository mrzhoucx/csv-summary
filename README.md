# csv-summary

Summarize a CSV file at a glance: row count, columns, and per-column stats.
Zero dependencies, Python 3.8+.

- Numeric columns: min, max, mean, missing count, distinct count
- Text columns: most common values, missing count, distinct count
- Missing cells are counted, never silently ignored

## Usage

```bash
python3 csv_summary.py data.csv
python3 csv_summary.py data.csv --json
python3 csv_summary.py data.csv --top 5
```

## Example

Using the included `example.csv`:

```text
$ python3 csv_summary.py example.csv
example.csv: 5 rows, 4 columns
  name (text, missing=0, distinct=5): most common: alice x1, bob x1, carol x1
  age (number, missing=1, distinct=3): min=25.0 max=41.0 mean=31.5
  city (text, missing=0, distinct=3): most common: Shanghai x3, Beijing x1, Guangzhou x1
  score (number, missing=1, distinct=4): min=79.5 max=95.0 mean=88.75
```

## Options

| Flag | Meaning |
| --- | --- |
| `--json` | Print the summary as JSON instead of text |
| `--top N` | Show N most-common values for text columns (default: 3) |
