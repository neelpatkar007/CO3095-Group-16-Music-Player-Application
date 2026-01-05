# Symbolic Analysis of `_print_playlist_contents` Function

### Symbolic Inputs
| Variable    | Symbol   | Type             | Description                                                                    |
|-------------|----------|------------------|--------------------------------------------------------------------------------|
| pl.tracks   | S1       | Iterable/Boolean | Represents the list of tracks. Evaluates to False if empty, True if populated. |
| track.attr  | S2       | Object           | Represents internal attributes (duration, name) accessed if `S1` is True.      |

### Path Conditions (PCs)
| Path ID  | Condition  | Logic Description                                                                                          |
|----------|------------|------------------------------------------------------------------------------------------------------------|
| PC_1     | NOT S1     | The track list is empty or None-like, triggering the early return.                                         |
| PC_2     | S1         | The track list contains at least one element, bypassing the guard clause and entering the iteration logic. |
