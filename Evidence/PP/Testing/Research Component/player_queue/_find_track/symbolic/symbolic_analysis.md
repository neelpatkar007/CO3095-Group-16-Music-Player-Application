# Symbolic Analysis for `_find_track` Method

## Symbolic Inputs
| Variable  | Symbol  | Type                 |
|-----------|---------|----------------------|
| state     | S1      | PlayerState (Object) |
| query     | S2      | str                  |


## Path Conditions (PCs)
| Path ID   | Condition                                                                                                                    |
|-----------|------------------------------------------------------------------------------------------------------------------------------|
| PC_1      | S2 is digit AND S1 has library_tracks AND S1.library_tracks is List AND 0 ≤ int(S2)-1 < len(S1.library_tracks)               |
| PC_2      | NOT PC_1 AND S1 has library_tracks AND S1.library_tracks is List AND (∃ t ∈ S1.library_tracks: S2 in t.display_name)         |
| PC_3      | NOT PC_1 AND (S1 lacks library_tracks OR S1.library_tracks is not List OR ∀ t ∈ S1.library_tracks: S2 not in t.display_name) |
| PC_4      | Exception Raised (e.g., S1 is None, S2 is None)                                                                              |
