# Symbolic Analysis for `_get_tracks_safe` Function

## Symbolic Inputs
| Variable    | Symbol  | Type                  |
|-------------|---------|-----------------------|
| state       | S1      | PlayerState (Object)  |
| raw_tracks  | S2      | Any (Derived from S1) |

## Path Conditions (PCs)
| Path ID   | Condition                                               |
|-----------|---------------------------------------------------------|
| PC_1      | S2 == None                                              |
| PC_2      | S2 != None AND type(S2) == list                         |
| PC_3      | S2 != None AND type(S2) != list AND is_iterable(S2)     |
| PC_4      | S2 != None AND type(S2) != list AND NOT is_iterable(S2) |
