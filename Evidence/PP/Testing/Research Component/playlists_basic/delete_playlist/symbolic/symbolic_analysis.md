# Symbolic Analysis for `delete_playlist`

## Symbolic Inputs
| Variable                      | Symbol  | Type               | Description                                              |
|-------------------------------|---------|--------------------|----------------------------------------------------------|
| pl                            | S1      | Optional[Playlist] | Result derived from `_resolve_playlist(state, selector)` |
| state.active_playlist_index   | S2      | Optional[int]      | Index pointer before modification                        |
| idx                           | S3      | int                | List index of `S1` within `state.playlists`              |
| state.playlists               | S4      | List[Playlist]     | The playlist container after deletion                    |

## Path Conditions (PCs)
| Path ID   | Condition                                                                            |
|-----------|--------------------------------------------------------------------------------------|
| PC_1      | S1 IS None                                                                           |
| PC_2      | S1 IS NOT None AND S2 IS None                                                        |
| PC_3      | S1 IS NOT None AND S2 IS NOT None AND S3 < S2                                        |
| PC_4      | S1 IS NOT None AND S2 IS NOT None AND NOT (S3 < S2) AND NOT (S3 == S2)               |
| PC_5      | S1 IS NOT None AND S2 IS NOT None AND NOT (S3 < S2) AND S3 == S2 AND S4 IS Empty     |
| PC_6      | S1 IS NOT None AND S2 IS NOT None AND NOT (S3 < S2) AND S3 == S2 AND S4 IS NOT Empty |