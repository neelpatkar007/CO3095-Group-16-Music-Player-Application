# Symbolic Analysis for `add_to_queue` Function

## Symbolic Inputs
| Variable             | Symbol  | Type           | Description                        |
|----------------------|---------|----------------|------------------------------------|
| state                | S1      | Object         | The player state object            |
| query                | S2      | String         | User search query                  |
| state.library_tracks | S3      | List / Boolean | Library existence and truthiness   |
| state.tracks         | S4      | List / Mutator | Track list and mutability          |
| _find_track(result)  | S5      | Object         | Result returned by helper function |
| found.display_name   | S6      | String         | Track name property                |
| len(state.tracks)    | S7      | Integer        | Queue length after append          |
| Exception            | S8      | Error          | Exception raised during append     |

## Path Conditions (PCs)
| Path ID  | Condition                                                                               |
|----------|-----------------------------------------------------------------------------------------|
| PC_1     | S1 is None OR Type(S1) IN {str, int, float, bool}                                       |
| PC_2     | NOT PC_1 AND (NOT S2 OR Type(S2) != str)                                                |
| PC_3     | NOT PC_1 AND NOT PC_2 AND (NOT hasattr(S1, "library_tracks") OR NOT S3)                 |
| PC_4     | NOT PC_1..PC_3 AND (NOT hasattr(S1, "tracks") OR S4 is None) AND Raises(AttributeError) |
| PC_5     | NOT PC_1..PC_4 AND (S5 is False/None)                                                   |
| PC_6     | NOT PC_1..PC_5 AND (NOT hasattr(S5, "display_name") OR NOT S6)                          |
| PC_7     | NOT PC_1..PC_6 AND Raises(Exception during append)                                      |
| PC_8     | NOT PC_1..PC_7 AND S7 > 500                                                             |
| PC_9     | NOT PC_1..PC_7 AND S7 <= 500                                                            |