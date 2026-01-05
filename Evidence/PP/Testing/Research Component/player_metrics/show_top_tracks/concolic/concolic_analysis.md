# Concolic Analysis of `show_top_tracks` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1...S8)   | Path Taken      | Constraint to Flip   | New Derived Input        |
|-------------|---------------------------|-----------------|----------------------|--------------------------|
| 1           | (None, ...)               | PC_1            | Flip (S1 == None)    | (Obj, NoCounts...)       |
| 2           | (Obj, CorruptType, ...)   | PC_3            | Flip (S3 Is Dict)    | (Obj, EmptyDict...)      |
| 3           | (Obj, EmptyDict, ...)     | PC_4            | Flip (S4 Empty)      | (Obj, {"a": 1})          |
| 4           | (Obj, {"a": 1}, FailSort) | PC_5            | Flip (S5 Success)    | (Obj, {"a": 1}, Success) |
| 5           | (Obj, {"a": -5}, Success) | PC_7 (Skip)     | Flip (S7 > 0)        | (Obj, {"a": 5})          |
| 6           | (Obj, {"a": 5}, NoLib)    | PC_8 (Fallback) | Flip (S8 Found)      | (Obj, {"a": 5}, Lib=[a]) |
| 7           | (Obj, 11_Items, ...)      | PC_6 (Limit)    | None                 | N/A                      |
