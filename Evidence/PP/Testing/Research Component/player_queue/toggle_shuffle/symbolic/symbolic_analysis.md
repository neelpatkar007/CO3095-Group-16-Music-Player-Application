# Symbolic Analysis of toggle_shuffle Function

## Symbolic Inputs
| Variable               | Symbol  | Type    | Description                                      |
|------------------------|---------|---------|--------------------------------------------------|
| `state`                | S1      | Object  | The player state object.                         |
| `len(tracks)`          | S2      | Integer | Number of tracks returned by `_get_tracks_safe`. |
| `state.shuffle_active` | S3      | Boolean | Current shuffle status (False=OFF, True=ON).     |
| `state.current_index`  | S4      | Integer | Current track index in the list.                 |
| `state.loop_mode`      | S5      | String  | Playback loop mode (e.g., 'one', 'off').         |

## Path Conditions (PCs)

| Path ID   | Condition (Logic)                                      | Logic Description                                                               |
|-----------|--------------------------------------------------------|---------------------------------------------------------------------------------|
| **PC_1**  | `S1 is None` OR `Type(S1) is Primitive`                | **Invalid State:** Input state is null or invalid type.                         |
| **PC_2**  | `NOT PC_1` AND `NOT hasattr(S1, 'tracks')`             | **Missing Tracks:** State object lacks the required `tracks` attribute.         |
| **PC_3**  | `NOT PC_1..2` AND `NOT S3` AND `S2 == 0`               | **Enable Empty:** Toggling ON with an empty queue.                              |
| **PC_4**  | `NOT PC_1..2` AND `NOT S3` AND `S2 == 1`               | **Enable Single:** Toggling ON with only 1 song (limited effect).               |
| **PC_5**  | `NOT PC_1..2` AND `NOT S3` AND `S2 > 1` AND `S4 >= S2` | **Enable & Reset:** Toggling ON, but index is out of bounds; resets index to 0. |
| **PC_6**  | `NOT PC_1..2` AND `NOT S3` AND `S2 > 1` AND `S4 < S2`  | **Enable Normal:** Toggling ON, index is valid; no reset occurs.                |
| **PC_7**  | `NOT PC_1..2` AND `S3` AND `S5 == 'one'`               | **Disable Loop:** Toggling OFF while "Loop One" is active (warning printed).    |
| **PC_8**  | `NOT PC_1..2` AND `S3` AND `S5 != 'one'`               | **Disable Normal:** Toggling OFF, standard behavior.                            |

