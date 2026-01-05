# Symbolic Analysis: merge_playlists Function

## Symbolic Inputs
| Variable                     | Symbol   | Type            |
|------------------------------|----------|-----------------|
| `target_selector`            | S1       | String          |
| `source_selector`            | S2       | String          |
| `target_playlist_obj`        | S3       | Playlist / None |
| `source_playlist_obj`        | S4       | Playlist / None |
| `source_playlist_obj.tracks` | S5       | List[Track]     |
| `dedupe`                     | S6       | Boolean         |

## Path Conditions (PCs)
| Path ID   | Condition                                                        |
|-----------|------------------------------------------------------------------|
| PC_1      | S1 == "" OR S1 == " "                                            |
| PC_2      | NOT (S1 == "" OR S1 == " ") AND (S2 == "" OR S2 == " ")          |
| PC_3      | NOT PC_1 AND NOT PC_2 AND S3 == None                             |
| PC_4      | NOT PC_1 AND NOT PC_2 AND S3 != None AND S4 == None              |
| PC_5      | NOT PC_1 AND NOT PC_2 AND S3 != None AND S4 != None AND S3 == S4 |
| PC_6      | NOT PC_1 AND NOT PC_2 AND S3 != S4 AND S5 is Empty               |
| PC_7      | NOT PC_1 AND NOT PC_2 AND S3 != S4 AND S5 NOT Empty              |
