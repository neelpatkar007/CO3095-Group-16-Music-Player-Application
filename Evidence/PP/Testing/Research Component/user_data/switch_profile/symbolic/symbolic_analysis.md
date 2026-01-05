# Symbolic Analysis of `switch_profile` Function

## Symbolic Inputs
| Variable             | Symbol   | Type        |
|----------------------|----------|-------------|
| state                | S1       | PlayerState |
| name                 | S2       | string      |
| state.profiles       | S3       | dict        |
| state.active_profile | S4       | string      |


## Path Conditions (PCs)
| Path ID   | Condition                                                                      |
|-----------|--------------------------------------------------------------------------------|
| PC_1      | S1 == None OR NOT hasattr(S1, 'profiles') OR NOT hasattr(S1, 'active_profile') |
| PC_2      | NOT (PC_1) AND (S2 NOT in S3 AND S2 != 'default')                              |
| PC_3      | NOT (PC_1 OR PC_2) AND (S2 == S4)                                              |
| PC_4      | NOT (PC_1 OR PC_2 OR PC_3) AND (S2 in S3)                                      |
| PC_5      | NOT (PC_1 OR PC_2 OR PC_3) AND (S2 NOT in S3)                                  |