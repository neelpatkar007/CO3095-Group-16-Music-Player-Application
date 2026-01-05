# Symbolic Analysis for `_save_current_to_profile`

## Symbolic Inputs
| Variable                         | Symbol   | Type                 |
|----------------------------------|----------|----------------------|
| state                            | S1       | Object (PlayerState) |
| hasattr(state, "profiles")       | S2       | Boolean              |
| hasattr(state, "active_profile") | S3       | Boolean              |
| _serialize_current_state(state)  | S4       | Dict / None          |

## Path Conditions (PCs)
| Path ID   | Condition                           |
|-----------|-------------------------------------|
| PC_1      | S1 == None OR NOT S2 OR NOT S3      |
| PC_2      | S1 != None AND S2 AND S3 AND NOT S4 |
| PC_3      | S1 != None AND S2 AND S3 AND S4     |