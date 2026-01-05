# Concolic Analysis for `play_next` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S4)  | Path Taken         | Constraint to Flip   | New Derived Input                               |
|-------------|-----------------------------|--------------------|----------------------|-------------------------------------------------|
| 1           | (None, "song", N/A)         | PC_1 (State Error) | Flip (S1 is None)    | (MockObject, "song", N/A)                       |
| 2           | (MockObj, 123, N/A)         | PC_2 (Usage Error) | Flip (S2 is Not Str) | (MockObj, "valid_query", N/A)                   |
| 3           | (MockObj, "q", None)        | PC_4 (Not Found)   | Flip (S4 is None)    | (MockObj, "q", TrackObj)                        |
| 4           | (MockObj, "q", TrackObj)    | PC_5 (Insert Fail) | Flip (Exception)     | (MockObj, "q", TrackObj) Mocking Insert Success |
| 5           | (MockObj, "q", TrackObj)    | PC_7 (Success)     | None                 | N/A                                             |