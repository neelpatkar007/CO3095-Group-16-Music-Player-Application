# Symbolic Analysis of `update_playback` Function

## Symbolic Inputs
| Variable / Predicate                                      | Symbol   | Type           | Description                                               |
|-----------------------------------------------------------|----------|----------------|-----------------------------------------------------------|
| isinstance(state, PlayerState)                            | S1       | Boolean        | Validity check for the state object type.                 |
| isinstance(delta_seconds, (int, float))                   | S2       | Boolean        | Validity check for the time delta type.                   |
| hasattr(state, "sleep_deadline") AND state.sleep_deadline | S3       | Boolean        | Existence and truthiness of the sleep deadline attribute. |
| time.time() > state.sleep_deadline                        | S4       | Boolean        | Temporal check to see if the sleep timer has expired.     |
| delta_seconds <= 0                                        | S5       | Boolean        | Validation that time delta is positive.                   |
| state.is_playing                                          | S6       | Boolean        | Flag indicating if the player is active.                  |
| state.is_paused                                           | S7       | Boolean        | Flag indicating if the player is paused.                  |
| state.current_track                                       | S8       | Object / None  | Existence check for the current track object.             |
| track.duration_seconds is not None                        | S9       | Boolean        | Validity check for track duration.                        |
| state.position_seconds >= track.duration_seconds          | S10      | Boolean        | Comparison to determine if the track has finished.        |

## Path Conditions (PCs)
| Path ID  | Condition                                                                               |
|----------|-----------------------------------------------------------------------------------------|
| PC_1     | NOT S1                                                                                  |
| PC_2     | S1 AND NOT S2                                                                           |
| PC_3     | S1 AND S2 AND S3 AND S4                                                                 |
| PC_4     | S1 AND S2 AND (NOT S3 OR NOT S4) AND S5                                                 |
| PC_5     | S1 AND S2 AND (NOT S3 OR NOT S4) AND NOT S5 AND (NOT S6 OR S7)                          |
| PC_6     | S1 AND S2 AND (NOT S3 OR NOT S4) AND NOT S5 AND S6 AND NOT S7 AND (NOT S8 OR NOT S9)    |
| PC_7     | S1 AND S2 AND (NOT S3 OR NOT S4) AND NOT S5 AND S6 AND NOT S7 AND S8 AND S9 AND S10     |
| PC_8     | S1 AND S2 AND (NOT S3 OR NOT S4) AND NOT S5 AND S6 AND NOT S7 AND S8 AND S9 AND NOT S10 |
