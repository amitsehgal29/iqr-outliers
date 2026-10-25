# iqr-outliers

Flag suspicious numeric values (a 500 among tens, a negative price) in CSV columns using the IQR rule, with the exact line number of each one.

Pure Python stdlib. Non-numeric and empty cells are skipped.

```bash
python iqr_outliers.py orders.csv --cols amount,quantity
python iqr_outliers.py orders.csv --cols amount -k 3   # extreme outliers only
```

Prints the fences and the outliers per column; exits `1` if any are found.

```bash
python -m unittest -v
```
