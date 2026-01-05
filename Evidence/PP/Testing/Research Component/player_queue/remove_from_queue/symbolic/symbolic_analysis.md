# Symbolic Analysis for `remove_from_queue` Function

## Symbolic Inputs
| Variable            | Symbol   | Type                 |
|---------------------|----------|----------------------|
| state               | S1       | PlayerState (Object) |
| query               | S2       | str                  |
| state.tracks        | S1_T     | List[Track]          |
| state.current_index | S1_IDX   | int                  |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------|
| PC_1      | (S1 == None) OR (S1 type IN {str, int, float, bool})                                                |
| PC_2      | NOT PC_1 AND (NOT hasattr(S1, "tracks") OR NOT type(S1.tracks) == list)                             |
| PC_3      | NOT PC_1 AND NOT PC_2 AND (len(S1.tracks) == 0)                                                     |
| PC_4      | NOT PC_1 AND NOT PC_2 AND NOT PC_3 AND (NOT S2 OR type(S2) != str)                                  |
| PC_5      | NOT PC_1 ... PC_4 AND (S2.isdigit()) AND (0 <= (int(S2)-1) < len(S1.tracks))                        |
| PC_6      | NOT PC_1 ... PC_4 AND (S2.isdigit()) AND NOT (0 <= (int(S2)-1) < len(S1.tracks))                    |
| PC_7      | NOT PC_1 ... PC_4 AND NOT (S2.isdigit()) AND (EXISTS t IN S1.tracks WHERE S2.lower IN t.name.lower) |
| PC_8      | NOT PC_1 ... PC_4 AND NOT (S2.isdigit()) AND (FOR ALL t IN S1.tracks, S2.lower NOT IN t.name.lower) |