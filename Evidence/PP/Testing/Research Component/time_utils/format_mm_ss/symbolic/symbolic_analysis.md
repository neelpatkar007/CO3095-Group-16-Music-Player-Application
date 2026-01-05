# Symbolic Analysis for `format_mm_ss`

## Symbolic Inputs
| Variable   | Symbol  | Type          |
|------------|---------|---------------|
| seconds    | S1      | float OR None |

## Path Conditions (PCs)
| Path ID   | Condition                  |
|-----------|----------------------------|
| PC_1      | S1 is None OR S1 < 0       |
| PC_2      | S1 is NOT None AND S1 >= 0 |