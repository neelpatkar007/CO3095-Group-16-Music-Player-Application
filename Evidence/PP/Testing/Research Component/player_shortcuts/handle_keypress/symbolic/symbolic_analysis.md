# Symbolic Analysis of `handle_keypress` Function

## Symbolic Inputs
| Variable          | Symbol   | Type    |
|-------------------|----------|---------|
| key               | S1       | String  |
| state.tracks      | S2       | List    |
| state.is_playing  | S3       | Boolean |
| state.volume      | S4       | Integer |

## Path Conditions (PCs)
| Path ID   | Condition                                                         |
|-----------|-------------------------------------------------------------------|
| PC_1      | NOT S1                                                            |
| PC_2      | S1 == 'p' AND NOT S2                                              |
| PC_3      | S1 == 'p' AND S2 AND S3                                           |
| PC_4      | S1 == 'p' AND S2 AND NOT S3                                       |
| PC_5      | S1 == 's' AND S3                                                  |
| PC_6      | S1 == 's' AND NOT S3                                              |
| PC_7      | S1 == 'm'                                                         |
| PC_8      | S1 == '+' AND S4 < 100                                            |
| PC_9      | S1 == '+' AND S4 >= 100                                           |
| PC_10     | S1 == '-' AND S4 > 0                                              |
| PC_11     | S1 == '-' AND S4 <= 0                                             |
| PC_12     | S1 != 'p' AND S1 != 's' AND S1 != 'm' AND S1 != '+' AND S1 != '-' |
