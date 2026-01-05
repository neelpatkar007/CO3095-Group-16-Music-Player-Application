# Symbolic Analysis for `change_volume` Function

## Symbolic Inputs
| Variable    | Symbol  | Type                         |
|-------------|---------|------------------------------|
| state       | S1      | Object (PlayerState) OR None |
| raw_input   | S2      | str OR int OR float OR Any   |


## Path Conditions (PCs)
| Path ID  | Condition                                                                     |
|----------|-------------------------------------------------------------------------------|
| PC_1     | S1 == None                                                                    |
| PC_2     | S1 != None AND (NOT hasattr(S1, 'volume') OR NOT hasattr(S1, 'audio_engine')) |
| PC_3     | S1 valid AND NOT S2 (Empty/None)                                              |
| PC_4     | S1 valid AND S2 valid AND NOT isinstance(S2, [str, int, float])               |
| PC_5     | S1 valid AND S2 type valid AND int(S2) raises ValueError/TypeError            |
| PC_6     | S1 valid AND S2 is numeric AND NOT (0 <= int(S2) <= 100)                      |
| PC_7     | S1 valid AND S2 valid numeric AND range ok AND (S1.is_muted == True)          |
| PC_8     | S1 valid AND S2 valid numeric AND range ok AND (S1.is_muted == False)         |