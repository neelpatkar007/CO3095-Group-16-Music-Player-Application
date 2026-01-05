# Symbolic Execution Analysis: `total_duration_seconds`

## Symbolic Inputs
| Variable            | Symbol  | Type      | Description                                            |
|---------------------|---------|-----------|--------------------------------------------------------|
| self.tracks         | S1      | Iterable  | A list or iterable of track objects                    |
| t.duration_seconds  | S2      | Any       | The duration attribute of the current track object `t` |


## Path Conditions (PCs)
| Path ID  | Condition                                         | Explanation                                                                  |
|----------|---------------------------------------------------|------------------------------------------------------------------------------|
| PC_1     | S1 is Empty                                       | The loop is never entered; the initial total (`0.0`) is returned immediately |
| PC_2     | S1 NOT Empty AND NOT (S2 is numeric)              | The loop is entered, but `duration_seconds` is `None` or a non-numeric type  |
| PC_3     | S1 NOT Empty AND (S2 is numeric) AND NOT (S2 > 0) | The attribute is numeric but violates the positive value constraint (`≤ 0`)  |
| PC_4     | S1 NOT Empty AND (S2 is numeric) AND (S2 > 0)     | All constraints are satisfied; the value `S2` is added to the total          |