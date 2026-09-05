From the repository root in PowerShell, activate the existing project environment
before running `pytest`:

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

Alternatively, run without activation:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

If you are already inside the nested `linear-algebra-calculator` directory,
use `..\.venv\Scripts\Activate.ps1` or `..\.venv\Scripts\python.exe -m pytest`.

To install test dependencies, run these commands from `linear-algebra-calculator`
with your Python environment activated:

```powershell
python -m pip install -r tests/requirements.txt
pytest
```

The repository's `pytest.ini` sets test discovery and the application import
path, so `pytest` also works from the repository root. Use `pytest -q` for
compact output or `pytest tests/numeric_test.py` from `linear-algebra-calculator`
to run a single file. `python -m pytest` works too.

The optional pytest cache plugin is disabled in `pytest.ini` to avoid Windows
permission errors writing `.pytest_cache`. Tests still run normally, but cache
features such as `--lf` (rerun last failures) are unavailable.

Measure statement and branch coverage across the application:

```powershell
python -B -m coverage run --branch --source=app -m pytest -p no:cacheprovider -q
python -m coverage report -m
python -m coverage html
```

Open `htmlcov/index.html` to inspect uncovered lines and branches. Application
event-loop startup is not exercised by this suite. No application modules are
excluded from the coverage command.

Tests cover math results and error cases, decomposition identities, step
snapshots, history isolation, parsing and formatting, calculation dispatch,
widgets, and the current window's history, clipboard, and import/export flows.
Qt tests run offscreen without opening windows; dialogs are replaced in tests
and file operations use pytest temporary directories. PySide6 is required, and
missing UI dependencies fail collection instead of silently skipping coverage.

Temporary test files use a fresh folder under `tests/.pytest_tmp/` for each run.
This avoids permission errors from the shared Windows `pytest-of-angel` folder
and keeps concurrent runs separate. These ignored folders are retained for
debugging. An explicit `pytest --basetemp=...` overrides this default.
