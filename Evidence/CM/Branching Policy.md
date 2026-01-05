# Branching Policy - Music Player Application

Version: 1.3
Date: 2026-01-05
To: All Contributors


## 1. Objective
The document outlines the version control standard for our group. We are using these rules to meet the requirements of Configuration Management (CM) process area.
The goal is - if a piece of code exists, we must be able to trace it back to a specific user story and a sprint. 


## 2. Branch Structure
- Default Branch (main) - This is the production baseline. And any code in main must work. Must not make any direct commits and all changes must come from a Pull Request. 
- Development Branches - Create a new branch for every single user story or feature or bug fix. And make sure not to delete the branches after merging as we need them as evidence for the final report and the CMMI audit trail.


## 3. Branches Naming Standards
- Each branch must follow this specific format for consistency and traceability. If a branch is named wrong, then you must close it and start over again.
- The format is: <type>/<sprint-id>-<story-id>-<short-description>
- Some examples are:
  - feature/S1-04-volume-control 
  - feature/S3-08-like-songs 
  - bugfix/S1-08-seek-edgecase


## 4. Workflow Requirements
1. Start - Always make sure to pull main before creating a new branch.
2. Branch - Create your branch using the naming convention mentioned above.
3. Commit - Each commit must make sense and be as small as possible and must relate to the user story.
4. Pull Request (PR) - Open the PR against main when you meet the Definition of Done.
    You must tag at least one group member as a reviewer for their review.
    Quality Check - Do not merge if there are merge conflicts. 
5. Merge - Once it is approved, then the code is able to be merged into main.


## 5. Releases and Baselines
- Tagging - Use Semantic Versioning (e.g., v0.1.0, v0.2.0, v1.0.0) for tagging releases.
- Before tagging, make sure that the repository has - The latest stable code in main.
- At the end of each sprint, we make sure to also update the evidence folders - (REQM, PP, PMC, CM, MA, PPQA).
- And finally, we create the EVM & COCOMO I and II tracking sheets for each of the 4 Sprints.
++

## 6.Handling Changes (Change Control)
- If there are any changes that need to be made to a user story that is already merged:
  - Go to the closed GitHub issue and comment why the change is needed
  - Create a new branch with a version (-v2)
    - For example - feature/S1-04-volume-control-v2
  - Then update the requirements traceability matrix (excel) in /Evidence/REQM/requirements_traceability.xlsx to point to the new branch


## 7. Tool Stack
- VSC - Git via PyCharm
- Repository - GitHub
- Code Reviews - GitHub Pull Requests  
- Issue Tracking - GitHub Projects Board