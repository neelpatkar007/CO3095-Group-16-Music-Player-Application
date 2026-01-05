# Symbolic Analysis of `_apply_profile_data`

## Symbolic Inputs

| Variable             | Symbol  | Type               |
|----------------------|---------|--------------------|
| state                | S1      | PlayerState / None |
| data                 | S2      | dict / None        |
| state.library_tracks | S3      | list               |
| p_dict.get("tracks") | S4      | list               |

## Path Conditions (PCs)
| Path ID   | Condition                              |
|-----------|----------------------------------------|
| PC_1      | S1 == None                             |
| PC_2      | S1 != None AND NOT S2                  |
| PC_3      | S1 != None AND S2 AND NOT S2 playlists |
| PC_4      | S1 != None AND S2 AND S2 playlists     |
