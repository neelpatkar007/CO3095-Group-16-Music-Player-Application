# Symbolic Analysis of `add_track_from_library` Function

## Symbolic Inputs
| Variable          | Symbol  | Type        |
|-------------------|---------|-------------|
| state             | S1      | PlayerState |
| playlist_selector | S2      | String      |
| library_index_str | S3      | String      |

## Path Conditions (PCs)
| Path ID   | Condition                                                                                                                                              |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| PC_1      | S1 == None                                                                                                                                             |
| PC_2      | S1 != None AND NOT S2                                                                                                                                  |
| PC_3      | S1 != None AND S2 AND NOT S3                                                                                                                           |
| PC_4      | S1 != None AND S2 AND S3 AND NOT S1.tracks                                                                                                             |
| PC_5      | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) == None                                                                               |
| PC_6      | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) != None AND NOT is_int(S3)                                                            |
| PC_7      | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) != None AND is_int(S3) AND NOT in_bounds(S3)                                          |
| PC_8      | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) != None AND is_int(S3) AND in_bounds(S3) AND track == None                            |
| PC_9      | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) != None AND is_int(S3) AND in_bounds(S3) AND track != None AND track.display_name     |
| PC_10     | S1 != None AND S2 AND S3 AND S1.tracks AND _get_playlist(S1, S2) != None AND is_int(S3) AND in_bounds(S3) AND track != None AND NOT track.display_name |