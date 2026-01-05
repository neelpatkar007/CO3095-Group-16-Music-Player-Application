# Symbolic Analysis for rate_song Function

## Symbolic Inputs
| Variable                     | Symbol   | Type               |
|------------------------------|----------|--------------------|
| state                        | S1       | PlayerState / None |
| hasattr(S1, "current_track") | S2       | Boolean            |
| S1.current_track             | S3       | Track / None       |
| rating_str                   | S4       | String             |
| hasattr(S3, "path")          | S5       | Boolean            |
| hasattr(S1, "song_ratings")  | S6       | Boolean            |

## Path Conditions (PCs)
| Path ID  | Condition                                                                             |
|----------|---------------------------------------------------------------------------------------|
| PC_1     | S1 is None OR NOT S2                                                                  |
| PC_2     | NOT (S1 is None OR NOT S2) AND S3 is None                                             |
| PC_3     | NOT (S1 is None OR NOT S2) AND NOT S3 is None AND (S4 is NOT Int OR S4 < 1 OR S4 > 5) |
| PC_4     | NOT (PC_1 OR PC_2 OR PC_3) AND (NOT S5 OR NOT S6)                                     |
| PC_5     | NOT (PC_1 OR PC_2 OR PC_3) AND S5 AND S6                                              |
