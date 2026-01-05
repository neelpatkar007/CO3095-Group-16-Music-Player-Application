# Concolic Analysis of `update_playback` Function

## Path Exploration Table
| Iteration   | Concrete Seed (Inputs & State)           | Path Taken           | Constraint to Flip   | New Derived Input                        |
|-------------|------------------------------------------|----------------------|----------------------|------------------------------------------|
| 1           | state = None, delta = 1.0                | PC_1 (Type Error)    | Flip (NOT S1) → S1   | state = PlayerState(), delta = 1.0       |
| 2           | state = PlayerState, delta = "invalid"   | PC_2 (Type Error)    | Flip (NOT S2) → S2   | state = PlayerState, delta = 1.0         |
| 3           | state (deadl = None), delta = 1.0        | PC_4 (Delta check\*) | Flip (NOT S3) → S3   | state (deadl = expired), delta = 1.0     |
| 4           | state (deadl = expired), delta = 1.0     | PC_3 (Sleep Stop)    | Flip (S4) → NOT S4   | state (deadl = future), delta = 1.0      |
| 5           | state (deadl = future), delta = -1.0     | PC_4 (Neg Delta)     | Flip (S5) → NOT S5   | state (deadl = future), delta = 1.0      |
| 6           | state (playing = False), delta = 1.0     | PC_5 (Not Playing)   | Flip (NOT S6) → S6   | state (playing = True), delta = 1.0      |
| 7           | state (paused = True), delta = 1.0       | PC_5 (Paused)        | Flip (S7) → NOT S7   | state (paused = False), delta = 1.0      |
| 8           | state (no track), delta = 1.0            | PC_6 (No Track)      | Flip (NOT S8) → S8   | state (track = Track), delta = 1.0       |
| 9           | state (pos = 10, dur = 100), delta = 1.0 | PC_8 (Progress)      | Flip (NOT S10) → S10 | state (pos = 99, dur = 100), delta = 2.0 |
| 10          | state (pos = 99, dur = 100), delta = 2.0 | PC_7 (Next Track)    | None (Complete)      | N/A                                      |