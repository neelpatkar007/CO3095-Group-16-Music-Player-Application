# Concolic Analysis Strategy: `_print_tracks_table`

## Path Exploration Table
| Iteration   | Concrete Seed ($S1$, $S2$)     | Path Taken                | Constraint to Flip                         | New Derived Input                          |
|:------------|:-------------------------------|:--------------------------|:-------------------------------------------|:-------------------------------------------|
| **1**       | $S1$ = `[]`                    | **PC_1** (Early Return)   | Flip ($NOT S1$) → $S1$                     | `[None]` (A non-empty list)                |
| **2**       | $S1$ = `[None]`, $S2$ = `None` | **PC_2** (Skip Iteration) | Flip ($S2$ IS `None`) → $S2$ IS NOT `None` | `[MockTrack]` (A list with a valid object) |
| **3**       | $S1$ = `[Obj]`, $S2$ = `Obj`   | **PC_3** (Print Row)      | None (All structural branches covered)     | N/A                                        |