# Symbolic Analysis of `next_track` Function

## Symbolic Inputs
| Variable             | Symbol  | Type     | Description                              |
|----------------------|---------|----------|------------------------------------------|
| state                | S1      | Object   | The primary player state object.         |
| tracks               | S2      | List     | Retrieved via `_get_tracks_safe(S1)`.    |
| state.current_index  | S3      | Integer  | The index of the currently active track. |
| state.loop_mode      | S4      | String   | Playback mode ('off', 'one', 'all').     |
| state.shuffle_active | S5      | Boolean  | Flag indicating if shuffle is enabled.   |
| state.is_playing     | S6      | Boolean  | Flag indicating active playback.         |
| state.is_paused      | S7      | Boolean  | Flag indicating paused playback.         |
| n                    | S8      | Integer  | Derived length of tracks (`len(S2)`).    |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                | Description                           |
|-----------|------------------------------------------------------------------------------------------|---------------------------------------|
| PC_1      | S1 is None OR Type(S1) in Primitives                                                     | Invalid State Input (Early Return).   |
| PC_2      | NOT PC_1 AND (S2 is None OR len(S2) == 0)                                                | No Tracks Available (Early Return).   |
| PC_3      | NOT PC_1 AND NOT PC_2 AND S4 == 'one'                                                    | Loop One Mode (Stays on current).     |
| PC_4      | NOT PC_1 AND NOT PC_2 AND S4 != 'one' AND S5 == True AND S8 > 1                          | Shuffle Mode (Random jump).           |
| PC_5      | NOT PC_1 AND NOT PC_2 AND S4 != 'one' AND S5 == False AND (S3 + 1) >= S8 AND S4 != 'all' | Sequential End - Stop (Early Return). |
| PC_6      | NOT PC_1 AND NOT PC_2 AND S4 != 'one' AND S5 == False AND (S3 + 1) >= S8 AND S4 == 'all' | Sequential End - Loop All (Wrap).     |
| PC_7      | NOT PC_1 AND NOT PC_2 AND S4 != 'one' AND S5 == False AND (S3 + 1) < S8                  | Sequential Normal (Next Track).       |