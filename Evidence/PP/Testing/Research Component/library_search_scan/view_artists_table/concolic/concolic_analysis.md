# Concolic Analysis of `view_artists_table` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3)    | Path Taken  | Constraint to Flip    | New Derived Input            |
|-------------|-------------------------------|-------------|-----------------------|------------------------------|
| 1           | None                          | PC_1        | Flip (S1 is None)     | S1 = PlayerState()           |
| 2           | S1=Obj (No attrs)             | PC_2        | Flip (No attr)        | S1.library_tracks = []       |
| 3           | S1=Obj, S2=[]                 | PC_3        | Flip (S2 Empty)       | S1.library_tracks = [None]   |
| 4           | S1=Obj, S2=[None]             | PC_4        | Flip (S3 is None)     | S2 = [Track()]               |
| 5           | S1=Obj, S2=[Track()]          | PC_5        | Flip (No artist)      | S2 = [Track(artist=None)]    |
| 6           | S1=Obj, S2=[Track(None)]      | PC_6        | Flip (Art is None)    | S2 = [Track(artist=" ")]     |
| 7           | S1=Obj, S2=[Track(" ")]       | PC_7        | Flip (Art Empty)      | S2 = [Track(artist="Queen")] |
| 8           | S1=Obj, S2=[Track("Queen")]   | PC_8        | None                  | N/A                          |