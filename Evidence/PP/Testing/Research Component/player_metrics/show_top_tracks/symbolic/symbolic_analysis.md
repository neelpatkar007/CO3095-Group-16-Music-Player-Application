# Symbolic Analysis for `show_top_tracks` Function

## Symbolic Inputs
| Variable                          | Symbol  | Type                                        |
|-----------------------------------|---------|---------------------------------------------|
| state                             | S1      | PlayerState (Object OR None)                |
| state.play_counts (Existence)     | S2      | Boolean (HasAttr AND Not None)              |
| state.play_counts (Type Validity) | S3      | Boolean (Is Dict)                           |
| state.play_counts (Is Empty)      | S4      | Boolean (True if Empty)                     |
| Sorting Operation (Success)       | S5      | Boolean (True = Success, False = Exception) |
| Loop Control (i < 10)             | S6      | Boolean (True = Continue, False = Break)    |
| Count Validity (count > 0)        | S7      | Boolean (True = Valid, False = Skip)        |
| Library Resolution (Found)        | S8      | Boolean (True = Name Resolved)              |

## Path Conditions (PCs)
| Path ID   | Condition                                   |
|-----------|---------------------------------------------|
| PC_1      | S1 == None                                  |
| PC_2      | (S1 != None) AND (NOT S2)                   |
| PC_3      | ... AND S2 AND (NOT S3) (Corrupt)           |
| PC_4      | ... AND S3 AND S4 (Empty)                   |
| PC_5      | ... AND (NOT S4) AND (NOT S5) (Sort Fail)   |
| PC_6      | ... AND S5 AND (NOT S6) (Limit Reached)     |
| PC_7      | ... AND S5 AND S6 AND (NOT S7) (Zero Count) |
| PC_8      | ... AND S5 AND S6 AND S7 (Valid Display)    |