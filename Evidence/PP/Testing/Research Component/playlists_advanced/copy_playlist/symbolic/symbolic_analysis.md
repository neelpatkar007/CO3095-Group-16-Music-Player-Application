# Symbolic Analysis of copy_playlist Function

## Symbolic Inputs

| Variable | Symbol | Type | Description |
| --- | --- | --- | --- |
| `state` | S1 | Object | The player state object containing playlists. |
| `source_name` | S2 | String | The name of the playlist to copy from. |
| `new_name` | S3 | String/Other | The proposed name for the new playlist. |

## Path Conditions (PCs)

| Path ID | Condition (Logic) | Logic Description |
| --- | --- | --- |
| **PC_1** | `NOT isinstance(S3, str)` | **Type Error:** New name is not a string (e.g., Integer). |
| **PC_2** | `S3 IN ReservedWords` | **Reserved Name:** New name is a system reserved word (e.g., "help"). |
| **PC_3** | `S1 is None` (or Invalid) | **Invalid State:** State object is missing or invalid. |
| **PC_4** | `len(S1.playlists) == 0` | **Empty State:** No playlists exist to copy from. |
| **PC_5** | `len(S3.strip()) == 0` | **Whitespace Error:** New name is empty or only whitespace. |
| **PC_6** | `len(S3) < 3` | **Length Error (Min):** New name is too short. |
| **PC_7** | `len(S3) > 20` | **Length Error (Max):** New name is too long. |
| **PC_8** | `NOT S3.isalnum()` | **Format Error:** New name contains special characters. |
| **PC_9** | `S3 IN AdminList` | **Restricted Name:** New name is in the admin restricted list. |
| **PC_10** | `GetPlaylist(S2) is None` | **Source Missing:** The source playlist (`S2`) does not exist. |
| **PC_11** | `S3 IN ExistingNames` | **Duplicate Error:** A playlist with the new name already exists. |
| **PC_12** | `(All checks pass)` | **Success:** Source exists, name is valid and unique; copy performed. |

