# Symbolic Execution Analysis: `sort_playlist`

## Symbolic Inputs
| Variable                  | Symbol   | Type        |
|---------------------------|----------|-------------|
| state                     | S1       | PlayerState |
| selector                  | S2       | str         |
| criteria                  | S3       | str         |
| _resolve_playlist(S1, S2) | S4       | Playlist    |
| S4.tracks                 | S5       | List        |
| criteria (normalized)     | S6       | str         |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                        |
|-----------|--------------------------------------------------------------------------------------------------|
| PC_1      | S1 is None                                                                                       |
| PC_2      | NOT (S1 is None) AND (NOT S2 OR S2 is Whitespace)                                                |
| PC_3      | NOT (PC_1 OR PC_2) AND (NOT S3 OR Type(S3) != str)                                               |
| PC_4      | NOT (PC_1 OR PC_2 OR PC_3) AND (S4 is None)                                                      |
| PC_5      | NOT PC_4 AND (NOT hasattr(S4, tracks) OR S5 is None)                                             |
| PC_6      | NOT PC_5 AND (S5 is Empty)                                                                       |
| PC_7      | NOT PC_6 AND (S6 == "title") AND (Sort Success)                                                  |
| PC_8      | NOT PC_6 AND (S6 == "title") AND (Sort Exception Raised)                                         |
| PC_9      | NOT PC_6 AND (S6 != "title" AND S6 == "artist") AND (Sort Success)                               |
| PC_10     | NOT PC_6 AND (S6 != "title" AND S6 == "artist") AND (Sort Exception Raised)                      |
| PC_11     | NOT PC_6 AND (S6 != "title" AND S6 != "artist" AND S6 == "duration") AND (Sort Success)          |
| PC_12     | NOT PC_6 AND (S6 != "title" AND S6 != "artist" AND S6 == "duration") AND (Sort Exception Raised) |
| PC_13     | NOT PC_6 AND (S6 != "title" AND S6 != "artist" AND S6 != "duration")                             |