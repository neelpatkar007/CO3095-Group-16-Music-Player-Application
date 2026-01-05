# Symbolic Analysis of `show_queue` Function

## Symbolic Inputs
| Variable             | Symbol   | Type        |
|----------------------|----------|-------------|
| state                | S1       | PlayerState |
| _get_tracks_safe(S1) | S2       | List[Track] |
| state.current_index  | S3       | int         |
| state.is_playing     | S4       | bool        |
| state.is_paused      | S5       | bool        |
| state.shuffle_active | S6       | bool        |


## Path Conditions (PCs)
| Path ID   | Condition                                         |
|-----------|---------------------------------------------------|
| PC_1      | S1 is None OR type(S1) IN {str, int, float, bool} |
| PC_2      | NOT PC_1 AND (Normalised S3 >= Len(S2))           |
| PC_3      | NOT PC_2 AND S4                                   |
| PC_4      | NOT PC_2 AND NOT S4 AND S5                        |
| PC_5      | NOT PC_2 AND NOT S4 AND NOT S5                    |