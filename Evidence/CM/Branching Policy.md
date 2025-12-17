# Branching Policy for Music Player Application

Version: 1.2
Date: 2025-12-17
To: All Contributors


## 1. Goal
We need a stricter version control process to meet the CMMI Level 2 - Configuration Management (CM) requirements. This is to ensure that we have a clear and auditable trail for every single line of code that's written.


## 2. Branching Strategy
- Default Branch (main): This should always be stable and deployable as this is our production code.
- Development Branches: Create a new branch for every single user story or feature or bug fix.
- Tagging: Semantic versioning used per sprint (e.g., v0.1.0, v0.2.0).
- Retention Rules: Do not delete any branches after merging as we must keep these as evidence of the process and traceability during the audit.


## 3. Branches Naming Conventions
Each branch should link to a specific GitHub Issue (user story) for traceability and use the following format:
The format is: <type>/<sprint-id>-<story-id>-<short-description>
- Some Examples:
  - feature/S1-04-volume-control 
  - feature/S3-08-like-songs 
  - bugfix/S1-08-seek-edgecase


## 4. Workflow Rules
1. Start: Must always branch off `main`.
2. Commit: Commits must be made often. The commit message must start with the ID:
    - [S1-04] Implement volume clamp (0–100)
    - [S2-09] Fix scanner duplicate handling
3. Pull Request (PR): Push branch and open a Pull Request when you meet the Definition of Done
4. Review: You will need a peer review from at least one group member before you can merge.
5. Merge: Merge the branch into `main`
6. Tagging: We tag the release at the end of each sprint:
   - Sprint 1 -> `v0.1.0`
   - Sprint 2 -> `v0.2.0`
   - Sprint 3 -> `v0.3.0`
   - Sprint 4 -> `v1.0.0`
7. Cleanup: As mentioned in Section 2, we will leave the remote branches for proof for the final report.


## 5. Branch Protection, Access Control and Reviews
We have locked the `main` branch to prevent any accidental changes or breakages to the code.
- Direct Pushing: Do not push any code directly to `main`. All changes must come from a Pull Request.
- Quality Gate: Ensure that all tests do pass with at least an 85 % coverage before merging.
- Approvals: Requires at least 1 reviewer to approve. 


## 6. Configuration Baselines ("Snapshot")
- At the end of each sprint, we create a baseline. We do this by ensuring the following things are updated and committed before tagging:
    - All the source code (via git tag)
    - Test coverage report in: `/Evidence/MA/coverage_report.xlsx`
    - The evidence folder updates: (REQM, PP, PMC, CM, MA, PPQA).
    - Finally, EVM & COCOMO I and II tracking sheets.


## 7. Change Control
- If any modifications are needed to be made to a user story that has already been merged or implemented, then:
    1. Post a new comment on the original GitHub Issue on the Project Board and explain why the change is needed and get approval.
    2. Create a new branch referencing the original story ID - for example - feature/S1-04-volume-control-v2.
    3. Ensure to update the traceability matrix in `/Evidence/REQM/requirements_traceability.xlsx`.


## 8. Tool Stack
- Version Control (VCS): Git + GitHub
- Code Reviews: GitHub Pull Requests  
- Issue Tracking: GitHub Projects Board