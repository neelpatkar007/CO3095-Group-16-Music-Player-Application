# Symbolic Analysis of `view_rated` Function

## Symbolic Inputs
| Variable                       | Symbol   | Type                     |
|--------------------------------|----------|--------------------------|
| state                          | S1       | Optional[PlayerState]    |
| hasattr(state, "song_ratings") | S2       | bool                     |
| state.song_ratings             | S3       | Optional[Dict[str, Any]] |
| bool(state.song_ratings)       | S4       | bool                     |
| sorted() execution             | S5       | bool (Success/Failure)   |
| int(rating) conversion         | S6       | bool (Success/Failure)   |
| str(t.path) == path_str        | S7       | bool                     |


## Path Conditions (PCs)
| Path ID   | Condition                                            |
|-----------|------------------------------------------------------|
| PC_1      | S1 is None                                           |
| PC_2      | NOT S1 AND NOT S2                                    |
| PC_3      | NOT S1 AND S2 AND S3 is None                         |
| PC_4      | NOT S1 AND S2 AND NOT S3 AND NOT S4                  |
| PC_5      | NOT S1 AND S2 AND NOT S3 AND S4 AND NOT S5           |
| PC_6      | NOT S1 AND S2 AND NOT S3 AND S4 AND S5 AND NOT S6    |
| PC_7      | NOT S1 AND S2 AND NOT S3 AND S4 AND S5 AND S6 AND S7 |

