# Symbolic Analysis of player_core.pause Function

## Symbolic Inputs
| Variable           | Symbol   | Type     |
|--------------------|----------|----------|
| state.is_playing   | S1       | Boolean  |
| state.is_paused    | S2       | Boolean  |

## Path Conditions (PCs)
| Path ID   | Condition       |
|-----------|-----------------|
| PC_1      | (NOT S1) OR S2  |
| PC_2      | S1 AND (NOT S2) |
