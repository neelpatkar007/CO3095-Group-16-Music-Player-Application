# Symbolic Analysis of `handle_mute_command`

## Symbolic Inputs
| Variable   | Symbol   | Type        | Note                                               |
|------------|----------|-------------|----------------------------------------------------|
| state      | S1       | PlayerState | None                                               |
| raw        | S2       | Any         | The raw input string to be processed               |
| is_muted   | S3       | Boolean     | Derived property: `getattr(S1, 'is_muted', False)` |
| cmd        | S4       | String      | Derived transformation: `S2.strip().lower()`       |

## Path Conditions (PCs)
| Path ID  | Condition                                                                | Logic Justification                                                    |
|----------|--------------------------------------------------------------------------|------------------------------------------------------------------------|
| PC_1     | S1 == None                                                               | The function guards against null state objects immediately.            |
| PC_2     | S1 != None AND NOT isinstance(S2, str)                                   | The function enforces type strictness on the raw input.                |
| PC_3     | S1 != None AND isinstance(S2, str) AND S4 == "/mute" AND S3 == True      | The user requests a mute, but the state is already muted.              |
| PC_4     | S1 != None AND isinstance(S2, str) AND S4 == "/mute" AND S3 == False     | Valid state change: The user requests mute, and the system complies.   |
| PC_5     | S1 != None AND isinstance(S2, str) AND S4 == "/unmute" AND S3 == False   | The user requests unmute, but the state is already unmuted.            |
| PC_6     | S1 != None AND isinstance(S2, str) AND S4 == "/unmute" AND S3 == True    | Valid state change: The user requests unmute, and the system complies. |
| PC_7     | S1 != None AND isinstance(S2, str) AND S4 != "/mute" AND S4 != "/unmute" | The input string does not match any known command literals.            |