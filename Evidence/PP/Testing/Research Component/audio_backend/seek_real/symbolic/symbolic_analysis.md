# Symbolic Execution Analysis: `_seek_real`

## Symbolic Inputs
| Variable                 | Symbol   | Type    | Description                                 |
|--------------------------|----------|---------|---------------------------------------------|
| pygame (Module State)    | S1       | Module  | Global Pygame module state (None or Valid). |
| seconds                  | S2       | Float   | The target seek position in seconds.        |
| self.current_speed       | S3       | Float   | The playback speed multiplier.              |
| self.temp_file.exists()  | S4       | Boolean | Result of file system check for temp file.  |
| self.muted               | S5       | Boolean | The audio mute state flag.                  |
| Exception (Runtime)      | S6       | Error   | Occurs if load, play, or set_volume fail.   |


## Path Conditions (PCs)
| Path ID   | Condition                                  | Description                                               |
|-----------|--------------------------------------------|-----------------------------------------------------------|
| PC_1      | NOT S1                                     | pygame is None; Assertion fails immediately.              |
| PC_2      | S1 AND (S3 != 1.0 AND S4) AND NOT S6       | Valid pygame, speed modified, temp file exists, no error. |
| PC_3      | S1 AND NOT (S3 != 1.0 AND S4) AND NOT S6   | Valid pygame, normal speed OR no temp file, no error.     |
| PC_4      | S1 AND NOT S6 AND S5                       | Execution succeeds, muted volume branch taken.            |
| PC_5      | S1 AND NOT S6 AND NOT S5                   | Execution succeeds, normal volume branch taken.           |
| PC_6      | S1 AND S6                                  | Valid pygame, but runtime Exception occurs during logic.  |