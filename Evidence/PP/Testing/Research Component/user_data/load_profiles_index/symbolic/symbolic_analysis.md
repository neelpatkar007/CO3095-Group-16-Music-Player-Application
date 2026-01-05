# Symbolic Analysis for `load_profiles_index` Function

## Symbolic Inputs
| Variable              | Symbol  | Type                 |
|-----------------------|---------|----------------------|
| state                 | S1      | Object (PlayerState) |
| PROFILE_FILE.exists() | S2      | Boolean              |
| json.load(f)          | S3      | Dictionary / Other   |
| data["active"]        | S4      | String               |
| data["profiles"]      | S5      | Dictionary           |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                 |
|-----------|-------------------------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                                |
| PC_2      | NOT S1 is None AND NOT S2                                                                 |
| PC_3      | NOT S1 is None AND S2 AND NOT S3                                                          |
| PC_4      | NOT S1 is None AND S2 AND S3 AND S4 in S5                                                 |
| PC_7      | NOT S1 is None AND S2 AND S3 AND NOT S4 in S5 AND S4 == 'default' AND NOT 'default' in S5 |