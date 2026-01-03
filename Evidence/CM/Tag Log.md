# Tag Log – Music Player Application

Version: 1.2 
Date: 2025-12-17  
To: All Contributors


Goal: We can use this log to track every "baseline" (official release) of our code. This is required for CMMI Level 2 audit to prove that our releases are stable versions and traceable.


## 1. Overview of How we use Tags
Each tag is basically a "save point" and we create one at the end of every Sprint to mark a stable version of the music player app that has passed all the tests. 
We use the following versioning format which is: v<Major>.<Minor>.<Patch>.

- Major e.g. v1.0.0 – Will be a major milestone or the final release  
- Minor e.g. v0.1.0 – A standard sprint-level release  
- Patch e.g. v0.1.1 – Are quick fixes, hotfixes or minor adjustment if we do find any bugs after a sprint release


## 2. Tag History Log

| Tag  | Date       | Sprint | Commit Hash | Author        | Description / Contents     | QA Status  | Evidence Links                                                                              |
|------|------------|--------|-------------|---------------|----------------------------|------------|---------------------------------------------------------------------------------------------|
| v0.1 | 18/12/2025 | 1      | 56e8603     | neelpatkar007 | Completed Sprint 1 Release | Verified   | https://github.com/neelpatkar007/CO3095-Group-16-Music-Player-Application/releases/tag/v0.1 |
| v0.2 | 19/12/2025 | 2      | ca140db     | neelpatkar007 | Completed Sprint 2 Release | Verified   | https://github.com/neelpatkar007/CO3095-Group-16-Music-Player-Application/releases/tag/v0.2 |
| v0.3 | 25/12/2025 | 3      | 2ff6ca2     | neelpatkar007 | Completed Sprint 3 Release | Verified   | https://github.com/neelpatkar007/CO3095-Group-16-Music-Player-Application/releases/tag/v0.3 |
| v0.4 | 03/01/2025 | 4      | 54d2f49     | neelpatkar007 | Completed Sprint 4 Release | Verified   | https://github.com/neelpatkar007/CO3095-Group-16-Music-Player-Application/releases/tag/v0.4 |
| v1.0 |            | N/A    |             |               | Final Release              |            |                                                                                             |
|




## 3. Process of How to do Tag Creation & Maintenance
Before you create a tag, make sure that you have followed and met these rules so we don't break the project's versioning and stability:
1. All acceptance criteria for the sprint must be 100% complete.
2. Never tag a feature branch - only tag `main` after the merge.
3. We need at least an 85% test coverage across the board.
4. Now you can create the tag:
    - Merge all approved Pull Requests into `main`.
    - Run the tests one last time to ensure everything works.
    - Run the git tag command (git tag v0.x.0) and push it.
    - Update the table in Section 2 immediately after tagging is done.
5. If any releases are messed up, do not delete the tag and instead fix the bug, merge it, and create a Patch tag (for example v0.1.1).