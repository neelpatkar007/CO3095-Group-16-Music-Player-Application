# Symbolic Analysis of `display_name` Method

## Symbolic Inputs
| Variable      | Symbol  | Type          | Description                         |
|---------------|---------|---------------|-------------------------------------|
| self.title    | S1      | String        | The primary identifier of the track |
| self.artist   | S2      | String / None | Artist metadata (truthy or falsy)   |

## Path Conditions (PCs)
| Path ID   | Condition  | Resulting State   |
|-----------|------------|-------------------|
| PC_1      | S2         | `S1 – S2`         |
| PC_2      | NOT S2     | `S1`              |