---
name: sparringday-workspace
description: Use for work in the SparringDay multi-repository workspace, including Codex setup, repository boundaries, AWS SAM scaffolds, automation, ADRs, service and frontend changes, or local validation.
---

# SparringDay workspace

## Role

Coordinate work across the SparringDay repositories and route domain tasks to the user's existing skills. Keep this skill as a short workspace overlay; do not copy specialist skill instructions into it.

## Task

Before changing files, read the nearest `AGENTS.md`, identify the Git root that owns each target, inspect its current state and relevant ADRs, then use the existing skill registry at `automation/scripts/codex/skills/registry.md` to select the smallest applicable skill set.

When the environment provides a listed skill, invoke it by its registered name. If it is unavailable in local Codex, follow the repository instructions and local overlay, then state any material limitation.

## Format

Use the user's requested output format. For structured task content, apply Role, Task, Format (R-T-F). Report commands and results exactly as observed.

## Repository rules

1. Work in one Git repository at a time. Do not edit sibling repositories from the current repository's task context.
2. Integrate services only through APIs, events, or versioned packages; never add relative imports between services.
3. Use Node.js 22, strict TypeScript and arm64 for SAM services, following the local repository's actual template.
4. Keep credentials out of tracked files, examples, logs and prompts. Reference SSM Parameter Store or Secrets Manager by name only.
5. Keep AWS deployment and production actions out of CI. Run them only when the user explicitly asks and the change is reviewed.
6. Treat scaffold/TODO status honestly; a static presence check does not prove a template deploys or a workflow passes.
7. Keep the current architecture plan authoritative for this workspace. Do not introduce Terraform where the current stack is defined as SAM/CloudFormation.

## Reuse map

- Architecture, roadmap, ADR, readiness: `$sparringday-platform-architect`.
- Codex task, prompt, backlog or handoff: `$sparringday-codex-task-writer`.
- Authentication, IAM, authorization, privacy or secrets: `$sparringday-auth-security-reviewer`.
- Sparringday portal feature: `$sparringday-frontend-feature-builder`; add `$tailwind-layout-engineer` for layout or accessibility.
- Ranking, rating or matchmaking: `$sparringday-glicko-ranking-engineer`.
- HML/PRD release or rollback: `$sparringday-release-manager`.
- CloudFront access-log/Athena analysis: `$cloudfront-athena-reporter`.
- Terraform modules: `$terraform-module-factory` only when Terraform is explicitly the target.

The complete trigger descriptions and local fallback recipes live in `automation/scripts/codex/skills/registry.md`.
