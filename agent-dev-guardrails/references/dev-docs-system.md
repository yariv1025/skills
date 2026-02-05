# Dev Docs System

Persistent documentation for complex tasks. Prevents "losing the plot" across sessions.

## Table of Contents

1. [When to Use Dev Docs](#when-to-use-dev-docs)
2. [Folder Structure](#folder-structure)
3. [Templates](#templates)
4. [Update Protocol](#update-protocol)
5. [Compaction Protocol](#compaction-protocol)
6. [Examples](#examples)

---

## When to Use Dev Docs

Create a task folder for any feature or refactor expected to take **>30 minutes** or span **multiple sessions**.

| Task Size | Dev Docs? |
|-----------|-----------|
| Quick fix (<10 min) | No |
| Small feature (10–30 min) | Optional |
| Medium feature (30 min – 2 hours) | Yes |
| Large feature (>2 hours) | Yes, mandatory |
| Multi-session work | Yes, mandatory |

---

## Folder Structure

Create task folders at: `dev/active/<task-name>/`

```
dev/
└── active/
    └── add-user-auth/
        ├── add-user-auth-plan.md      # Approved plan
        ├── add-user-auth-context.md   # Key files, decisions, constraints
        └── add-user-auth-tasks.md     # Checkbox execution list
```

**Naming convention:** Use lowercase, hyphens, descriptive names.

---

## Templates

### `<task-name>-plan.md`

```markdown
# Plan: [Task Name]

## Goal
[One sentence describing the desired end state]

## Non-goals (YAGNI guard)
- [Explicitly out of scope item 1]
- [Explicitly out of scope item 2]

## Proposed Design

### Components & Responsibilities
| Component | Responsibility |
|-----------|---------------|
| [Component 1] | [What it does] |
| [Component 2] | [What it does] |

### Data Flow
[Describe how data moves through the system]

### Public API Changes
[New endpoints, functions, or breaking changes]

## Migration Plan (if needed)
[Steps to migrate from current state to new state]

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to address] |

## Validation Plan
[Exact commands to verify success]

## Approval
- [ ] Plan reviewed and approved by user
```

### `<task-name>-context.md`

```markdown
# Context: [Task Name]

## Key Files
| File | Purpose |
|------|---------|
| [path/to/file1.py] | [What it contains] |
| [path/to/file2.py] | [What it contains] |

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| [Decision 1] | [Why we chose this] | [Date] |
| [Decision 2] | [Why we chose this] | [Date] |

## Edge Cases Discovered
- [Edge case 1]: [How handled]
- [Edge case 2]: [How handled]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Observability Notes
- Logging: [What to log]
- Metrics: [What to measure]
- Tracing: [Correlation IDs, spans]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]
```

### `<task-name>-tasks.md`

```markdown
# Tasks: [Task Name]

## Progress
- Started: [Date]
- Current slice: [Slice N]
- Status: [In Progress / Blocked / Complete]

## Slices

### Slice 1: [Description]
- [ ] Sub-task 1.1
- [ ] Sub-task 1.2
- [ ] Validation: [Command to run]

### Slice 2: [Description]
- [ ] Sub-task 2.1
- [ ] Sub-task 2.2
- [ ] Validation: [Command to run]

### Tests
- [ ] Unit tests for [component]
- [ ] Integration tests for [flow]
- [ ] Edge case tests

### Documentation
- [ ] API docs updated
- [ ] README updated (if needed)
- [ ] Code comments for non-obvious logic

### Release / Rollback
- [ ] Migration script (if needed)
- [ ] Rollback plan documented
- [ ] Deployment checklist

## Blockers
| Blocker | Status | Resolution |
|---------|--------|------------|
| [Blocker 1] | [Open/Resolved] | [How resolved] |

## Notes
[Any additional notes from implementation]
```

---

## Update Protocol

**Before continuing work on a task:**
1. Read all three files (`-plan.md`, `-context.md`, `-tasks.md`)
2. Verify you understand current state and next steps

**After completing a slice:**
1. Update `-tasks.md` — Check off completed items
2. Update `-context.md` — Add any new decisions or edge cases discovered
3. Summarize what was done and what's next

**When decisions change:**
1. Update `-context.md` with new decision and rationale
2. Update `-plan.md` if the change affects design
3. Update `-tasks.md` if the change affects task list

---

## Compaction Protocol

Before the user compacts (resets) the conversation or starts a fresh session:

1. **Update all dev docs** with:
   - Completed items (check them off)
   - New decisions and rationale
   - Edge cases discovered
   - Next steps clearly stated

2. **Write a handoff summary** at the top of `-tasks.md`:

```markdown
## Handoff Summary (Last Updated: [Date/Time])

**Completed:** Slices 1–3 (user model, login endpoint, middleware)
**Current:** Slice 4 (token refresh)
**Blocked:** None
**Next:** Implement refresh endpoint, then tests

**Key Context:**
- Using PyJWT for tokens
- Decided on 15-min access / 7-day refresh expiry
- Edge case: handle concurrent refresh requests
```

This preserves intent across context loss.

---

## Examples

### Example: Starting a New Task

```
User: "Add rate limiting to the API"

Agent:
This is a medium-sized task (~1 hour). Creating dev docs.

Created:
- dev/active/add-rate-limiting/add-rate-limiting-plan.md
- dev/active/add-rate-limiting/add-rate-limiting-context.md
- dev/active/add-rate-limiting/add-rate-limiting-tasks.md

Plan summary:
- Goal: Add per-user rate limiting (100 req/min)
- 4 slices: middleware, storage, config, tests
- Risk: Redis dependency (mitigated with fallback)

Waiting for plan approval before implementation.
```

### Example: Resuming Work

```
Agent:
Reading dev docs for "add-rate-limiting"...

Current state:
- ✓ Slice 1: Middleware structure
- ✓ Slice 2: Redis storage
- → Slice 3: Configuration (in progress)
- ○ Slice 4: Tests

Continuing with Slice 3: Adding config options for rate limits.
```

### Example: Handoff Before Compaction

```
User: "I need to close this session, please save state"

Agent:
Updating dev docs with current state...

Updated add-rate-limiting-tasks.md:

## Handoff Summary (Last Updated: 2026-02-05 14:30)

**Completed:** Slices 1–2 (middleware, Redis storage)
**Current:** Slice 3 (configuration) — 50% done
**Blocked:** None
**Next:** Finish config loading, then Slice 4 (tests)

**Key Context:**
- Using Redis with 60s TTL for counters
- Config via env vars: RATE_LIMIT_MAX, RATE_LIMIT_WINDOW
- Decided to use sliding window algorithm

Dev docs are up to date. You can safely compact or start a new session.
```
