# Symbolic Analysis for `player_core.stop`

## Symbolic Inputs
| Variable                | Symbol  | Type     | Description                            |
|-------------------------|---------|----------|----------------------------------------|
| state.is_playing        | S1      | Boolean  | Flag indicating active playback.       |
| state.is_paused         | S2      | Boolean  | Flag indicating suspended playback.    |
| state.audio_engine      | S3      | Object   | The underlying audio driver interface. |
| state.position_seconds  | S4      | Float    | The cursor position of the track.      |


## Path Conditions (PCs)
| Path ID   | Condition         | Logic Description                            |
|-----------|-------------------|----------------------------------------------|
| PC_1      | NOT S1 AND NOT S2 | System is neither playing nor paused (Idle). |
| PC_2      | S1 OR S2          | System is either playing, paused, or both.   |
