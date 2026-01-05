# Symbolic Execution Analysis: `total_duration_mm_ss`

## Symbolic Inputs
| Variable                    | Symbol   | Type                 |
|-----------------------------|----------|----------------------|
| self.tracks                 | S1       | Boolean / Collection |
| self.total_duration_seconds | S2       | Integer / Float      |
| format_mm_ss (External)     | N/A      | Function             |


## Path Conditions (PCs)
| Path ID   | Condition  |
|-----------|------------|
| PC_1      | NOT S1     |
| PC_2      | S1         |