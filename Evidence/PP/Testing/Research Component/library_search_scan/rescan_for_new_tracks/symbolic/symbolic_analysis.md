# Symbolic Execution Analysis of `rescan_for_new_tracks`

## Symbolic Inputs
| Variable             | Symbol  | Type   | Description                                    |
|----------------------|---------|--------|------------------------------------------------|
| state                | S1      | Object | None                                           |
| discover_tracks()    | S2      | List   | None                                           |
| state.library_tracks | S3      | List   | The internal list of tracks existing within S1 |

## Path Conditions
| Path ID   | Condition                                                                       |
|-----------|---------------------------------------------------------------------------------|
| PC_1      | S1 == None                                                                      |
| PC_2      | S1 != None AND (NOT S2 OR S2 is Empty)                                          |
| PC_3      | S1 != None AND S2 has items AND (Intersection of S2 and S3 result is Empty)     |
| PC_4      | S1 != None AND S2 has items AND (Intersection of S2 and S3 result is NOT Empty) |