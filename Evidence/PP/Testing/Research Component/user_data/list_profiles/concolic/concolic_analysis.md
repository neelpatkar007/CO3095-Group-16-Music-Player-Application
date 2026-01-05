# Concolic Analysis of list_profiles Function
 
## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3)             | Path Taken   | Constraint to Flip   | New Derived Input              |
|-----------|----------------------------------------|--------------|----------------------|--------------------------------|
| 1         | S1=None                                | PC_1         | NOT(S1 == None)      | S1=ValidObj, S2={}, S3="none"  |
| 2         | S1=ValidObj, S2={}, S3="default"       | PC_2         | NOT(S3 == "default") | S1=ValidObj, S2={}, S3="guest" |
| 3         | S1=ValidObj, S2={}, S3="guest"         | PC_3         | None                 | N/A                            |