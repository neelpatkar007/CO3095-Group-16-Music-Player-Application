# Symbolic Analysis of _playback_worker Function

## Symbolic Inputs
| Variable              | Symbol   | Type    | Description                             |
|-----------------------|----------|---------|-----------------------------------------|
| `stop_event.is_set()` | S1       | Boolean | Loop termination condition              |
| `state.is_playing`    | S2       | Boolean | Flag indicating if playback is active   |
| `state.is_paused`     | S3       | Boolean | Flag indicating if playback is paused   |
| `time.time()`         | S4       | Float   | Current timestamp (affects alarm logic) |

## Path Conditions (PCs)
| Path ID   | Condition (Logic)                                         | Logic Description                                                                      |
|-----------|-----------------------------------------------------------|----------------------------------------------------------------------------------------|
| **PC_1**  | `S1`                                                      | **Early Return:** Stop event is set immediately.                                       |
| **PC_2**  | `(NOT S1) AND (S2 AND (NOT S3)) AND (S4 % 10 == 0)`       | **Play & Alarm:** Running, Playing (not paused), Time triggers alarm.                  |
| **PC_3**  | `(NOT S1) AND (S2 AND (NOT S3)) AND (S4 % 10 != 0)`       | **Play & No Alarm:** Running, Playing (not paused), Time does NOT trigger alarm.       |
| **PC_4**  | `(NOT S1) AND (NOT (S2 AND (NOT S3))) AND (S4 % 10 == 0)` | **No Play & Alarm:** Running, Not Playing (or Paused), Time triggers alarm.            |
| **PC_5**  | `(NOT S1) AND (NOT (S2 AND (NOT S3))) AND (S4 % 10 != 0)` | **No Play & No Alarm:** Running, Not Playing (or Paused), Time does NOT trigger alarm. |

