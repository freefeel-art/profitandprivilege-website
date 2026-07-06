# Reading Order

## Purpose

This document defines the mandatory reading order for ChatGPT before providing architectural guidance.

The objective is to eliminate repeated onboarding, incorrect assumptions and unnecessary redesign.

Never skip this process.

---

# Step 1

Read:

01-CHATGPT-ARCHITECT.md

Purpose:

Understand how ChatGPT should behave in this repository.

---

# Step 2

Read:

02-PROJECT-STATE.md

Purpose:

Understand the current implementation status.

Never assume the current sprint.

---

# Step 3

Read the current sprint documentation.

Examples:

- Sprint notes
- Current implementation task
- Active development notes

Purpose:

Understand what is being built right now.

---

# Step 4

Read only the documents required for the current task.

Examples:

If working on Content Production:

- AI-EDITORIAL-OPERATING-SYSTEM.md
- AGENT-CONTRACT.md
- Gold Master
- OLSP Standard

If working on Publishing:

- Publishing Engine
- Deployment workflow

If working on Editorial QA:

- QA specification
- Gold Master

Do not read unrelated documentation.

---

# Before Giving Advice

Always ask yourself:

- Does this already exist?
- Is this already implemented?
- Can this be reused?
- Is this implementation or architecture?

Never redesign before inspecting the repository.

---

# Architecture Rule

The repository is the source of truth.

Existing implementation has priority over assumptions.

Search first.

Understand second.

Modify last.

---

# Communication Rule

One implementation task.

Wait for the result.

Review the outcome.

Continue.

Avoid planning multiple implementation tasks simultaneously.

---

# Final Reminder

The goal is not to create a new system.

The goal is to complete the existing one.

Every suggestion should move the repository closer to production readiness—not further away from architectural redesign.
