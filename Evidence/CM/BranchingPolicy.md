# Branching Policy – Music Player Application

**Version:** 1.0  
**Date:** 2025-11-12   
**Applies To:** All contributors to this repository

---

## 1. Purpose
To establish a consistent, auditable process for managing source code versions and changes throughout the project, to meet **CMMI Level 2 – Configuration Management (CM)**.

---

## 2. Branching Model Overview
- **Default Branch:** `main` – always stable and deployable.
- **Development Branches:** Created per user story or feature.
- **Tagging:** Semantic Versioning used per sprint (e.g., `v0.1.0`, `v0.2.0`).
- **Branch Retention:** Feature branches are not deleted after merge (evidence of process and traceability).

---

## 3. Branch Naming Convention
- feature/<sprint-id>-<story-id>-<short-description>
- bugfix/<issue-id>-<short-description>
- **Examples:**
  - feature/S1-04-volume-control 
  - feature/S3-08-like-songs 
  - bugfix/issue-21-seek-edgecase

Each branch must correspond to an open GitHub Issue (user story) for traceability.

---

## 4. Workflow Rules

1. **Create branch** from `main` when starting a story.  
2. **Commit often** with clear messages following:
   - [S1-04] Implement volume clamp (0–100)
   - [S2-09] Fix scanner duplicate handling
3. **Push branch** and open a Pull Request (PR) once all Definition-of-Done criteria met.
4. **Peer review** by at least one other group member before merging.
5. **Merge into `main`**.
6. **Tag new version** on successful sprint completion:
- Sprint 1 → `v0.1.0`
- Sprint 2 → `v0.2.0`
- Sprint 3 → `v0.3.0`
- Sprint 4 → `v1.0.0`
7. **Retain branch** for report and demonstration.

## 5. Access Control and Reviews
- **Branch Protection:** `main` requires Pull Request review and at least 85 % test coverage.
- **Reviewer Assignment:** Scrum Master assigns reviewers based on feature area.
- **Approval Required:** 1 reviewer + Scrum Master.

---

## 6. Configuration Baselines
- Each sprint release (tagged version) forms a **baseline**.
- Artefacts captured at baseline:
- Source code snapshot (tag)
- Test coverage report
- Evidence folder (REQM, PP, PMC, CM, MA, PPQA)
- EVM & COCOMO artefacts

---

## 7. Change Control
- Any modification to an implemented story must go through:
1. Updated Issue comment on Projects Board (reason + approval).
2. New branch referencing original story ID.
3. Updated traceability in `/evidence/REQM/requirements_traceability.csv`.

---

## 8. Tools
- **Version Control:** Git + GitHub
- **Code Review:** GitHub Pull Requests  
- **Issue Tracking:** GitHub Projects Board
