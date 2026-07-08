# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

    Today's Schedule
    --------------------
    08:00 - Rex: Walk
    12:30 - Milo: Feed
    16:00 - Rex: Vet visit

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```
What the tests cover (`tests/test_pawpal.py`):

- **Task basics** — marking a task complete flips its status; adding a task to a pet increases that pet's task count.
- **Sorting correctness** — tasks added out of chronological order across multiple pets come back from `Scheduler.get_schedule()` sorted earliest-to-latest.
- **Recurrence logic** — completing a `"daily"` task marks it done and automatically schedules a new, incomplete follow-up task for the next occurrence.
- **Conflict detection** — `Scheduler.detect_conflicts()` flags a single pet double-booked at the same time and different pets both needing attention at once, and reports no warnings when task times don't overlap.

Sample test output:

```
============================= test session starts ==============================
collected 6 items

tests/test_pawpal.py ......                                              [100%]

============================== 6 passed in 0.02s ===============================

```

**Confidence level: ★★★☆☆ (3/5)**

All 6 tests pass, and the core happy paths — sorting, filtering, recurrence, and conflict detection between assigned pets — are verified. Confidence isn't higher because several edge cases aren't covered yet: conflicts between unassigned (no-pet) tasks at the same time, malformed date/time strings outside `detect_conflicts`, duplicate task titles on removal, and the 30-day (non-calendar-accurate) monthly recurrence math. Treat this as solid on the primary workflow, less proven on the edges.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by `Task.get_datetime()` (date + time combined into a real `datetime`), tie-breaking on pet name so same-time tasks have a stable order. Used internally by `Scheduler.get_schedule()`. |
| Filtering | `Scheduler.filter_tasks()` | Filters a task list by pet name and/or completion status; either can be omitted to skip that filter. Powers the "Filter by pet" and "Hide completed" controls in `app.py`. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups the sorted list by exact same date+time with `itertools.groupby`, then flags both a single pet double-booked and different pets both needing attention at once. Returns ready-to-display warning strings and skips any task with unparseable date/time data instead of crashing. |
| Recurring tasks | `Scheduler.complete_task()` | Marking a task complete rolls it forward automatically for `"daily"`/`"weekly"`/`"monthly"` frequencies (via `Scheduler._FREQUENCY_DELTAS`), scheduling the next occurrence at *today's date* + the frequency offset (not the original due date), keeping the same time-of-day. Non-recurring tasks just get marked complete. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
