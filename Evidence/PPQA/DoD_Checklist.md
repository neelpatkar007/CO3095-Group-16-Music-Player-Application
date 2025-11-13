# Definition of Done (DoD) – Music Player Application

Version: 1.1
Date: 2025-11-13
Purpose:
To define objective criteria for user stories, features, and sprints, so that all deliverables meet the project’s quality, testing, and documentation standards in compliance with CMMI Level 2.


## 1. Story-Level Completion Criteria

| Area                    | Criterion                                                            | Status |
|-------------------------|----------------------------------------------------------------------|--------|
| Requirements            | Story acceptance criteria implemented exactly as defined.            | YES/NO |
|                         | Story linked to GitHub issue with correct ID (e.g., S2-05).          | YES/NO |
|                         | `requirements_traceability.csv` updated with code and test links.    | YES/NO |
| Design & Implementation | Code follows naming conventions and PEP-8 style.                     | YES/NO |
|                         | Functions contain docstrings/inline comments.                        | YES/NO |
|                         | Code runs on lab machines without external dependencies.             | YES/NO |
|                         | All relevant CIs committed and versioned.                            | YES/NO |
| Testing                 | Unit tests (black-box and white-box) created and pass locally.       | YES/NO |
|                         | Symbolic and concolic tests created and executed successfully.       | YES/NO |
|                         | Minimum 85 % coverage achieved (verified in `coverage_report.csv`).  | YES/NO |
|                         | No critical or major defects open.                                   | YES/NO |
| Quality Assurance       | Peer review and DoD checklist completed.                             | YES/NO |
|                         | Evidence uploaded to `/evidence/MA` and `/evidence/PPQA`.            | YES/NO |
| Documentation           | Help/CLI documentation updated for new commands in `README.md`.      | YES/NO |
|                         | Evidence links included in `requirements_traceability.csv`.          | YES/NO |
|                         | Tagged release committed                                             | YES/NO |



## 2. Sprint-Level Completion Criteria

| Area                     | Criterion                                                                           | Status |
|--------------------------|-------------------------------------------------------------------------------------|--------|
| Planning                 | Sprint plan approved and PERT diagram updated.                                      | YES/NO |
| Monitoring               | Burndown, Velocity, and EVM reports completed.                                      | YES/NO |
| Measurement              | Coverage and metrics reports filed in `/evidence/MA/`.                              | YES/NO |
| Configuration Management | All branches merged, reviewed, tagged (e.g., `v0.x.0`), and logged in `Tag_Log.md`. | YES/NO |
| Quality Assurance        | Scrum Master completed sprint review.                                               | YES/NO |
| CMMI Evidence            | All six process areas (REQM, PP, PMC, CM, MA, PPQA) updated.                        | YES/NO |



## 3. Final Project DoD

| Deliverable   | Criterion                                                               | Status |
|---------------|-------------------------------------------------------------------------|--------|
| Codebase      | Fully functional on lab machine; all four sprints merged into `main`.   | YES/NO |
| Testing       | All planned tests implemented and ≥ 85 % passed.                        | YES/NO |
| Documentation | README, Report (Sections A & B), and Video completed.                   | YES/NO |
| Evidence      | CMMI folders complete with evidence included.                           | YES/NO |
| Release       | Final tag `v1.0.0` created and recorded in `Tag_Log.md`.                | YES/NO |

