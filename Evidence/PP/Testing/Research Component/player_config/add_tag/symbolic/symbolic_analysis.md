# Symbolic Analysis for add_tag Function

## Symbolic Inputs
| Variable                  | Symbol   | Type                         |
|---------------------------|----------|------------------------------|
| state                     | S1       | PlayerState object (or None) |
| index_str                 | S2       | String (or None)             |
| tag                       | S3       | String (or None)             |
| state.song_tags           | S4       | Dictionary                   |
| state.library_tracks      | S5       | List[Track]                  |
| len(state.library_tracks) | S6       | Integer                      |
| state.library_tracks[idx] | S7       | Track object (or None)       |

## Path Conditions (PCs)
| Path ID  | Condition                                                                  |
|----------|----------------------------------------------------------------------------|
| PC_1     | S1 == None                                                                 |
| PC_2     | S1 != None AND (S2 is None OR NOT IsInt(S2))                               |
| PC_3     | S1 != None AND IsInt(S2) AND (S4 is Missing OR Not Dict)                   |
| PC_4     | PC_3_Prefix AND S4 Valid AND (S5 is Missing OR Not List)                   |
| PC_5     | PC_4_Prefix AND S5 Valid AND (Idx < 0 OR Idx >= S6)                        |
| PC_6     | PC_5_Prefix AND (Idx >= 0 AND Idx < S6) AND S7 is None                     |
| PC_7     | PC_6_Prefix AND S7 != None AND S3 is None                                  |
| PC_8     | PC_7_Prefix AND S3 != None AND Length(Clean(S3)) > 15                      |
| PC_9     | PC_8_Prefix AND Length(Clean(S3)) <= 15 AND ContainsInvalidChar(Clean(S3)) |
| PC_10    | PC_9_Prefix AND AllCharsValid(Clean(S3)) AND Count(Tags) >= 5              |
| PC_11    | PC_10_Prefix AND Count(Tags) < 5 AND Clean(S3) IN Tags                     |
| PC_12    | PC_10_Prefix AND Count(Tags) < 5 AND Clean(S3) NOT IN Tags                 |