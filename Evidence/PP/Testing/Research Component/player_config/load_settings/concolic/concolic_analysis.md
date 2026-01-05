# Concolic Analysis for `load_settings` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1..S7)                                    | Path Taken        | Constraint to Flip      | New Derived Input     |
|------------|-----------------------------------------------------------|-------------------|-------------------------|-----------------------|
| 1          | S1=True, S2=50, S3=True, S4="one", S5=1.0, S6={}, S7=10.0 | PC_3 (Happy Path) | Flip (S2 is int)        | S2="invalid" (String) |
| 2          | S1=True, S2="invalid", ... (others valid)                 | PC_VolTypeFail    | Flip (0 <= S2 <= 100)   | S2=150 (Int)          |
| 3          | S1=True, S2=150, ... (others valid)                       | PC_VolRangeFail   | Flip (S3 is bool)       | S3=1 (Int)            |
| 4          | S1=True, S3=1, ... (others valid)                         | PC_ShuffTypeFail  | Flip (S4 is str)        | S4=False (Bool)       |
| 5          | S1=True, S4=False, ... (others valid)                     | PC_LoopTypeFail   | Flip (S4 in [valid])    | S4="unknown"          |
| 6          | S1=True, S4="unknown", ... (others valid)                 | PC_LoopValFail    | Flip (S5 is num)        | S5="fast" (String)    |
| 7          | S1=True, S5="fast", ... (others valid)                    | PC_SpeedTypeFail  | Flip (0.5 <= S5 <= 2.0) | S5=3.0                |
| 8          | S1=True, S5=3.0, ... (others valid)                       | PC_SpeedRangeFail | Flip (S6 is dict)       | S6=[] (List)          |
| 9          | S1=True, S6=[], ... (others valid)                        | PC_TagsTypeFail   | Flip (S7 is num)        | S7="long" (String)    |
| 10         | S1=True, S7="long", ... (others valid)                    | PC_TimeTypeFail   | Flip (S7 >= 0)          | S7=-5.0               |
| 11         | S1=True, S7=-5.0, ... (others valid)                      | PC_TimeNegFail    | Flip (S1)               | S1=False              |