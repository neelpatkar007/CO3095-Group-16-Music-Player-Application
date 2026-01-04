# Symbolic Analysis of `read_metadata` Function

## Symbolic Inputs
| Variable             | Symbol  | Type               | Description                                 |
|----------------------|---------|--------------------|---------------------------------------------|
| `path.stem`          | S1      | String             | Fallback title derived from filename        |
| `HAS_MUTAGEN`        | S2      | Boolean            | Global flag indicating library availability |
| `mutagen.File(path)` | S3      | Object / None      | Result of attempting to load the audio file |
| `info.length`        | S4      | Float / Exception  | Duration value or failure during casting    |
| `audio.tags`         | S5      | Boolean            | Whether tags exist and are non-empty        |
| `tags["TIT2"]`       | S6      | String / Exception | Title tag presence and castability          |
| `tags["TPE1"]`       | S7      | String / Exception | Artist tag presence and castability         |

## Path Conditions (PCs)
| Path ID   | Condition                        | Logical Description                                                          |
|-----------|----------------------------------|------------------------------------------------------------------------------|
| **PC_1**  | ¬S2                              | Library unavailable; immediate return of defaults                            |
| **PC_2**  | S2 ∧ ¬S3                         | Library present, but file loading fails                                      |
| **PC_3**  | S2 ∧ S3 ∧ ¬S5                    | File loaded, but no tags present (duration may or may not be set)            |
| **PC_4**  | S2 ∧ S3 ∧ S4 ∧ S5 ∧ S6 ∧ S7      | Maximal success: duration, title, and artist all extracted successfully      |
| **PC_5**  | S2 ∧ S3 ∧ ¬S4 ∧ S5 ∧ (¬S6 ∨ ¬S7) | Resilient path: file loaded, but one or more metadata fields fail gracefully |