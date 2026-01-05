# Symbolic Analysis for import_song Function

## Symbolic Inputs
| Variable                        | Symbol   | Type                                          |
|---------------------------------|----------|-----------------------------------------------|
| source_path_str                 | S1       | String                                        |
| src.exists()                    | S2       | Boolean                                       |
| src.is_file()                   | S3       | Boolean                                       |
| src.stat().st_size              | S4       | Integer                                       |
| src.suffix.lower()              | S5       | String                                        |
| MUSIC_DIR.exists()              | S6       | Boolean                                       |
| dest.exists()                   | S7       | Boolean                                       |
| shutil.copy2 (Exception Status) | S8       | Integer (0: Success, 1: Permission, 2: Other) |
| imported_track                  | S9       | Object / Optional                             |

## Path Conditions (PCs)
| Path ID   | Condition                                                                          |
|-----------|------------------------------------------------------------------------------------|
| PC_1      | NOT S1                                                                             |
| PC_2      | S1 AND NOT S2                                                                      |
| PC_3      | S1 AND S2 AND NOT S3                                                               |
| PC_4      | S1 AND S2 AND S3 AND S4 == 0                                                       |
| PC_5      | S1 AND S2 AND S3 AND S4 != 0 AND S5 NOT IN SUPPORTED                               |
| PC_6      | S1 AND S2 AND S3 AND S4 != 0 AND S5 IN SUPPORTED AND S7                            |
| PC_7      | S1 AND S2 AND S3 AND S4 != 0 AND S5 IN SUPPORTED AND NOT S7 AND S8 == 1            |
| PC_8      | S1 AND S2 AND S3 AND S4 != 0 AND S5 IN SUPPORTED AND NOT S7 AND S8 == 2            |
| PC_9      | S1 AND S2 AND S3 AND S4 != 0 AND S5 IN SUPPORTED AND NOT S7 AND S8 == 0 AND S9     |
| PC_10     | S1 AND S2 AND S3 AND S4 != 0 AND S5 IN SUPPORTED AND NOT S7 AND S8 == 0 AND NOT S9 |
