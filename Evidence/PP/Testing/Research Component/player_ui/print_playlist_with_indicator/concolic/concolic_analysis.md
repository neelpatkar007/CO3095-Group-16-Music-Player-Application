# Concolic Analysis: `print_playlist_with_indicator`

## Path Exploration Table
| Iteration  | Concrete Seed ($S_1 \dots S_8$)                                   | Path Taken             | Constraint to Flip       | New Derived Input                 |
|------------|-------------------------------------------------------------------|------------------------|--------------------------|-----------------------------------|
| 1          | State is `None` ($S_1 = True$)                                    | PC_1 (Early Return)    | Flip ($S_1$)             | State is valid object             |
| 2          | State valid, Tracks = `"InvalidString"` ($S_2 = True$)            | PC_2 (Type Error)      | Flip ($S_2$)             | State valid, Tracks = `[]`        |
| 3          | State valid, Tracks = `[]` ($S_3 = True$)                         | PC_3 (Empty Error)     | Flip ($S_3$)             | State valid, Tracks = `[T1]`      |
| 4          | Tracks = `[T1]`, Current ≠ `T1` ($S_6 = False$)                   | PC_4 (No Indicator)    | Flip ($S_6$)             | Tracks = `[T1]`, Current = `T1`   |
| 5          | Current = `T1`, Playing = `True` ($S_7 = True$)                   | PC_5 (Play Indicator)  | Flip ($S_7$)             | Current = `T1`, Playing = `False` |
| 6          | Current = `T1`, Playing = `False`, Paused = `True` ($S_8 = True$) | PC_6 (Pause Indicator) | Flip ($S_8$)             | Current = `T1`, Paused = `False`  |
| 7          | Current = `T1`, Not Playing, Not Paused                           | PC_7 (Stop Indicator)  | None (Coverage Complete) | N/A                               |