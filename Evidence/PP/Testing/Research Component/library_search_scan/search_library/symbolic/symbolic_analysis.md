# Symbolic Execution Analysis of `search_library`

## Symbolic Inputs
 | Variable                 | Symbol      | Type                   |
 |--------------------------|-------------|------------------------|
 | state                    | S1          | Object (PlayerState)   |
 | query                    | S2          | String                 |
 | state.library_tracks     | S3          | List                   |
 | t (iteration element)    | S4          | Object (Track)         |
 | t.title                  | S5          | StringOrNone           |
 | t.artist                 | S6          | StringOrNone           |
 | t.path                   | S7          | ObjectOrNone (Path)    |
 | t.path.name              | S8          | String                 |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                         |
|-----------|---------------------------------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                                        |
| PC_2      | NOT (S1 is None) AND NOT S2                                                                       |
| PC_3      | (Valid State) AND NOT hasattr(S1, 'library_tracks')                                               |
| PC_4      | (Valid State) AND hasattr(S1, 'library_tracks') AND NOT isinstance(S3, list)                      |
| PC_5      | (Valid State) AND isinstance(S3, list) AND (S3 is Empty OR No Match Found)                        |
| PC_6      | (Valid State) AND (S3 has S4) AND (S4 is None)                                                    |
| PC_7      | (Valid State) AND (S4 is Valid) AND (S2 in S5)                                                    |
| PC_8      | (Valid State) AND (S4 is Valid) AND NOT (S2 in S5) AND (S2 in S6)                                 |
| PC_9      | (Valid State) AND (S4 is Valid) AND NOT (S2 in S5) AND NOT (S2 in S6) AND (S7 Valid AND S2 in S8) |
| PC_10     | (Valid State) AND (S4 is Valid) AND NOT (S2 in S5) AND NOT (S2 in S6) AND NOT (Match Path)        |
