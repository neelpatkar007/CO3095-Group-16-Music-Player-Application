# Symbolic Analysis for `play_playlist` Function

## Symbolic Inputs
| Variable   | Symbol   | Type        |
|------------|----------|-------------|
| state      | S1       | PlayerState |
| selector   | S2       | str         |

## Path Conditions (PCs)
| Path ID   | Condition                             |
|-----------|---------------------------------------|
| PC_1      | _resolve_playlist(S1, S2) IS None     |
| PC_2      | _resolve_playlist(S1, S2) IS NOT None |
