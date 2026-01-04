# Concolic Analysis of `discover_tracks` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S5)  | Path Taken                | Constraint to Flip           | New Derived Input         |
|-------------|---------------------------------|---------------------------|------------------------------|---------------------------|
| **1**       | (False, N/A, N/A, N/A)          | PC_1 (Early Return)       | ¬S1 → S1                     | (True, False, N/A, N/A)   |
| **2**       | (True, False, N/A, N/A)         | PC_2 (Not a File)         | ¬S2 → S2                     | (True, True, False, N/A)  |
| **3**       | (True, True, False, N/A)        | PC_3 (Unsupported Suffix) | ¬S3 → S3                     | (True, True, True, None)  |
| **4**       | (True, True, True, None)        | PC_4 (Default Duration)   | S5 == None → S5 ≠ None       | (True, True, True, 200.0) |
| **5**       | (True, True, True, 200.0)       | PC_5 (Real Duration)      | None (All branches explored) | N/A                       |