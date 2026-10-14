# Goa Heritage & Culture Guide Agent — Project Instructions

## 1. Project Overview

This project is an AI-powered **Goa Heritage & Culture Guide Agent** designed as an MSc Artificial Intelligence project.

The system is a knowledge-first heritage and culture companion for Goa.

Its primary capabilities are:

- Explain Goa's historical and cultural heritage.
- Explain the significance and symbolism of heritage places.
- Identify places or structures from user descriptions.
- Answer questions about traditions and religious/cultural practices.
- Provide respectful visitor etiquette.
- Discover heritage places dynamically across Goa.
- Build dynamic multi-day heritage trails.
- Find and match festivals with travel dates.
- Display heritage places, events, and routes on Google Maps.
- Maintain conversation context and user constraints.
- Provide grounded answers with sources.
- Explicitly communicate uncertainty instead of inventing historical or cultural facts.

This is NOT a generic travel-planning application.

The primary focus is:

**heritage + culture + grounded research + dynamic discovery + intelligent routing.**

---

# 2. Core Architecture

The project uses:

- Python
- LangChain
- Deep Agents
- LangGraph
- Groq or another supported LLM provider
- Streamlit
- Google Maps/Places/Routes
- Wikipedia
- Web search provider(s)
- LangSmith
- Persistent state/checkpointing

The architectural relationship is:

```text
Streamlit
    ↓
Main Deep Agent
    ↓
LangGraph
    ↓
State + Checkpointer
    ↓
Subagents / Tools / Middleware
```

Deep Agents provide the agent capabilities.

LangGraph provides stateful execution, thread-based conversation state, and checkpointing.

Do NOT treat Deep Agents and LangGraph as competing alternatives.

---

# 3. Conversation Architecture

Every independent conversation must have its own `thread_id`.

Conceptually:

```text
User
 ├── Chat A → thread_id A
 ├── Chat B → thread_id B
 └── Chat C → thread_id C
```

Conversation state must never leak between different threads.

The application should initially support a single active chat, but the architecture must be designed so that multi-chat can be added later without redesigning the agent.

The long-term UI should behave similarly to ChatGPT:

```text
+ New Chat

Chat 1
Chat 2
Chat 3
```

Each chat maps to an independent LangGraph thread.

---

# 4. Memory Rules

Do not use the sandbox as the primary conversation-memory mechanism.

Conversation memory should be handled through:

- LangGraph state
- `thread_id`
- LangGraph checkpointer
- structured constraint state

The filesystem should be used for artifacts such as:

```text
notes/
trails/
events/
cache/
```

Important user constraints should be extracted into structured state instead of relying entirely on raw conversation history.

Example:

```json
{
  "days": 3,
  "interests": ["temples", "Portuguese history"],
  "pace": "relaxed",
  "place_preference": "lesser_known",
  "starting_point": "Panjim",
  "region_order": null
}
```

Never assume a regional order unless the user explicitly requests one.

---

# 5. Geographic Scope Rule

This is a critical project requirement.

The system MUST NOT hardcode:

```text
North Goa → Panjim → South Goa
```

as the default itinerary or traversal order.

Any example involving North Goa, Panjim, or South Goa is illustrative only.

Geographic scope and ordering must be determined dynamically from the user's request.

Examples:

```text
"Explore Goa heritage"
→ potentially search across Goa.

"South Goa heritage"
→ focus on South Goa.

"Ponda temples"
→ focus on Ponda and relevant nearby places.

"North first, then South"
→ explicitly preserve that order.

"3 days around Panjim"
→ optimize around Panjim.

"Show me hidden heritage places"
→ prioritize lesser-known/local places.
```

The system must respect explicit geographic constraints but must not invent them.

---

# 6. Heritage Seed Dataset

The project will maintain:

```text
data/goa_heritage_seed.json
```

This is a curated discovery/index dataset.

It is NOT the complete RAG knowledge base.

It should initially contain approximately 40–50 carefully curated heritage places and can later grow to 80–120+ entries.

The seed should contain compact metadata such as:

- id
- name
- aliases
- area
- district/region
- type
- themes
- significance
- description
- local/famous classification
- popularity classification
- latitude
- longitude
- source URLs
- verification status
- last verified date

Do NOT put thousands of words of historical content into each seed record.

The seed is primarily used for:

- candidate discovery
- geographic filtering
- place identification
- initial metadata
- trail candidate generation

Detailed factual claims should be retrieved and verified through appropriate sources.

---

# 7. No Hallucination Rule

Historical, cultural, religious, architectural, and ritual claims must be grounded.

For important factual claims such as:

- dates
- centuries
- founders
- historical events
- architectural claims
- rituals
- religious practices
- festival dates
- opening hours

the system should retrieve supporting information.

Never invent information merely to provide a complete answer.

When reliable information cannot be found, explicitly say so.

Use confidence categories where appropriate:

- Well documented
- Commonly said / varies by tradition or community
- Not confirmed

For ritual or religious practices, avoid presenting one local practice as universal.

When exact local meaning is uncertain, recommend confirming with the relevant temple/church/mosque/local authority.

---

# 8. Source Requirements

Important factual answers should contain sources.

Preferred source hierarchy depends on the claim, but generally prioritize:

1. Official government/heritage sources
2. Archaeological/heritage institutions
3. Official religious/institutional sources
4. UNESCO or recognized heritage organizations
5. Reliable academic/historical sources
6. Wikipedia for discovery/background
7. General web sources for filling verified gaps

Wikipedia should not automatically be treated as the final authority for every claim.

---

# 9. Main Agent

The main agent is the orchestrator.

It should:

- understand user intent
- maintain context
- interpret constraints
- delegate to subagents
- coordinate tools
- validate results
- compose the final answer

The main agent should NOT independently invent domain facts when a Researcher subagent should retrieve them.

Subagents:

```text
Main Deep Agent
    ├── Heritage Researcher
    ├── Festival Agent
    └── Trail Planner
```

---

# 10. Heritage Researcher

The Heritage Researcher handles:

- explain mode
- identify mode
- historical research
- cultural significance
- symbolism
- religious/cultural etiquette
- place research
- trail-stop enrichment

Research order should generally be:

```text
Seed
  ↓
Wikipedia / known sources
  ↓
Web search for missing information
  ↓
Fetch authoritative/relevant sources
  ↓
Structured research note
```

The Researcher should return compact structured information rather than raw webpages.

---

# 11. Festival Agent

The Festival Agent handles:

- festival discovery
- current festival dates
- travel-date matching
- location
- date confidence
- source verification

Never invent festival dates.

Lunar-calendar dates should be verified against current/reliable sources.

Festival results should distinguish:

- confirmed
- approximate
- unconfirmed

Unconfirmed festival events should not automatically become confirmed map pins.

---

# 12. Trail Planner

The Trail Planner creates heritage trails only after relevant candidate places are available.

Trail planning has two stages:

### Stage 1 — Candidate generation

Use:

- seed dataset
- Places search
- geographic constraints
- user interests
- local/famous preference

Generate candidate places and show them to the user when appropriate.

### Stage 2 — Final routing

After confirmation:

- cluster geographically
- calculate travel times
- assign places to days
- optimize the route
- respect explicit geographic ordering
- respect user pace
- avoid duplicate places
- consider meals/lunch if requested

Suggested stop limits:

```text
Relaxed → 2–3 stops/day
Normal  → 3–4 stops/day
Fast    → more only when practical
```

Do not force an itinerary to contain too many stops.

---

# 13. Dynamic Routing

Routing must be dynamic.

The system must consider:

- user starting point
- requested geographic area
- requested regions
- explicit region ordering
- place coordinates
- travel time
- number of days
- user pace
- interests
- selected places

Never implement a fixed route such as:

```text
North → Panjim → South
```

unless the user explicitly requests it.

---

# 14. API Provider Architecture

External providers must be abstracted.

Do not scatter provider-specific calls throughout the codebase.

Use routers/adapters such as:

```text
infrastructure/
    llm_router.py
    search_router.py
    maps_router.py
    quota_manager.py
```

The application should request a capability:

```text
LLM generation
Web search
Places search
Routing
```

rather than directly depending on one provider everywhere.

Provider failure should be handled through legitimate fallback providers/configurations.

Never design API rotation to circumvent provider terms, quotas, or account restrictions.

The LLM provider should be replaceable without changing conversation memory.

---

# 15. Tools

Tools should return compact structured results.

Prefer:

```python
{
    "ok": True,
    "data": ...
}
```

or:

```python
{
    "ok": False,
    "error": "..."
}
```

Avoid returning large raw HTML responses directly to agents.

Initial tools include:

```text
wikipedia_lookup()
web_search()
fetch_page()
lookup_heritage_seed()
places_search()
geocode_place()
get_distance_time()
show_on_map()
save_trail()
```

---

# 16. Middleware

The project will eventually contain:

```text
middleware/
    constraints.py
    grounding.py
    validation.py
```

### ConstraintStateMiddleware

Updates structured user constraints from new messages.

### GroundingGuardMiddleware

Checks important factual claims against retrieved sources.

### TrailValidationMiddleware

Checks:

- day count
- geographic scope
- explicit region order
- duplicate places
- travel feasibility
- etiquette
- sources
- festival status

Middleware should not silently change user requirements.

---

# 17. Project Structure

Target structure:

```text
goa-heritage-agent/
│
├── .github/
│   └── copilot-instructions.md
│
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── prompts.py
│   └── state.py
│
├── agents/
│   ├── heritage_researcher.py
│   ├── festival_agent.py
│   └── trail_planner.py
│
├── tools/
│   ├── wikipedia.py
│   ├── web_search.py
│   ├── fetch_page.py
│   ├── heritage_seed.py
│   ├── places.py
│   ├── routes.py
│   ├── map.py
│   └── save_trail.py
│
├── middleware/
│   ├── constraints.py
│   ├── grounding.py
│   └── validation.py
│
├── infrastructure/
│   ├── llm_router.py
│   ├── search_router.py
│   ├── maps_router.py
│   └── quota_manager.py
│
├── data/
│   └── goa_heritage_seed.json
│
├── state/
│
├── notes/
├── trails/
├── events/
├── cache/
├── tests/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

Do not create all files immediately.

Create components as their respective development phases begin.

---

# 18. Coding Principles

Write clean, modular Python.

Prefer small functions with clear responsibilities.

Do not create giant files.

Do not duplicate provider/API logic.

Use type hints where practical.

Use descriptive names.

Handle API failures explicitly.

Do not hide exceptions that are useful for debugging.

Keep secrets out of source code.

Never commit `.env`.

Use environment variables for API credentials.

---

# 19. Development Rules

Implement the project incrementally.

Do not build the entire system in one step.

After each major component:

1. implement
2. run it
3. test it
4. inspect errors
5. fix it
6. only then move to the next component

Do not introduce advanced infrastructure before it is needed.

Prefer the simplest implementation that satisfies the current phase.

---

# 20. Current Development Order

Follow this order:

```text
Phase 1  → Project Foundation
Phase 2  → Conversation & State
Phase 3  → Heritage Seed
Phase 4  → Retrieval Tools
Phase 5  → Heritage Researcher
Phase 6  → Main Deep Agent
Phase 7  → API/Provider Router
Phase 8  → Middleware / Grounding
Phase 9  → Festival Agent
Phase 10 → Dynamic Discovery
Phase 11 → Trail Planner
Phase 12 → Trail Validation
Phase 13 → Google Maps
Phase 14 → Streamlit Product UI
Phase 15 → Multi-Chat
Phase 16 → Persistence
Phase 17 → Observability
Phase 18 → Evaluation
Phase 19 → Deployment
Phase 20 → Documentation
```

Do not skip ahead unless explicitly instructed.

---

# 21. Current Phase

The current phase is:

**Phase 1 — Project Foundation**

Focus only on:

- repository setup
- Python environment
- dependency management
- `.env`
- `.gitignore`
- basic project structure
- LangChain/Deep Agents/LangGraph foundation
- Groq configuration
- minimal Streamlit application
- basic application startup

Do NOT implement the full agent, RAG, trail planner, festival agent, Google Maps, or multi-chat yet.

---

# 22. Copilot Behavior

When generating code for this project:

- First understand the existing project structure.
- Follow these instructions before generating new files.
- Do not overwrite existing working code unnecessarily.
- Reuse existing utilities.
- Check whether a component already exists before creating another.
- Keep changes limited to the current development phase.
- Explain important architectural decisions briefly.
- When an external library API may have changed, verify the installed version/API before assuming syntax.
- Do not invent library APIs.
- Do not hardcode API keys.
- Do not hardcode Goa itinerary ordering.
- Do not fabricate heritage facts or sources.
- Do not introduce unnecessary dependencies.

When modifying existing code, preserve working behavior unless the requested change requires otherwise.

---

# 23. Definition of Done

A phase is complete only when:

- the implementation exists
- it runs successfully
- basic tests/manual verification pass
- errors are handled appropriately
- the project structure remains clean
- the implementation follows this document

Only then should development proceed to the next phase.