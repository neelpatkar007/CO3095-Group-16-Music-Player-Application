# Symbolic Analysis for record_play Function

## Symbolic Inputs
| Variable                       | Symbol   | Type                           |
|--------------------------------|----------|--------------------------------|
| state                          | S1       | PlayerState (Object OR None)   |
| state.current_track            | S2       | Boolean (HasAttr AND Truthy)   |
| track.path                     | S3       | Boolean (HasAttr)              |
| state.play_counts (Existence)  | S4       | Boolean (HasAttr AND Not None) |
| Existing Count Type (Sanity)   | S5       | Boolean (Is Instance Int)      |

## Path Conditions (PCs)
| Path ID  | Condition                                            |
|----------|------------------------------------------------------|
| PC_1     | S1 == None                                           |
| PC_2     | (S1 != None) AND (NOT HasAttr(current_track))        |
| PC_3     | (S1 != None) AND HasAttr(current_track) AND (NOT S2) |
| PC_4     | (S1 != None) AND S2 AND (NOT S3)                     |
| PC_5     | ... AND S3 AND (NOT S5) (Corrupt Count Reset)        |
| PC_6     | ... AND S3 AND S5 (Normal Increment)                 |