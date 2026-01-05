# Concolic Testing Analysis: `_get_playlist_summary`

## Path Exploration Table

| Iteration   | Concrete Seed (S1, S2, S3)   | Path Taken           | Constraint to Flip           | New Derived Input            |
|:------------|:-----------------------------|:---------------------|:-----------------------------|:-----------------------------|
| 1           | [] (Empty List)              | PC_1 (Early Return)  | Flip (NOT S1) -> S1          | [Track()] (List with 1 item) |
| 2           | [Track(no_attr)]             | PC_2 (Invalid Track) | Flip (Validation False)      | [Track(duration=-5)]         |
| 3           | [Track(duration=-5)]         | PC_2 (Negative Val)  | Flip (S3 < 0) -> S3 >= 0     | [Track(duration=180)]        |
| 4           | [Track(duration=180)]        | PC_3 (Valid Track)   | None (All branches explored) | N/A                          |

