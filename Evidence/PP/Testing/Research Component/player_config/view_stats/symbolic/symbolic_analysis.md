# Symbolic Execution Analysis: `view_stats`

## Symbolic Inputs
| Variable               | Symbol  | Type        | Description                                       |
|------------------------|---------|-------------|---------------------------------------------------|
| state                  | S1      | Object      | The primary input object instance                 |
| state.play_counts      | S2      | Dictionary  | Mapping of file paths to play frequencies         |
| state.library_tracks   | S3      | List        | Collection of `Track` objects containing metadata |
| state.total_play_time  | S4      | Int/Float   | Cumulative listening duration in seconds          |
| Derived: artist_counts | S5      | Dictionary  | Computed aggregation of plays per artist          |

## Path Conditions (PCs)
| Path ID   | Condition                                                                      |
|-----------|--------------------------------------------------------------------------------|
| PC_1      | `S1 == None`                                                                   |
| PC_2      | `S1 != None AND NOT (S2 is Dict)`                                              |
| PC_3      | `S1 != None AND S2 is Dict AND S2 is Empty`                                    |
| PC_4      | `S1 != None AND S2 is Dict AND NOT Empty AND NOT (S3 is List AND S3 != Empty)` |
| PC_5      | `... AND (S3 is List AND S3 != Empty) AND NOT (S4 is Numeric)`                 |
| PC_6      | `... AND (S4 is Numeric) AND (S5 is Empty)`                                    |
| PC_7      | `... AND (S4 is Numeric) AND NOT (S5 is Empty)`                                |