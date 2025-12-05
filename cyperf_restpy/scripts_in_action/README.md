# Sample Scripts

## How to Run test1.py

To avoid import issues, always run this script as a module from the project root:

```bash
cd /Users/ashwjosh/Desktop/cyperf_restpy
python -m cyperf_restpy.sample_scripts.test1
```

This ensures that Python treats `cyperf_restpy` as a package and resolves imports correctly.

### Alternative (not recommended)
You can also run directly if you set the `PYTHONPATH`:

```bash
export PYTHONPATH=/Users/ashwjosh/Desktop/cyperf_restpy
python cyperf_restpy/sample_scripts/test1.py
```

But the first method is preferred for all package-based Python projects. 