# Symbolic Analysis of `previous_track` Function

## Symbolic Inputs
| Variable             | Symbol   | Type                                   |
|----------------------|----------|----------------------------------------|
| state                | S1       | PlayerState object (or None/primitive) |
| _get_tracks_safe(S1) | S2       | List[Track]                            |
| len(S2)              | S3       | Integer (n)                            |
| state.current_index  | S4       | Integer (old)                          |
| state.loop_mode      | S5       | String                                 |
| state.shuffle_active | S6       | Boolean                                |
| state.history        | S7       | List[Track]                            |
| state.is_playing     | S8       | Boolean                                |
| state.is_paused      | S9       | Boolean                                |


## Path Conditions (PCs)
| Path ID  | Condition                                                             |
|----------|-----------------------------------------------------------------------|
| PC_1     | S1 is None OR S1 is a primitive type                                  |
| PC_2     | NOT PC_1 AND (S2 is None OR S2 is Empty)                              |
| PC_3     | NOT PC_1 AND S2 is Valid AND S3 == 0                                  |
| PC_4     | NOT PC_1 ... PC_3 AND (S5 == "one") AND (new index OutOfBounds)       |
| PC_5     | NOT PC_1 ... PC_3 AND Valid Selection AND S8 (Playing)                |
| PC_6     | NOT PC_1 ... PC_3 AND Valid Selection AND NOT S8 AND S9 (Paused)      |
| PC_7     | NOT PC_1 ... PC_3 AND Valid Selection AND NOT S8 AND NOT S9 (Stopped) |