# Path Analysis for update_metadata Function

## Symbolic Inputs
| Variable             | Symbol  | Type    | Description                   |
|----------------------|---------|---------|-------------------------------|
| index_str            | S1      | String  | User input for track index    |
| field                | S2      | String  | Metadata key (title/artist)   |
| value                | S3      | String  | New metadata content          |
| state.library_tracks | S4      | List    | Current application state     |
| os.access            | S5      | Boolean | File system permission status |
| import mutagen       | S6      | Boolean | Library availability          |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                                |
|-----------|----------------------------------------------------------------------------------------------------------|
| PC_1      | S1 == ""                                                                                                 |
| PC_2      | NOT (S1 is Digit) OR (S1 - 1) < 0 OR (S1 - 1) >= length(S4)                                              |
| PC_3      | NOT S1 == "" AND PC_2 is False AND (S3 == "" OR S3 == " ")                                               |
| PC_4      | NOT S1 == "" AND PC_2 is False AND PC_3 is False AND (S2 != "title" AND S2 != "artist")                  |
| PC_5      | NOT S1 == "" AND PC_2 is False AND PC_3 is False AND (S2 == "title" OR S2 == "artist") AND NOT S5        |
| PC_6      | NOT S1 == "" AND PC_2 is False AND PC_3 is False AND (S2 == "title" OR S2 == "artist") AND S5 AND NOT S6 |
| PC_7      | NOT S1 == "" AND PC_2 is False AND PC_3 is False AND (S2 == "title" OR S2 == "artist") AND S5 AND S6     |