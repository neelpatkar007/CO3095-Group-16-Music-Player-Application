# Symbolic Analysis of `play_next` Function

## Symbolic Inputs
| Variable           | Symbol  | Type           | Description                                     |
|--------------------|---------|----------------|-------------------------------------------------|
| state              | S1      | PlayerState    | The playback state object                       |
| query              | S2      | str            | Track search query                              |
| state.tracks       | S3      | list           | List of track objects in the state              |
| _find_track()      | S4      | Track          | Result returned by the helper function          |
| tracks.insert()    | S5      | Void/Exception | Outcome of insertion attempt                    |
| Post-Insert Check  | S6      | bool           | Verification that `tracks[insert_idx] == found` |

## Path Conditions (PCs)
| Path ID   | Condition                                                                      |
|-----------|--------------------------------------------------------------------------------|
| PC_1      | S1 is None OR S1 is Primitive                                                  |
| PC_2      | NOT PC_1 AND (S2 is Empty OR S2 is NOT str)                                    |
| PC_3      | NOT PC_1 AND NOT PC_2 AND (S3 NOT List) AND (Setting S3 raises AttributeError) |
| PC_4      | NOT PC_1 AND NOT PC_2 AND (S3 is List OR Fixed) AND (S4 is None)               |
| PC_5      | NOT PC_1 AND NOT PC_2 AND NOT PC_4 AND (S5 raises Exception)                   |
| PC_6      | NOT PC_1 AND NOT PC_2 AND NOT PC_4 AND NOT PC_5 AND (S6 is False)              |
| PC_7      | NOT PC_1 AND NOT PC_2 AND NOT PC_4 AND NOT PC_5 AND (S6 is True)               |

