# Symbolic Analysis for `play` Method in `player_core`

## Symbolic Inputs
| Variable                 | Symbol  | Type        | Description                                      |
|--------------------------|---------|-------------|--------------------------------------------------|
| state                    | S1      | PlayerState | The primary input object.                        |
| state.audio_engine       | S2      | Object      | The backend audio driver instance.               |
| state.audio_engine.play  | S3      | Method      | The play method on the engine (existence check). |
| state.current_track      | S4      | Object      | The track object loaded in the state.            |
| state.current_track.path | S5      | String      | File path of the track (existence check).        |
| state.is_playing         | S6      | Boolean     | Flag indicating playback status.                 |
| state.is_paused          | S7      | Boolean     | Flag indicating pause status.                    |

## Path Conditions (PCs)
| Path ID   | Condition                                                                 |
|-----------|---------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                |
| PC_2      | S1 is NOT None AND NOT isinstance(S1, PlayerState)                        |
| PC_3      | S1 is PlayerState AND NOT hasattr(S1, "audio_engine")                     |
| PC_4      | S1 has S2 AND NOT hasattr(S2, "play")                                     |
| PC_5      | S1 has S2.play AND S4 is None                                             |
| PC_6      | S1 has S4 AND NOT hasattr(S4, "path")                                     |
| PC_7      | S1 Valid AND S6 is True AND S7 is False                                   |
| PC_8      | S1 Valid AND (S6 is False OR (S6 is True AND S7 is True)) AND S7 is True  |
| PC_9      | S1 Valid AND (S6 is False OR (S6 is True AND S7 is True)) AND S7 is False |