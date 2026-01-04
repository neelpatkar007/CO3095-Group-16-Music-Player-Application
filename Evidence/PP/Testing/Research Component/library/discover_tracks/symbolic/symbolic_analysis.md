# Symbolic Analysis of `discover_tracks` Function

## Symbolic Inputs
| Variable                             | Symbol   | Type         | Description                                           |
|--------------------------------------|----------|--------------|-------------------------------------------------------|
| `MUSIC_DIR.exists()`                 | S1       | Boolean      | Indicates whether the root music directory exists     |
| `path.is_file()`                     | S2       | Boolean      | Whether the current directory entry is a file         |
| `path.suffix ∈ SUPPORTED_EXTENSIONS` | S3       | Boolean      | Predicate checking if the file extension is supported |
| `_read_metadata(path)`               | S4       | Tuple        | Metadata tuple `(title, artist, duration)`            |
| `duration` (from S4)                 | S5       | Float / None | Duration value extracted from metadata                |

## Path Conditions (PCs)
| Path ID    | Condition                  |
|------------|----------------------------|
| **PC_1**   | ¬S1                        |
| **PC_2**   | S1 ∧ ¬S2                   |
| **PC_3**   | S1 ∧ S2 ∧ ¬S3              |
| **PC_4**   | S1 ∧ S2 ∧ S3 ∧ (S5 = None) |
| **PC_5**   | S1 ∧ S2 ∧ S3 ∧ (S5 ≠ None) |