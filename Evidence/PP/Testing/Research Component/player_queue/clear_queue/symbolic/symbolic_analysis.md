# Symbolic Analysis for `clear_queue` Function

## Symbolic Inputs
| Variable             | Symbol   | Type                 |
|----------------------|----------|----------------------|
| state                | S1       | Object (PlayerState) |
| state.tracks         | S2       | List (or Variant)    |
| state.current_index  | S3       | Integer              |
| state.is_playing     | S4       | Boolean              |
| state.is_paused      | S5       | Boolean              |

## Path Conditions (PCs)
| Path ID   | Condition                                                                            |
|-----------|--------------------------------------------------------------------------------------|
| PC_1      | S1 is None OR S1 is Primitive                                                        |
| PC_2      | NOT PC_1 AND (S2 is None)                                                            |
| PC_3      | NOT PC_1 AND NOT PC_2 AND (S2 is not List) AND (Conversion Fails)                    |
| PC_4      | NOT PC_1 AND NOT PC_2 AND ((S2 is List) OR (Conversion Succeeds)) AND (len(S2) == 0) |
| PC_5      | NOT PC_4 AND (0 <= S3 < len(S2)) AND (Current Valid) AND (S4 OR S5)                  |
| PC_6      | NOT PC_4 AND (0 <= S3 < len(S2)) AND (Current Valid) AND (NOT S4 AND NOT S5)         |
| PC_7      | NOT PC_4 AND NOT (0 <= S3 < len(S2)) AND (NOT S4 AND NOT S5)                         |
