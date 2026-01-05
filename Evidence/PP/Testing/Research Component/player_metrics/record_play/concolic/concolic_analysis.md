# Concolic Analysis of `record_play` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1...S5)   | Path Taken        | Constraint to Flip   | New Derived Input               |
|-------------|---------------------------|-------------------|----------------------|---------------------------------|
| 1           | (None, N/A...)            | PC_1 (State None) | Flip (S1 == None)    | (Obj, False, False, True, True) |
| 2           | (Obj, NoAttr, ...)        | PC_2 (No Attr)    | Flip (HasAttr)       | (Obj, True, False, True, True)  |
| 3           | (Obj, NoneTrack, ...)     | PC_3 (None Track) | Flip (Track Truthy)  | (Obj, Track, False, True, True) |
| 4           | (Obj, Track, NoPath...)   | PC_4 (No Path)    | Flip (HasAttr Path)  | (Obj, Track, Path, True, True)  |
| 5           | (..., Path, "Five")       | PC_5 (Bad Type)   | Backtrack S5         | (..., Path, 5)                  |
| 6           | (..., Path, 5)            | PC_6 (Success)    | None                 | N/A                             |