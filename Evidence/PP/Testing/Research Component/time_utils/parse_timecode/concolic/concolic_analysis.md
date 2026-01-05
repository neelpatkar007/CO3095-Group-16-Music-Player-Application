# Concolic Analysis of `parse_timecode` Function

## Path Exploration Table
| Iteration | Concrete Seed (S1)   | Path Taken  | Constraint to Flip  | New Derived Input   |
|-----------|----------------------|-------------|---------------------|---------------------|
| 1         | ""                   | PC_1        | text.strip != ""    | 10:00               |
| 2         | 10:00                | PC_4        | ":" NOT IN text     | 60                  |
| 3         | 60                   | PC_4        | total < 0           | -5                  |
| 4         | -5                   | PC_3        | Exception trigger   | invalid_str         |
| 5         | 1:2:3                | PC_2        | len(parts) == 2     | 5:30                |
