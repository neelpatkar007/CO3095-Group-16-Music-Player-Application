# Symbolic Execution Analysis: `view_songs_table`

## Symbolic Inputs
| Variable               | Symbol   | Type          |
|------------------------|----------|---------------|
| state                  | S1       | PlayerState   |
| state.library_tracks   | S2       | List[Track]   |

## Path Conditions (PCs)
| Path ID   | Condition     |
|-----------|---------------|
| PC_1      | NOT S1        |
| PC_2      | S1 AND NOT S2 |
| PC_3      | S1 AND S2     |