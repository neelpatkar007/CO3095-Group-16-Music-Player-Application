# Concolic Analysis of `change_volume` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2)           | Path Taken            | Constraint to Flip           | New Derived Input                          |
|:-----------|:---------------------------------|:----------------------|:-----------------------------|:-------------------------------------------|
| 1          | S1=None, S2="50"                 | PC_1 (Early Return)   | S1 == None                   | S1 = PlayerState(), S2 = "50"              |
| 2          | S1=PlayerState(no attr), S2="50" | PC_2 (Missing Attr)   | hasattr(S1, 'volume')...     | S1 = PlayerState(vol=10, eng=E), S2 = "50" |
| 3          | S1=Valid, S2=""                  | PC_3 (Show Vol)       | NOT S2                       | S1 = Valid, S2 = [] (List)                 |
| 4          | S1=Valid, S2=[]                  | PC_4 (Type Error)     | isinstance(S2, ...)          | S1 = Valid, S2 = "invalid_int"             |
| 5          | S1=Valid, S2="abc"               | PC_5 (Val Error)      | int(S2) throws               | S1 = Valid, S2 = "-1"                      |
| 6          | S1=Valid, S2="-1"                | PC_6 (Range Error)    | 0 <= val <= 100              | S1 = Valid, S2 = "50"                      |
| 7          | S1=Valid(muted), S2="50"         | PC_7 (Success+Unmute) | is_muted == True             | S1 = Valid(unmuted), S2 = "50"             |
| 8          | S1=Valid(unmuted), S2="50"       | PC_8 (Success)        | None (All branches explored) | N/A                                        |