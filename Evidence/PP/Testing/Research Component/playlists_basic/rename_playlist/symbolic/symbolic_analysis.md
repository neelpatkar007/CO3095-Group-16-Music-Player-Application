# Symbolic Analysis for rename_playlist Function

## Symbolic Inputs
| Variable   | Symbol  | Type                           |
|------------|---------|--------------------------------|
| state      | S1      | PlayerState (Composite Object) |
| selector   | S2      | str                            |
| new_name   | S3      | str                            |


## Path Conditions (PCs)
| Path ID   | Condition                                                                                                                                                      |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PC_1      | `(S3 OR empty_string) stripped IS empty`                                                                                                                       |
| PC_2      | `(S3 OR empty_string) stripped IS NOT empty AND _resolve_playlist(S1, S2) IS None`                                                                             |
| PC_3      | `(S3 OR empty_string) stripped IS NOT empty AND _resolve_playlist(S1, S2) IS NOT None AND EXISTS other IN S1.playlists (other IS NOT pl AND other.name == S3)` |
| PC_4      | `(S3 OR empty_string) stripped IS NOT empty AND _resolve_playlist(S1, S2) IS NOT None AND FOR ALL other IN S1.playlists (other IS pl OR other.name != S3)`     |

