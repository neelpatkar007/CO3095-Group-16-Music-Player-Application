# Concolic Analysis for import_song Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3...)            | Path Taken   | Constraint to Flip         | New Derived Input                        |
|------------|------------------------------------------|--------------|----------------------------|------------------------------------------|
| 1          | ("", False, False...)                    | PC_1         | Flip (NOT S1)              | ("song.mp3", False, False...)            |
| 2          | ("song.mp3", False, False...)            | PC_2         | Flip (NOT S2)              | ("song.mp3", True, False...)             |
| 3          | ("song.mp3", True, False...)             | PC_3         | Flip (NOT S3)              | ("song.mp3", True, True, 0...)           |
| 4          | ("song.mp3", True, True, 0...)           | PC_4         | Flip (S4 == 0)             | ("song.mp3", True, True, 100...)         |
| 5          | ("song.mp3", True, True, 100, ".txt"...) | PC_5         | Flip (S5 NOT IN SUPPORTED) | ("song.mp3", True, True, 100, ".mp3"...) |
