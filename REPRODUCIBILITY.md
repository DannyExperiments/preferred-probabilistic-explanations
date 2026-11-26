# Reproducibility

Run from the repository root using Python 3.9 or newer. The exact replay uses the Python standard library.

```sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
```

Compare the replay output with [the checked log](verification/logs/replay.txt). See the [PDF build](paper/BUILD.md) and [visualization guide](visualization/README.md) for optional rebuilds. Open the offline explorer on a local browser with JavaScript. Its comparisons use exact counts of equal-mass points.
