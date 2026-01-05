# Symbolic Analysis for `list_playlists` Function

## Symbolic Inputs
| Variable                 | Symbol  | Type                    |
|--------------------------|---------|-------------------------|
| state                    | S1      | PlayerState OR NoneType |
| getattr(S1, 'playlists') | S2      | List OR NoneType OR Any |
| isinstance(S2, list)     | S3      | Boolean                 |
| len(S2) > 0              | S4      | Boolean                 |
| S2[0] (Iterator Item)    | S5      | Playlist OR NoneType    |
| S1.active_playlist_index | S6      | Integer OR NoneType     |
| current_index (idx - 1)  | S7      | Integer                 |
| track_count              | S8      | Integer                 |

## Path Conditions (PCs)
| Path ID   | Condition                                              |
|-----------|--------------------------------------------------------|
| PC_1      | S1 is None                                             |
| PC_2      | S1 is NOT None AND S2 is None                          |
| PC_3      | S1 is NOT None AND S2 is NOT None AND S3 is False      |
| PC_4      | S1 is NOT None AND S3 is True AND S4 is False          |
| PC_5      | … AND S4 is True AND S5 is None                        |
| PC_6      | … AND S5 is NOT None AND (S6 is None OR S6 != S7)      |
| PC_7      | … AND S5 is NOT None AND (S6 is NOT None AND S6 == S7) |