# Symbolic Analysis for `show_current_playlist` Function

## Symbolic Inputs
| Variable                     | Symbol   | Type    | Description                                                                |
|------------------------------|----------|---------|----------------------------------------------------------------------------|
| state                        | S1       | Object  | None                                                                       |
| hasattr(state, "playlists")  | S2       | Boolean | Predicate checking if the state object possesses the 'playlists' attribute |
| state.active_playlist_index  | S3       | Integer | None if no active index selected                                           |
| state.playlists (Truthiness) | S4       | Boolean | Evaluates to True if the list is populated, False if empty                 |

## Path Conditions (PCs)
| Path ID  | Condition                                   | Logic Justification                                                                    |
|----------|---------------------------------------------|----------------------------------------------------------------------------------------|
| PC_1     | S1 == None                                  | The state object itself is null; execution terminates immediately at the first check.  |
| PC_2     | S1 != None AND NOT S2                       | The state exists, but lacks the required `playlists` attribute.                        |
| PC_3     | S1 != None AND S2 AND S3 == None            | State and attributes exist, but no active index is selected (`None`).                  |
| PC_4     | S1 != None AND S2 AND S3 != None AND NOT S4 | An index is selected, but the playlist collection itself evaluates to `False` (empty). |
| PC_5     | S1 != None AND S2 AND S3 != None AND S4     | All guard clauses are satisfied; the function proceeds to display the playlist.        |