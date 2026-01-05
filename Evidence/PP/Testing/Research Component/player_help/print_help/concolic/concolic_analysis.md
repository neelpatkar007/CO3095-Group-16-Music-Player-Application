# Concolic Analysis of `print_help` Function

## Path Exploration Table
| Iteration  | Concrete Seed ($S_1$)   | Path Taken         | Constraint to Flip                     | New Derived Input   |
|:-----------|:------------------------|:-------------------|:---------------------------------------|:--------------------|
| 1          | "undefined_val"         | PC_ELSE (Fallback) | $T$ != "quit" -> $T$ == "quit"         | "quit"              |
| 2          | "quit"                  | PC_QUIT            | $T$ != "list" -> $T$ == "list"         | "list"              |
| 3          | "list"                  | PC_LIST            | $T$ != "bar" -> $T$ == "bar"           | "bar"               |
| 4          | "bar"                   | PC_BAR             | $T$ != "progress" -> $T$ == "progress" | "progress"          |
| 5          | "progress"              | PC_PROGRESS        | $T$ != "info" -> $T$ == "info"         | "info"              |
| ...        | ...                     | ...                | ...                                    | ...                 |
| 48         | "volume"                | PC_10 (Volume)     | $T$ == "volume" -> $T$ == "ff"         | "ff"                |
| 49         | "play"                  | PC_2 (Play)        | $T$ == "play" -> $S_1$ is None         | None                |