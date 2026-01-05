# Symbolic Analysis for open_playlist

## Symbolic Inputs
| Variable   | Symbol   | Type        |
|------------|----------|-------------|
| state      | S1       | PlayerState |
| selector   | S2       | str         |

## Path Conditions (PCs)
| Path ID   | Condition               |
|-----------|-------------------------|
| PC_1      | Resolve(S1, S2) == None |
| PC_2      | Resolve(S1, S2) != None |