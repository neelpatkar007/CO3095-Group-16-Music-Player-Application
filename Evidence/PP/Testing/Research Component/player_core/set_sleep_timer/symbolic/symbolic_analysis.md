# Symbolic Analysis for `set_sleep_timer` Function

## Symbolic Inputs
| Variable          | Symbol   | Type         | Description                        |
|-------------------|----------|--------------|------------------------------------|
| state             | S1       | PlayerState  | The primary state object.          |
| minutes           | S2       | float / int  | Temporal input from the user.      |
| S1.audio_engine   | S3       | Object       | Dependency check for audio engine. |
| S1.sleep_deadline | S4       | float / None | Current sleep deadline.            |
| time.time()       | S5       | float        | Current system time (environment). |
| S1.is_playing     | S6       | bool         | Playback status flag.              |

## Path Conditions (PCs)
| Path ID   | Condition                                            | Note                             |
|-----------|------------------------------------------------------|----------------------------------|
| PC_1      | NOT (S1 is PlayerState)                              | Input Validation Failure         |
| PC_2      | (S1 is PlayerState) AND (S1 is None)                 | Logically Impossible (Dead Code) |
| PC_3      | S1 valid AND (S3 is None)                            | Engine Dependency Failure        |
| PC_4      | S1 valid AND S3 valid AND NOT (S2 is Numeric)        | Input Type Failure               |
| PC_5      | … AND (S2 <= 0) AND (S4 is NOT None)                 | Cancellation Success             |
| PC_6      | … AND (S2 <= 0) AND (S4 is None)                     | Cancellation Fail                |
| PC_7      | … AND (S2 > 1440)                                    | Upper Boundary Violation         |
| PC_8      | … AND (S2 > 0) AND (S2 <= 1440) AND (Deadline <= S5) | Temporal Anomaly                 |
| PC_9      | … AND (S2 valid) AND (S2 >= 60)                      | Valid Set (Hours)                |
| PC_10     | … AND (S2 valid) AND (S2 < 1)                        | Valid Set (Seconds)              |
| PC_11     | … AND (S2 valid) AND (S2 >= 1) AND (S2 < 60)         | Valid Set (Minutes)              |
| PC_12     | … AND (Exception Occurs)                             | Robustness Check                 |