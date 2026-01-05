# Symbolic Analysis for play_active_playlist

### Symbolic Inputs
| Variable                    | Symbol  | Type                |
|-----------------------------|---------|---------------------|
| state.active_playlist_index | S1      | Integer OR NoneType |
| state.playlists             | S2      | List[Playlist]      |


### Path Conditions (PCs)
| Path ID   | Condition                      |
|-----------|--------------------------------|
| PC_1      | S1 == None                     |
| PC_2      | S1 != None AND S2 is Empty     |
| PC_3      | S1 != None AND S2 is NOT Empty |