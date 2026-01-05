# Symbolic Analysis for player_seek_nudge

## Symbolic Inputs
| Variable               | Symbol  | Type                  |
|------------------------|---------|-----------------------|
| state                  | S1      | Optional[PlayerState] |
| state.position_seconds | S2      | Any (Expected float)  |
| offset_seconds         | S3      | float                 |

## Path Conditions (PCs)
| Path ID  | Condition                                         |
|----------|---------------------------------------------------|
| PC_1     | S1 == None                                        |
| PC_2     | NOT S1 == None AND NOT (S2 is float OR S2 is int) |
| PC_3     | NOT S1 == None AND (S2 is float OR S2 is int)     |