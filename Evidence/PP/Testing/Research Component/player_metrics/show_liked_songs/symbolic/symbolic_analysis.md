# Symbolic Analysis for `show_liked_songs` Function

## Symbolic Inputs
| Variable                           | Symbol  | Type                                |
|------------------------------------|---------|-------------------------------------|
| state                              | S1      | PlayerState (Object OR None)        |
| state.liked_tracks (Data Exists)   | S2      | Boolean (HasAttr AND Not None)      |
| state.liked_tracks (Is Empty)      | S3      | Boolean (True if Empty)             |
| state.library_tracks (Data Exists) | S4      | Boolean (HasAttr AND Not None)      |
| state.library_tracks (Type Valid)  | S5      | Boolean (Is List)                   |
| Track Validity (Inside Loop)       | S6      | Boolean (Item is valid)             |
| Match Found (path in likes)        | S7      | Boolean (True = Match)              |
| found_count == 0                   | S8      | Boolean (True = No Matches Printed) |


## Path Conditions (PCs)
| Path ID   | Condition                                    |
|-----------|----------------------------------------------|
| PC_1      | S1 == None                                   |
| PC_2      | (S1 != None) AND (NOT S2)                    |
| PC_3      | ... AND S2 AND S3 (Empty Set)                |
| PC_4      | ... AND (NOT S3) AND (NOT S4) (Lib Missing)  |
| PC_5      | ... AND S4 AND (NOT S5) (Lib Corrupt)        |
| PC_6      | ... AND S5 AND (Loop runs) AND (S8 is True)  |
| PC_7      | ... AND S5 AND (Loop runs) AND (S8 is False) |