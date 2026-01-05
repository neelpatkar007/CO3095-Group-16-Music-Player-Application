# Symbolic Analysis for `_get_playlist_summary` in `playlists_basic`

## Symbolic Inputs
| Variable               | Symbol   | Type         |
|------------------------|----------|--------------|
| pl.tracks              | S1       | List[Track]  |
| track (element of S1)  | S2       | Object       |
| track.duration_seconds | S3       | int or float |


## Path Conditions (PCs)

| Path ID  | Condition                                        |
|----------|--------------------------------------------------|
| PC_1     | NOT S1                                           |
| PC_2     | S1 AND (NOT HasAttr OR NOT IsInstance OR S3 < 0) |
| PC_3     | S1 AND (HasAttr AND IsInstance AND S3 >= 0)      |

