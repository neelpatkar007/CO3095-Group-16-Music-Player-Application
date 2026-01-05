# Symbolic Execution Analysis: `print_now_playing`

| Variable                    | Symbol   | Type               | Description                               |
|-----------------------------|----------|--------------------|-------------------------------------------|
| `_ensure_player_state(...)` | S1       | PlayerState        | None                                      |
| `state.current_track`       | S2       | Track              | None                                      |
| `isinstance(S2, Track)`     | S3       | Boolean            | Type integrity check for the track object |
| `hasattr(S2, "name")`       | S4       | Boolean            | Presence of display name metadata         |
| `state.is_playing`          | S5       | Boolean            | Boolean flag for active playback          |
| `state.is_paused`           | S6       | Boolean            | Boolean flag for paused playback          |

## Path Conditions (PCs)
| Path ID  | Condition                                                     |
|----------|---------------------------------------------------------------|
| PC_1     | S1 == None                                                    |
| PC_2     | S1 != None AND S2 == None                                     |
| PC_3     | S1 != None AND S2 != None AND NOT S3                          |
| PC_4     | S1 != None AND S2 != None AND S3 AND NOT S4                   |
| PC_5     | S1 != None AND S2 != None AND S3 AND S4 AND S5 AND S6         |
| PC_6     | S1 != None AND S2 != None AND S3 AND S4 AND S5 AND NOT S6     |
| PC_7     | S1 != None AND S2 != None AND S3 AND S4 AND NOT S5 AND S6     |
| PC_8     | S1 != None AND S2 != None AND S3 AND S4 AND NOT S5 AND NOT S6 |
