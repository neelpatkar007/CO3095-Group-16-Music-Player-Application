# Symbolic Analysis for remove_track_from_playlist

## Symbolic Inputs
| Variable               | Symbol   | Type               |
|------------------------|----------|--------------------|
| state                  | S1       | PlayerState / None |
| playlist_selector      | S2       | str                |
| playlist_index_str     | S3       | str                |
| _get_playlist(S1, S2)  | S4       | Tuple / None       |
| pl.tracks              | S5       | List / None        |
| int(S3) - 1            | S6       | int / Exception    |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                                                       |
|-----------|---------------------------------------------------------------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                                                                      |
| PC_2      | NOT S1 is None AND NOT S2                                                                                                       |
| PC_3      | NOT S1 is None AND S2 AND NOT S3                                                                                                |
| PC_4      | NOT S1 is None AND S2 AND S3 AND S4 is None                                                                                     |
| PC_5      | NOT S1 is None AND S2 AND S3 AND NOT S4 is None AND S6 is Exception                                                             |
| PC_6      | NOT S1 is None AND S2 AND S3 AND NOT S4 is None AND NOT S6 is Exception AND S6 < 0                                              |
| PC_7      | NOT S1 is None AND S2 AND S3 AND NOT S4 is None AND NOT S6 is Exception AND NOT S6 < 0 AND NOT S6 < len S5                      |
| PC_8      | NOT S1 is None AND S2 AND S3 AND NOT S4 is None AND NOT S6 is Exception AND NOT S6 < 0 AND S6 < len S5 AND S5 at S6 is None     |
| PC_9      | NOT S1 is None AND S2 AND S3 AND NOT S4 is None AND NOT S6 is Exception AND NOT S6 < 0 AND S6 < len S5 AND NOT S5 at S6 is None |