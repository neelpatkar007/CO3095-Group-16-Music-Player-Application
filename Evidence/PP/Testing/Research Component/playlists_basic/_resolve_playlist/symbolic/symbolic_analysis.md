# Symbolic Analysis for _resolve_playlist

## Symbolic Inputs
| Variable        | Symbol   | Type                 |
|-----------------|----------|----------------------|
| state           | S1       | PlayerState (Object) |
| selector        | S2       | str                  |
| state.playlists | S3       | list[Playlist]       |

## Path Conditions (PCs)
| Path ID  | Condition                                                                                                      |
|----------|----------------------------------------------------------------------------------------------------------------|
| PC_1     | `S1 == None`                                                                                                   |
| PC_2     | `S1 != None AND NOT hasattr(S1, playlists)`                                                                    |
| PC_3     | `S1 != None AND hasattr(S1, playlists) AND NOT isinstance(S3, list)`                                           |
| PC_4     | `S1 valid AND S3 valid AND NOT isinstance(S2, str)`                                                            |
| PC_5     | `S1 valid AND S3 valid AND isinstance(S2, str) AND is_numeric(S2) AND (0 <= int(S2)-1 < len(S3))`              |
| PC_6     | `S1 valid AND S3 valid AND isinstance(S2, str) AND is_numeric(S2) AND NOT (0 <= int(S2)-1 < len(S3))`          |
| PC_7     | `S1 valid AND S3 valid AND isinstance(S2, str) AND NOT is_numeric(S2) AND EXISTS pl IN S3 : pl.name == S2`     |
| PC_8     | `S1 valid AND S3 valid AND isinstance(S2, str) AND NOT is_numeric(S2) AND NOT EXISTS pl IN S3 : pl.name == S2` |