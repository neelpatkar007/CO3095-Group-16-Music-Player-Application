# Symbolic Analysis for `_get_playlist` Function

## Symbolic Inputs
| Variable                          | Symbol  | Type                 |
|-----------------------------------|---------|----------------------|
| state                             | S1      | PlayerState (Object) |
| selector                          | S2      | String               |
| _resolve_playlist (Return Value)  | S3      | Object (Playlist)    |
| state.playlists (Inclusion Check) | S4      | Boolean (Inferred)   |

## Path Conditions (PCs)
| Path ID  | Condition                                              |
|----------|--------------------------------------------------------|
| PC_1     | S1 == None                                             |
| PC_2     | S1 != None AND S2 == ""                                |
| PC_3     | S1 != None AND S2 != "" AND S3 == None                 |
| PC_4     | S1 != None AND S2 != "" AND S3 != None AND S4 == False |
| PC_5     | S1 != None AND S2 != "" AND S3 != None AND S4 == True  |