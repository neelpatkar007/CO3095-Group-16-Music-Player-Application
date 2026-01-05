# Symbolic Analysis for move_track_within_playlist

## Symbolic Inputs
| Variable              | Symbol  | Type            |
|-----------------------|---------|-----------------|
| state                 | S1      | PlayerState     |
| playlist_selector     | S2      | str             |
| from_index_str        | S3      | str             |
| to_index_str          | S4      | str             |
| _get_playlist(S1, S2) | S5      | Optional[Tuple] |
| len(pl.tracks)        | S6      | int             |
| track.display_name    | S7      | str             |

## Path Conditions (PCs)
| Path ID   | Condition                                                                               |
|-----------|-----------------------------------------------------------------------------------------|
| PC_1      | S1 == None                                                                              |
| PC_2      | NOT (S1 == None) AND (NOT S2)                                                           |
| PC_3      | NOT (S1 == None) AND S2 AND (NOT S3 OR NOT S4)                                          |
| PC_4      | NOT (S1 == None) AND S2 AND S3 AND S4 AND (S5 == None)                                  |
| PC_5      | NOT (S1 == None) AND S2 AND S3 AND S4 AND NOT (S5 == None) AND NOT (S3, S4 are numeric) |
| PC_6      | ... AND (S3, S4 are numeric) AND (NOT (0 <= from_idx < S6))                             |
| PC_7      | ... AND (0 <= from_idx < S6) AND (NOT (0 <= to_idx < S6))                               |
| PC_8      | ... AND (0 <= from_idx < S6) AND (0 <= to_idx < S6) AND (from_idx == to_idx)            |
| PC_9      | ... AND (from_idx != to_idx) AND (Track == None)                                        |
| PC_10     | ... AND (from_idx != to_idx) AND NOT (Track == None) AND S7                             |
| PC_11     | ... AND (from_idx != to_idx) AND NOT (Track == None) AND NOT S7                         |