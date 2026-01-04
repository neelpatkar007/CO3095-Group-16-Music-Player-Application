# Concolic Analysis for `read_metadata` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S2, S3, S4, S5)      | Path Taken                | Constraint to Flip         | New Derived Input                   |
|------------|-------------------------------------|---------------------------|----------------------------|-------------------------------------|
| **1**      | (False, N/A, N/A, N/A)              | PC_1 (Library Missing)    | ¬S2 → S2                   | (True, None, N/A, N/A)              |
| **2**      | (True, None, N/A, N/A)              | PC_2 (File Load Failure)  | ¬S3 → S3                   | (True, Object, Valid, Valid)        |
| **3**      | (True, Object, Valid, Valid)        | PC_4 (Full Success)       | S4 (Duration) → Exception  | (True, Object, Exception, Valid)    |
| **4**      | (True, Object, Exception, Valid)    | PC_5 (Bad Duration)       | S6 (Title Tag) → Exception | (True, Object, Exception, BadTitle) |
| **5**      | (True, Object, Exception, BadTitle) | PC_5 (Malformed Metadata) | All branches explored      | N/A                                 |