# Concolic Analysis of view_stats Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3, S4)                | Path Taken  | Constraint to Flip        | New Derived Input         |
|------------|-----------------------------------------------|-------------|---------------------------|---------------------------|
| 1          | `None`                                        | PC_1        | Flip `(S1 == None)`       | `S1 = Empty Object`       |
| 2          | `S1=Obj, S2=None`                             | PC_2        | Flip `(S2 is Dict)`       | `S1=Obj, S2={}`           |
| 3          | `S1=Obj, S2={}`                               | PC_3        | Flip `(S2 Empty)`         | `S1=Obj, S2={"f1": 1}`    |
| 4          | `S1=Obj, S2={"f1": 1}, S3=None`               | PC_4        | Flip `(S3 is Valid List)` | `S1=Obj, S3=[Track(...)]` |
| 5          | `S1=Obj, S3=[...], S4="invalid"`              | PC_5        | Flip `(S4 is Numeric)`    | `S1=Obj, S4=3600`         |
| 6          | `S1=Obj, S2={"f1": 1}, S3=[Track(path="f2")]` | PC_6        | Flip `(S5 Empty)`         | Modify S2/S3 to Match     |
| 7          | `S1=Obj, S2={"f1": 1}, S3=[Track(path="f1")]` | PC_7        | None (Fully Explored)     | N/A                       |