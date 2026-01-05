# Symbolic Analysis for list_all_tags Function

## Symbolic Inputs
| Variable                 | Symbol  | Type / Domain                    |
|--------------------------|---------|----------------------------------|
| state                    | S1      | Object OR None                   |
| state.song_tags          | S2      | Dictionary OR Other OR Undefined |
| state.library_tracks     | S3      | List OR Other OR Undefined       |
| state.song_tags.values() | S4      | Collection of Lists              |


## Path Conditions (PCs)
| Path ID  | Condition                                                                                                                              |
|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| PC_1     | S1 == None                                                                                                                             |
| PC_2     | S1 != None AND (NOT hasattr(S1, "song_tags") OR NOT isinstance(S2, dict))                                                              |
| PC_3     | S1 != None AND (hasattr(S1, "song_tags") AND isinstance(S2, dict)) AND (NOT hasattr(S1, "library_tracks") OR NOT isinstance(S3, list)) |
| PC_4     | S1 != None AND Valid_Structure(S2, S3) AND (Union(S4) == Empty)                                                                        |
| PC_5     | S1 != None AND Valid_Structure(S2, S3) AND (Union(S4) != Empty)                                                                        |