# Symbolic Analysis for create_playlist Function

## Symbolic Inputs
| Variable   | Symbol   | Type        | Description                                                   |
|------------|----------|-------------|---------------------------------------------------------------|
| state      | S1       | PlayerState | The composite object holding the list of playlists.           |
| name       | S2       | str         | The raw string input representing the proposed playlist name. |


## Path Conditions (PCs)
| Path ID   | Condition                                                             |
|-----------|-----------------------------------------------------------------------|
| PC_1      | (S2 IS None) OR (S2 IS EmptyString)                                   |
| PC_2      | NOT PC_1 AND (EXISTS pl IN S1.playlists : pl.name.lower == S2.lower)  |
| PC_3      | NOT PC_1 AND (FOR ALL pl IN S1.playlists : pl.name.lower != S2.lower) |
