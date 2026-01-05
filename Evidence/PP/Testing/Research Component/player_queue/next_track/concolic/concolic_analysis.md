# Concolic Analysis of Player Queue Next Track Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S4, S5)         | Path Taken           | Constraint to Flip                 | New Derived Input   |
|-------------|--------------------------------------------|----------------------|------------------------------------|---------------------|
| 1           | S1=None                                    | PC_1 (Invalid State) | Flip S1 is None                    | S1=Object (Valid)   |
| 2           | S1=Obj, S2=[]                              | PC_2 (No Tracks)     | Flip not S2                        | S2=[TrackA, TrackB] |
| 3           | S1=Obj, S2=[A,B], S3=1, S4='off', S5=False | PC_5 (End/Stop)      | Flip Stop at End (Set S4='all')    | S4='all'            |
| 4           | S1=Obj, S2=[A,B], S3=1, S4='all', S5=False | PC_6 (Loop All)      | Flip End of List (Set S3=0)        | S3=0                |
| 5           | S1=Obj, S2=[A,B], S3=0, S4='off', S5=False | PC_7 (Next)          | Flip S4 != 'one' (Set S4='one')    | S4='one'            |
| 6           | S1=Obj, S2=[A,B], S3=0, S4='one', S5=False | PC_3 (Loop One)      | Flip S5 == False (Set S5=True)     | S5=True             |
| 7           | S1=Obj, S2=[A,B], S3=0, S4='off', S5=True  | PC_4 (Shuffle)       | None (All major branches explored) | N/A                 |