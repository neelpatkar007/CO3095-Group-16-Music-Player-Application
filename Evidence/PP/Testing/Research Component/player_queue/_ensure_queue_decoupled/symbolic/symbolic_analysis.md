# Symbolic Analysis for `_ensure_queue_decoupled`

## Symbolic Inputs
| Variable                                         | Symbol   | Type     | Description                                                                                 |
|--------------------------------------------------|----------|----------|---------------------------------------------------------------------------------------------|
| `hasattr(state, "tracks")`                       | S1       | Boolean  | Existence of the primary `tracks` attribute.                                                |
| `hasattr(state, "library_tracks")`               | S2       | Boolean  | Existence of the library reference attribute.                                               |
| `state.tracks is state.library_tracks`           | S3       | Boolean  | Identity check confirming if the queue references the library.                              |
| `state.tracks is not None`                       | S4       | Boolean  | Validation that the `tracks` object is instantiated.                                        |
| `isinstance(library_tracks, (list, tuple, set))` | S5       | Boolean  | Type check to determine if the library is iterable.                                         |
| `hasattr(state, "playlists")`                    | S6       | Boolean  | Existence of the playlists container.                                                       |
| ∃pl ∈ playlists : `pl.tracks is tracks`          | S7       | Boolean  | Existence of a playlist within the collection that shares identity with the current tracks. |

## Path Conditions (PCs)
| Path ID   | Condition                                                        |
|-----------|------------------------------------------------------------------|
| PC_1      | NOT S1 OR NOT S2                                                 |
| PC_2      | S1 AND S2 AND S3 AND S4 AND S5                                   |
| PC_3      | S1 AND S2 AND S3 AND S4 AND (NOT S5)                             |
| PC_4      | S1 AND S2 AND (NOT S3 OR NOT S4) AND (NOT S6 OR (S6 AND NOT S7)) |
| PC_5      | S1 AND S2 AND (NOT S3 OR NOT S4) AND S6 AND S7                   |