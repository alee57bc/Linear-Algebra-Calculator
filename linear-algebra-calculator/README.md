Linear Algebra Calculator

Left:
- fix UI
- check tests
- update documentation
- release

UI improvements:
- Make Matrix A / Matrix B panels visually balanced and the same minimum size.
- Put the operation panel in a narrower centered column.
- Give Result more vertical space, especially for LU/QR/Diagonalization.
- Make the Step View wider and taller than History, because it carries more information.
- Make the History panel narrower but easier to scan.
- Add section padding and consistent spacing between widgets.
- Use slightly larger titles for group boxes.
- Make the Calculate button more visually prominent.
- Make result matrices centered instead of hugging the top-left.
- Add scroll areas to Result and Step View so large matrices don’t wreck the layout.
- Add a short operation description under the operation selector, like:
- “Compute A⁻¹”
- “Find eigenvalues of A”
- “Factor A into QR”
- Show matrix dimensions in the panel title, e.g. Matrix A (3 × 3).
- Disable Calculate when required inputs are invalid instead of waiting for an error dialog.
- Add clearer empty states like:
- No result yet, No calculation steps yet, No history yet
- Show operation names in History with a compact summary, like LU Decomposition — 3×3.
- Add a small “Clear Result” button near Result.
- Add Copy directly beside Result instead of relying only on Ctrl+C.
- For LU/QR/Diagonalization, visually separate each result matrix with spacing or a small divider.
- For eigenvalues/eigenvectors, use cleaner math-like labels such as λ₁, λ₂, v₁, v₂.
- Use monospace font for matrix values if you want columns to align better.

1. Result/Step scroll areas
2. Better spacing and sizing
3. Cleaner History entries
4. More polished matrix/result presentation
5. Small stylesheet
6. Operation descriptions
7. Better empty states
8. Optional light/dark theme later