# Planning Protocol

Rules and templates for structured planning before implementation. Accuracy over vibes.

## Table of Contents

1. [Planning Mode](#planning-mode)
2. [Question Templates](#question-templates)
3. [When to Ask vs Proceed](#when-to-ask-vs-proceed)
4. [Neutral Questions](#neutral-questions)
5. [Re-prompting](#re-prompting)
6. [Plan Template](#plan-template)
7. [Examples](#examples)

---

## Planning Mode

When asked to build something non-trivial:

1. **Ask for minimum needed context** — Request only files/constraints directly relevant
2. **Produce a plan** — Include phases, tasks, risks, success criteria
3. **Wait for acceptance** — Do not implement until plan is approved

**Context request order:**
1. Relevant file(s) the user mentions
2. Entry points (main configs, READMEs, key modules)
3. Only then: wider search

Avoid "read the whole repo."

---

## Question Templates

### Scope Questions

- "Should this handle [edge case X]?"
- "What's the expected scale/load?"
- "Are there existing patterns I should follow?"
- "Should this be a separate module or integrated into [existing module]?"

### Constraint Questions

- "Any performance requirements (latency, throughput)?"
- "Compatibility constraints (Python version, browser support, etc.)?"
- "Are there dependencies I should or shouldn't use?"
- "Any security requirements beyond standard practices?"

### Output Format Questions

- "What format should the output be (JSON, YAML, plain text)?"
- "Any existing templates or examples to match?"
- "Should this include tests? Documentation?"
- "Preferred error handling style (exceptions, result types, error codes)?"

### Clarification Questions

- "You mentioned X — did you mean [interpretation A] or [interpretation B]?"
- "The requirement says Y — should that include [related case Z]?"
- "Is this blocking, or can we iterate on it later?"

---

## When to Ask vs Proceed

| Situation | Action |
|-----------|--------|
| Clear, small change (<10 min) | Proceed directly |
| Ambiguous requirements | Ask 1–2 clarifying questions |
| Multiple valid approaches | Present options, ask for preference |
| Large scope (>30 min) | Produce plan, wait for approval |
| Breaking change or risk | Explain risk, confirm before proceeding |
| Missing critical context | Ask for specific file/info needed |

**Decision matrix:**

```
Is the task clear?
├─ Yes → Is it small (<10 min)?
│        ├─ Yes → Proceed
│        └─ No  → Produce plan, wait for approval
└─ No  → Ask 1–2 clarifying questions
```

---

## Neutral Questions

Avoid leading questions that confirm your assumptions. Ask open-ended, neutral questions.

### Wrong — Leading yourself

- "Is this approach good?"
- "Should I use the obvious solution X?"
- "This looks correct, right?"

### Right — Neutral, exploratory

- "What are the tradeoffs of this approach?"
- "What would break if we did X?"
- "What's missing from this design?"
- "What alternatives exist?"
- "What edge cases should we consider?"

---

## Re-prompting

If output is off-target:

1. **Restate constraints** — Be explicit about what was missed
2. **Add negative constraints** — "Do NOT do X; instead do Y"
3. **Keep the plan stable** — Adjust only the failing slice, not the whole plan
4. **Provide examples** — Show what good output looks like

---

## Plan Template

Use this structure for non-trivial work:

```markdown
# Plan: [Feature/Task Name]

## Goal
[One sentence describing the end state]

## Non-goals (YAGNI guard)
- [Things explicitly out of scope]
- [Avoid scope creep]

## Proposed Design

### Components
- [Component 1]: [Responsibility]
- [Component 2]: [Responsibility]

### Data Flow
[How data moves through the system]

### Public API Changes
[New endpoints, functions, or interfaces]

## Tasks
- [ ] Slice 1: [Description]
- [ ] Slice 2: [Description]
- [ ] Tests: [Description]
- [ ] Docs: [Description]

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [How to address] |
| [Risk 2] | [How to address] |

## Validation Plan
[Exact commands to verify success]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

## Examples

### Example: Clarifying Questions Before Implementation

```
User: "Add caching to the API"

Agent:
Before I implement caching, a few questions:

1. **Scope**: Should this cache all endpoints or specific ones?
2. **Storage**: In-memory (Redis/Memcached) or local (file-based)?
3. **Invalidation**: Time-based expiry, or invalidate on write?
4. **Constraints**: Any memory limits or latency requirements?

Once clarified, I'll produce a detailed plan.
```

### Example: Plan for Non-Trivial Work

```
User: "Add user authentication"

Agent:
# Plan: User Authentication

## Goal
Add JWT-based authentication with login/logout endpoints.

## Non-goals
- OAuth/social login (future iteration)
- Password reset flow (separate task)
- Rate limiting (separate task)

## Proposed Design

### Components
- `auth/models.py`: User model with hashed password
- `auth/routes.py`: Login, logout, refresh endpoints
- `auth/middleware.py`: JWT validation middleware
- `auth/utils.py`: Token generation, password hashing

### Data Flow
1. User submits credentials → validate → issue JWT
2. Subsequent requests include JWT → middleware validates → proceed or 401

## Tasks
- [ ] Slice 1: User model + password hashing
- [ ] Slice 2: Login endpoint + token generation
- [ ] Slice 3: Middleware + protected route example
- [ ] Slice 4: Logout + token refresh
- [ ] Tests: Unit + integration tests
- [ ] Docs: API documentation

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Token leakage | Use short expiry, secure cookies |
| Brute force | Add rate limiting (noted for future) |

## Validation Plan
- `pytest tests/auth/` — all pass
- Manual test: login, access protected route, logout
- Security review checklist

## Success Criteria
- [ ] Can register and login
- [ ] Protected routes require valid token
- [ ] Tokens expire and can be refreshed
- [ ] No plaintext passwords stored

Waiting for approval before implementation.
```

### Example: Re-prompting After Off-Target Output

```
User: "The output is too verbose, I wanted just the core logic"

Agent:
Understood. Let me restate the constraints:

**Constraints:**
- Core logic only, no boilerplate
- No comments unless non-obvious
- Minimal error handling (just the happy path)

**Do NOT:**
- Add logging or metrics
- Include full class definitions
- Add docstrings

Here's the revised implementation:
[minimal code]
```
