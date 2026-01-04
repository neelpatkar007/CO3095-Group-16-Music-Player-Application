# Concolic Testing Strategy & Instrumentation

## Path Exploration Table
| Iteration | Concrete Seed (S3, S4, S5, S6)  | Path Taken  | Constraint to Flip               | New Derived Input         |
|-----------|---------------------------------|-------------|----------------------------------|---------------------------|
| 1         | (1.0, False, True, True)        | PC_1        | Flip S5 (HAS_PYGAME)             | (1.0, False, False, True) |
| 2         | (1.0, False, False, True)       | PC_2        | Flip (S4 AND S3 != 1.0)          | (1.5, True, True, True)   |
| 3         | (1.5, True, True, True)         | PC_3        | Flip S5                          | (1.5, True, False, True)  |
| 4         | (1.5, True, False, True)        | PC_4        | Flip S6 (Force Exception)        | (1.5, True, True, False)  |
| 5         | (1.5, True, True, False)        | PC_5        | Flip S5                          | (1.5, True, False, False) |
| 6         | (1.5, True, False, False)       | PC_6        | None (All Paths Covered)         | N/A                       |