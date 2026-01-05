# Symbolic Analysis for `set_playback_speed` Method

## Symbolic Inputs
| Variable             | Symbol  | Type        | Description                          |
|----------------------|---------|-------------|--------------------------------------|
| state                | S1      | PlayerState | The target state object instance     |
| speed                | S2      | float       | Requested playback speed             |
| state.playback_speed | S3      | float       | Existing speed value before mutation |
| state.is_playing     | S4      | bool        | Flag indicating active playback      |
| state.is_paused      | S5      | bool        | Flag indicating paused status        |


## Path Conditions (PCs)
| Path ID  | Condition                                                                     |
|----------|-------------------------------------------------------------------------------|
| PC_1     | NOT isinstance(S1, PlayerState)                                               |
| PC_2     | isinstance(S1, PlayerState) AND S1 is None                                    |
| PC_3     | isinstance(S1, PlayerState) AND S1 is NOT None AND NOT isinstance(S2, Number) |
| PC_4     | ... AND isinstance(S2, Number) AND (S2 < 0.5 OR S2 > 2.0)                     |
| PC_5     | ... AND (0.5 <= S2 <= 2.0) AND hasattr(S1, 'playback_speed') AND (S3 == S2)   |
| PC_6     | ... AND (S3 != S2) AND S4                                                     |
| PC_7     | ... AND (S3 != S2) AND NOT S4 AND S5                                          |
| PC_8     | ... AND (S3 != S2) AND NOT S4 AND NOT S5                                      |
