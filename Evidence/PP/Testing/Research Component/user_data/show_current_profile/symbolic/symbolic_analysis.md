# Symbolic Analysis for show_current_profile Function

## Symbolic Inputs
To perform a formal analysis, the input parameter state is decomposed into its symbolic constituents.

| Variable                         | Symbol   | Type          |
|----------------------------------|----------|---------------|
| state                            | S1       | Object / None |
| hasattr(state, "active_profile") | S2       | Boolean       |


## Path Conditions (PCs)
| Path ID   | Condition               |
|-----------|-------------------------|
| PC_1      | S1 == None OR NOT S2    |
| PC_2      | NOT (S1 == None) AND S2 |
