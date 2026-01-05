# Symbolic Analysis of `print_help` Function

## Symbolic Inputs
| Variable   | Symbol   | Type           | Domain                 |
|:-----------|:---------|:---------------|:-----------------------|
| command    | $S_1$    | Optional[str]  | $\Sigma^* \cup {None}$ |

## Path Conditions (PCs)
| Path ID   | Condition                                              |
|:----------|:-------------------------------------------------------|
| PC_1      | $S_1$ == None OR $S_1$.strip() == ""                   |
| PC_2      | NOT PC_1 AND ($T$ == "play")                           |
| PC_3      | NOT PC_1 AND $T$ != "play" AND ($T$ == "pause")        |
| PC_4      | NOT PC_1 AND ... AND ($T$ == "stop")                   |
| PC_5      | NOT PC_1 AND ... AND ($T$ == "next")                   |
| PC_6      | NOT PC_1 AND ... AND ($T$ == "prev")                   |
| PC_7      | NOT PC_1 AND ... AND ($T$ == "seek")                   |
| PC_8      | NOT PC_1 AND ... AND ($T$ == "rw")                     |
| PC_9      | NOT PC_1 AND ... AND ($T$ == "ff")                     |
| PC_10     | NOT PC_1 AND ... AND ($T$ == "volume" OR $T$ == "vol") |
| PC_11     | NOT PC_1 AND ... AND ($T$ == "mute")                   |
| PC_12     | NOT PC_1 AND ... AND ($T$ == "unmute")                 |
| PC_ELSE   | NOT PC_1 AND $T$ != "play" ... AND $T$ != "quit"       |