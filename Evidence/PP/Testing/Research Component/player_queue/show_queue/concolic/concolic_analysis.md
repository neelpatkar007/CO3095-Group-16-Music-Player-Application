# Concolic Analysis of `show_queue` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2... S6)           | Path Taken          | Constraint to Flip       | New Derived Input         |
|------------|----------------------------------------|---------------------|--------------------------|---------------------------|
| 1          | S1=None                                | PC_1 (Early Return) | Flip (S1 is Invalid)     | S1=Object()               |
| 2          | S1=Obj, S2=[], S3=0                    | PC_2 (End of Queue) | Flip (S3 >= Len(S2))     | S1=Obj, S2=[T1], S3=0     |
| 3          | S1=Obj, S2=[T1], S3=0, S4=True         | PC_3 (Playing)      | Flip (S4 == True)        | S1=Obj, S2=[T1], S4=False |
| 4          | S1=Obj, S2=[T1], S4=False, S5=True     | PC_4 (Paused)       | Flip (S5 == True)        | S1=Obj, S2=[T1], S5=False |
| 5          | S1=Obj, S2=[T1], S5=False, S6=False    | PC_5 (Default)      | Flip (S6 == False)       | S1=Obj, S6=True           |