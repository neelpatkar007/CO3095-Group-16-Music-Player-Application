# Symbolic Analysis for summary_line Method

## Symbolic Inputs
| Variable                  | Symbol  | Type    |
|---------------------------|---------|---------|
| index                     | S1      | int     |
| active                    | S2      | bool    |
| self.name                 | S3      | str     |
| self.num_tracks           | S4      | int     |
| self.total_duration_mm_ss | S5      | str     |

## Path Conditions (PCs)
| Path ID   | Condition                         |
|-----------|-----------------------------------|
| PC_1      | (S1 is int) AND (S2 is True)      |
| PC_2      | (S1 is int) AND (S2 is False)     |
| PC_3      | NOT (S1 is int) AND (S2 is True)  |
| PC_4      | NOT (S1 is int) AND (S2 is False) |