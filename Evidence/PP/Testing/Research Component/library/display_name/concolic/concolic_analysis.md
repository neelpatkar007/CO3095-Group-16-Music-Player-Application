# Concolic Analysis of `display_name` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2)         | Path Taken                 | Constraint to Flip        | New Derived Input                |
|-------------|--------------------------------|----------------------------|---------------------------|----------------------------------|
| 1           | ("Bohemian Rhapsody", "")      | PC_2 (Else / Fall-through) | Flip `NOT S2`             | S2 must be non-empty → `"Queen"` |
| 2           | ("Bohemian Rhapsody", "Queen") | PC_1 (If Block)            | None (All paths explored) | N/A                              |