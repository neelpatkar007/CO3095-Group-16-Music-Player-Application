# Symbolic Analysis for `_get_playlist` Function

## Symbolic Inputs
| Variable           | Symbol  | Type                 |
|--------------------|---------|----------------------|
| `state`            | S1      | PlayerState (Object) |
| `selector`         | S2      | str                  |
| `state.playlists`  | S3      | List[Playlist]       |

## Path Conditions (PCs)
| Path ID   | Condition                                                                               |
|-----------|-----------------------------------------------------------------------------------------|
| PC_1      | S1 == None OR NOT hasattr(S1, 'playlists')                                              |
| PC_2      | NOT (PC_1) AND (NOT S2 OR NOT S2.strip())                                               |
| PC_3      | NOT (PC_1) AND NOT (PC_2) AND S2.isdigit() AND (int(S2)-1 < 0 OR int(S2)-1 >= len(S3))  |
| PC_4      | NOT (PC_1) AND NOT (PC_2) AND S2.isdigit() AND (int(S2)-1 >= 0 AND int(S2)-1 < len(S3)) |
| PC_5      | NOT (PC_1) AND NOT (PC_2) AND NOT S2.isdigit() AND (S2 in [p.name for p in S3])         |
| PC_6      | NOT (PC_1) AND NOT (PC_2) AND NOT S2.isdigit() AND NOT (S2 in [p.name for p in S3])     |