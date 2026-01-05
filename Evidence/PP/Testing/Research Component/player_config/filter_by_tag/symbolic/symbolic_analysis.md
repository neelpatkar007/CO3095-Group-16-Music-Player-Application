# Symbolic Analysis for filter_by_tag Function

## Symbolic Inputs
| Variable  | Symbol  | Type                             |
|-----------|---------|----------------------------------|
| state     | S1      | PlayerState (Object) OR NoneType |
| tag       | S2      | str OR NoneType                  |

## Path Conditions (PCs)
| Path ID  | Condition                                                                                                             |
|----------|-----------------------------------------------------------------------------------------------------------------------|
| PC_1     | S1 == None                                                                                                            |
| PC_2     | S1 != None AND (NOT hasattr(S1, "song_tags") OR NOT isinstance(S1.song_tags, dict))                                   |
| PC_3     | S1 != None AND Valid(S1.song_tags) AND (NOT hasattr(S1, "library_tracks") OR NOT isinstance(S1.library_tracks, list)) |
| PC_4     | S1 != None AND Valid(S1.song_tags) AND Valid(S1.library_tracks) AND S2 == None                                        |
| PC_5     | S1 != None AND Valid(S1.song_tags) AND Valid(S1.library_tracks) AND S2 != None AND Matches == Empty                   |
| PC_6     | S1 != None AND Valid(S1.song_tags) AND Valid(S1.library_tracks) AND S2 != None AND Matches != Empty                   |