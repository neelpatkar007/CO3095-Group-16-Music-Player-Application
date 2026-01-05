# Symbolic Analysis of `create_profile` Function

## Symbolic Inputs

| Variable   | Symbol   | Type                 |
|------------|----------|----------------------|
| state      | S1       | PlayerState (Object) |
| name       | S2       | String               |


## Path Conditions (PCs)
| Path ID  | Condition                                                                                                                               |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------|
| PC_1     | S1 is None OR NOT hasattr S1, 'profiles'                                                                                                |
| PC_2     | NOT (S1 is None OR NOT hasattr S1, 'profiles') AND (NOT S2 OR NOT isinstance S2, str)                                                   |
| PC_3     | NOT (S1 is None OR NOT hasattr S1, 'profiles') AND NOT (NOT S2 OR NOT isinstance S2, str) AND S2 == 'default'                           |
| PC_4     | NOT (S1 is None OR NOT hasattr S1, 'profiles') AND NOT (NOT S2 OR NOT isinstance S2, str) AND S2 != 'default' AND S2 IN S1.profiles     |
| PC_5     | NOT (S1 is None OR NOT hasattr S1, 'profiles') AND NOT (NOT S2 OR NOT isinstance S2, str) AND S2 != 'default' AND S2 NOT IN S1.profiles |
