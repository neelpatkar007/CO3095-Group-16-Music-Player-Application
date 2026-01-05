# Symbolic Analysis for `render_progress_bar` Function

## Symbolic Inputs
| Variable                    | Symbol   | Type               |
|-----------------------------|----------|--------------------|
| state                       | S1       | PlayerState / None |
| width                       | S2       | int / any          |
| pos (from `get_progress`)   | S3       | float / int / None |
| total (from `get_progress`) | S4       | float / int / None |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                    |
|-----------|----------------------------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                                   |
| PC_2      | NOT (S1 is None) AND NOT (S2 is int)                                                         |
| PC_3      | NOT (S1 is None) AND (S2 is int) AND S2 <= 0                                                 |
| PC_4      | NOT (S1 is None) AND (S2 is int) AND S2 > 0 AND S4 is None                                   |
| PC_5      | NOT (S1 is None) AND (S2 is int) AND S2 > 0 AND NOT (S4 is None) AND NOT (S4 is num)         |
| PC_6      | NOT (S1 is None) AND (S2 is int) AND S2 > 0 AND NOT (S4 is None) AND (S4 is num) AND S4 <= 0 |
| PC_7      | NOT (S1 is None) AND (S2 is int) AND S2 > 0 AND (S4 is num) AND S4 > 0                       |