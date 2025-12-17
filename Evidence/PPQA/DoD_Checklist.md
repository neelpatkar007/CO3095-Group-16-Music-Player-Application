# Definition of Done (DoD) – Music Player Application

Version: 1.3
Date: 2025-12-17
To: All Team Members

Purpose:
We use this checklist to stop us from saying "Im done" when the code is actually broken or undocumented. If you cannot check every box below, do not open a Pull Request. This is how we ensure we pass the CMMI Level 2 audit. 


## 1. Story-Level Completion Criteria
Before you mark a GitHub issue as done, check these:

| Area                    | Criterion                                                                        | Status |
|-------------------------|----------------------------------------------------------------------------------|--------|
| Requirements            | Did you meet the acceptance criteria exactly as they are defined?                | YES/NO |
|                         | Is the GitHub issue linked to the correct ID (e.g., S2-05)?                      | YES/NO |
|                         | Did you update the `requirements_traceability.csv` with the new code/test links? | YES/NO |
| Design & Implementation | Does the code follow our naming conventions and PEP-8 style?                     | YES/NO |
|                         | Do functions contain clear docstrings/inline comments?                           | YES/NO |
|                         | Does the code run on Lab Machines (without external dependencies)?               | YES/NO |
|                         | Are all relevant Configuration Items (CIs) are committed and versioned?          | YES/NO |
| Testing                 | Do unit tests (black-box and white-box) pass locally?                            | YES/NO |
|                         | Did you run the Symbolic and Concolic tests successfully?                        | YES/NO |
|                         | Is coverage at least 85% achieved (verified in `coverage_report.csv`)?           | YES/NO |
|                         | Are all major/critical bugs fixed?                                               | YES/NO |
| Quality Assurance       | Peer review finished and DoD checklist filled out?                               | YES/NO |
|                         | Did you upload evidence to `/evidence/MA` and `/evidence/PPQA`?                  | YES/NO |
| Documentation           | Did the update the Help/CLI documentation in `README.md`?                        | YES/NO |
|                         | Are the evidence links pasted into `requirements_traceability.csv`?              | YES/NO |
|                         | Is the release tag committed?                                                    | YES/NO |



## 2. Sprint-Level Completion Criteria
We only declare the Sprint "Over" when:

| Area                               | Criterion                                                            | Status |
|------------------------------------|----------------------------------------------------------------------|--------|
| Planning                           | Is the Sprint plan approved and PERT diagram updated?                | YES/NO |
| Metrics                            | Are the Burndown, Velocity, and EVM reports completed?               | YES/NO |
| Measurement                        | Are the final Coverage and metrics reports filed in `/evidence/MA/`. | YES/NO |
| Configuration Management (Release) | Are all the branches merged, reviewed, Tagged (e.g., `v0.x.0`)?      | YES/NO |
|                                    | Did you log the new tag in `Tag_Log.md`.                             | YES/NO |
| Reviews                            | Has the Scrum Master completed and signed off on the sprint review.  | YES/NO |
| CMMI Evidence                      | Did we update all six process areas (REQM, PP, PMC, CM, MA, PPQA)?   | YES/NO |



## 3. Final Project Checklist DoD

| Deliverable       | Criterion                                                             | Status |
|-------------------|-----------------------------------------------------------------------|--------|
| The Code          | Fully functional on lab machine. All four sprints merged into `main`. | YES/NO |
| Testing           | All planned tests implemented and coverage is ≥ 85 %.                 | YES/NO |
| The Documentation | README, Report (Sections A & B), and Video Demonstration are done.    | YES/NO |
| The Evidence      | CMMI folders are full and completed with evidence.                    | YES/NO |
| The Release       | Final tag `v1.0.0` created and recorded in `Tag_Log.md`.              | YES/NO |

