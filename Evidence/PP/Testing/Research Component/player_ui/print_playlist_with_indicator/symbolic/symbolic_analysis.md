# Symbolic Analysis of `print_playlist_with_indicator`

## Symbolic Inputs
| Variable / Expression                              | Symbol  | Type     | Description                                            |
|----------------------------------------------------|---------|----------|--------------------------------------------------------|
| `_ensure_player_state(...) is None`                | S1      | Boolean  | Failsafe check failure (state is invalid or `None`)    |
| `not isinstance(tracks, list)` OR invalid elements | S2      | Boolean  | Data integrity failure (invalid list or element types) |
| `not tracks`                                       | S3      | Boolean  | Empty library check                                    |
| `any(not t.display_name for t in tracks)`          | S4      | Boolean  | Metadata integrity warning (missing titles)            |
| `len(tracks) == 1`                                 | S5      | Boolean  | Cardinality warning (single-track library)             |
| `current and track == current`                     | S6      | Boolean  | Current track match in iteration                       |
| `state.is_playing`                                 | S7      | Boolean  | Playback state: playing                                |
| `state.is_paused`                                  | S8      | Boolean  | Playback state: paused                                 |


## Path Conditions (PCs)
| Path ID   | Condition                                | Outcome                       |
|-----------|------------------------------------------|-------------------------------|
| PC_1      | S1                                       | Early return (invalid state)  |
| PC_2      | NOT S1 AND S2                            | Early return (type error)     |
| PC_3      | NOT S1 AND NOT S2 AND S3                 | Early return (empty library)  |
| PC_4      | NOT S1 AND NOT S2 AND NOT S3 AND NOT S6  | Print track (no indicator)    |
| PC_5      | … AND S6 AND S7                          | Print track (play indicator)  |
| PC_6      | … AND S6 AND NOT S7 AND S8               | Print track (pause indicator) |
| PC_7      | … AND S6 AND NOT S7 AND NOT S8           | Print track (stop indicator)  |