# Symbolic Analysis for `load_data` Function

## Symbolic Inputs
| Variable             | Symbol  | Type                                            |
|----------------------|---------|-------------------------------------------------|
| `state`              | S1      | `PlayerState` (Object OR `None`)                |
| `DATA_FILE.exists()` | S2      | Boolean                                         |
| File/JSON Integrity  | S3      | Boolean (`True` = Success, `False` = Exception) |

## Path Conditions (PCs)
| Path ID   | Condition                          |
|----------:|------------------------------------|
|      PC_1 | `(NOT S2) OR (S1 == None)`         |
|      PC_2 | `S2 AND (S1 != None) AND S3`       |
|      PC_3 | `S2 AND (S1 != None) AND (NOT S3)` |