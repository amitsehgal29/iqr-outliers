"""iqr-outliers: flag numeric outliers in CSV columns using the IQR (Tukey fence) rule."""
import argparse, csv, json, statistics, sys

def fences(values, k=1.5):
    q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

def scan(path, cols, k=1.5):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for c in cols:
        vals = []
        for i, r in enumerate(rows, start=2):  # line 1 is the header
            try:
                vals.append((i, float(r[c])))
            except (KeyError, TypeError, ValueError):
                continue
        if len(vals) < 4:
            out[c] = {"skipped": "fewer than 4 numeric values"}
            continue
        lo, hi = fences([v for _, v in vals], k)
        out[c] = {"low": round(lo, 4), "high": round(hi, 4),
                  "outliers": [{"line": i, "value": v} for i, v in vals if v < lo or v > hi]}
    return out

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv"); p.add_argument("--cols", required=True, help="comma-separated numeric columns")
    p.add_argument("-k", type=float, default=1.5, help="fence multiplier (3 = extreme only)")
    a = p.parse_args(argv)
    rep = scan(a.csv, a.cols.split(","), a.k)
    print(json.dumps(rep, indent=2))
    return 1 if any(r.get("outliers") for r in rep.values()) else 0

if __name__ == "__main__":
    sys.exit(main())
