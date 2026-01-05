# Concolic Analysis Report
# for advanced_search Function

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2)         | Path Taken              | Constraint to Flip               | New Derived Input                  |
|-----------|--------------------------------|-------------------------|----------------------------------|------------------------------------|
| 1         | (None, "test")                 | PC_1 (Early Return)     | Flip (S1 is None)                | (ValidState, "test")               |
| 2         | (ValidState, None)             | PC_3 (Usage Info)       | Flip (S2 is None)                | (ValidState, "artist:Linkin_Park") |
| 3         | (ValidState, "artist:LP")      | PC_6 (Filter + Display) | Flip (results is empty)          | (ValidState, "unknown_artist")     |
| 4         | (ValidState, "unknown_artist") | PC_5 (No Matches)       | Flip (token starts with artist:) | (ValidState, "duration>180")       |