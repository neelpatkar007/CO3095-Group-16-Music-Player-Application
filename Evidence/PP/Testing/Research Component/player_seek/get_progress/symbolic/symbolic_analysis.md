# Symbolic Analysis for `get_progress` Function

## Symbolic Inputs
| Variable               | Symbol  | Type        |
|:-----------------------|:--------|:------------|
| state                  | S1      | PlayerState |
| state.current_track    | S2      | Track       |
| state.position_seconds | S3      | float       |


## Path Conditions (PCs)
| Path ID   | Condition                                                                         |
|:----------|:----------------------------------------------------------------------------------|
| PC_1      | (S1 == None) OR (S1 has no attribute current_track)                               |
| PC_2      | (S1 != None) AND (NOT isinstance S2, Track) AND (isinstance S3, int OR float)     |
| PC_3      | (S1 != None) AND (NOT isinstance S2, Track) AND (NOT isinstance S3, int OR float) |
| PC_4      | (S1 != None) AND (isinstance S2, Track)                                           |