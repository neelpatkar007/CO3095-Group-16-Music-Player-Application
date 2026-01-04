## Symbolic Execution Analysis: `main` Function

### Symbolic Inputs
| Variable                | Symbol   | Type      | Description                                        |
|-------------------------|----------|-----------|----------------------------------------------------|
| `input("> ")` Result    | S1       | String    | User-entered command string.                       |
| `input()` Exception     | S2       | Exception | Represents `EOFError` or `KeyboardInterrupt`.      |
| `handle_command` Result | S3       | Boolean   | Returns `True` to continue loop, `False` to break. |


### Path Conditions
| Path ID  | Condition           | Description                                                                                    |
|----------|---------------------|------------------------------------------------------------------------------------------------|
| PC_1     | S2                  | Input raises an exception (`EOFError` / `KeyboardInterrupt`), triggering immediate shutdown.   |
| PC_2     | NOT S2 AND NOT S3   | Input is valid, but `handle_command` returns `False`, causing loop exit.                       |
| PC_3     | NOT S2 AND S3       | Input is valid, and `handle_command` returns `True`, allowing the loop to continue.            |