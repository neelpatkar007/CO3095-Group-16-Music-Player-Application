# Symbolic Analysis for list_profiles

## Symbolic Inputs
| Variable             | Symbol  | Type                  |
|----------------------|---------|-----------------------|
| state                | S1      | Optional[PlayerState] |
| state.profiles       | S2      | Dict[str, Any]        |
| state.active_profile | S3      | str                   |

## Path Conditions (PCs)
| Path ID   | Condition                                                                           |
|-----------|-------------------------------------------------------------------------------------|
| PC_1      | S1 == None OR NOT hasattr(S1, profiles) OR NOT hasattr(S1, active_profile)          |
| PC_2      | S1 != None AND hasattr(S1, profiles) AND hasattr(S1, active_profile) AND S3 == name |
| PC_3      | S1 != None AND hasattr(S1, profiles) AND hasattr(S1, active_profile) AND S3 != name |