# Symbolic Analysis of handle_command Function

## Symbolic Inputs
| Variable                | Symbol   | Type    | Description                                                      |
|-------------------------|----------|---------|------------------------------------------------------------------|
| command                 | S1       | String  | The raw input string provided by the user                        |
| state.resume_active     | S2       | Boolean | Flag indicating if the player should resume from a saved point   |
| state.current_track     | S3       | Boolean | Represents validity of the current track (Non-None implies True) |
|  state.position_seconds | S4       | Float   | The saved playback position in seconds                           |

## Path Conditions
| Path ID | Condition                                               |
|---------|---------------------------------------------------------|
| PC_1    | S1.strip() is Empty                                     |
| PC_2    | NOT PC_1 AND (len(S1)==1 AND S1.lower() IN {p, s, m})   |
| PC_3    | NOT PC_2 AND base IN {/quit, /exit, q}                  |
| PC_4    | NOT PC_3 AND base == /play AND S2 AND S3 AND S4 > 0     |
| PC_5    | NOT PC_3 AND base == /play AND S2 AND S3 AND NOT S4 > 0 |
| PC_6    | NOT PC_3 AND base == /play AND NOT (S2 AND S3)          |
| PC_7    | NOT PC_4..6 AND base == /pause                          |
| PC_13   | NOT PC_1..12 AND base == /seek AND args is Empty        |
| PC_14   | NOT PC_1..12 AND base == /seek AND args is NOT Empty    |
|  PC_21  | NOT (Any prior valid command match)                     |