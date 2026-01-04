# Symbolic Analysis of view_artists_table Function

## Symbolic Inputs
| Variable              | Symbol   | Type                             | 
|-----------------------|----------|----------------------------------|
| state                 | S1       | PlayerState (Object) or NoneType |
| state.library_tracks  | S2       | List[Track]                      |
| t                     | S3       | Track (Object) or NoneType       |
| t.artist              | S4       | String or NoneType               |  
| by_artist             | S5       | Dictionary (Derived)             | 

## Path Conditions
| Path ID   | Condition                                                         |
|-----------|-------------------------------------------------------------------|
| PC_1      | S1 == None                                                        |
| PC_2      | S1 != None AND NOT hasattr(S1, library_tracks)                    |
| PC_3      | S1 != None AND hasattr(S1, library_tracks) AND S2 is Empty        |
| PC_4      | PC_3_Base AND S3 is None                                          |
| PC_5      | PC_3_Base AND S3 != None AND NOT hasattr(S3, artist)              |
| PC_6      | PC_3_Base AND S3 != None AND hasattr(S3, artist) AND S4 is None   |
| PC_7      | PC_3_Base AND S3 != None AND S4 != None AND str(S4).strip() == "" |
| PC_8      | PC_3_Base AND S3 != None AND S4 != None AND str(S4).strip() != "" |

