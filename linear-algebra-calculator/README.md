# Linear Algebra Calculator

A desktop matrix calculator made with Python and PySide6. Enter a matrix, pick an operation, and see the answer with calculation steps.

## Run it

From the repository root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\linear-algebra-calculator\requirements.txt
cd .\linear-algebra-calculator
..\.venv\Scripts\python.exe -m app.main
```

Already have `.venv`? Skip the first command. If it's activated, you can launch with `python -m app.main` from the inner `linear-algebra-calculator` folder.

Getting `No module named 'app'`? Make sure you're in the folder that contains `app`.

## What it can do

- Addition, subtraction, scalar and matrix multiplication, transpose
- Gaussian elimination and RREF
- Determinants and inverses
- Gram-Schmidt, LU, and QR decomposition
- Eigenvalues, eigenvectors, and diagonalization
- Import/export, clipboard copy/paste, and calculation history

## How to use it

1. Choose the rows and columns for Matrix A (up to 10 each).
2. Double-click cells to enter numbers. Use decimals like `0.5` instead of fractions like `1/2`.
3. Pick an operation and fill in Matrix B or the scalar if needed.
4. Click **Calculate**. Scroll through **Result** and **Steps** to see more.

If Calculate is disabled, check the message under the operation selector. Basic operations show an answer without steps.

Click a **History** entry to bring back its inputs, result, and steps. History lasts until you close the app. **Clear Result** clears the answer and steps but keeps your inputs and history.

For a quick example, enter this matrix and choose **Eigenvalues**:

```text
4 1
2 3
```

You should get eigenvalues **5** and **2**.

## Files and shortcuts

**Import Matrix** and **Ctrl+V** load data into Matrix A. Use one row per line, with spaces or commas between numbers. Every row needs the same number of entries, with no headers or brackets.

**Copy** puts the answer on your clipboard. **Export Result** saves it as text or CSV. For decompositions, these save only U for LU, R for QR, or D for diagonalization.

| Shortcut | Action |
|---|---|
| Ctrl+Enter | Calculate |
| Ctrl+L | Reset inputs, result, and steps; keep dimensions and history |
| Ctrl+C | Copy result |
| Ctrl+V | Paste Matrix A |

## A few things to know

- Enter real numbers; eigenvalue and eigenvector answers can be complex.
- Displayed values and matrix exports are rounded to at most two decimal places.
- Some operations need square matrices or independent columns. The app will flag incompatible inputs.
- Gram-Schmidt gives orthogonal columns; QR also normalizes them.
- Eigenvalue calculations are numerical, so difficult matrices can still fail to converge.