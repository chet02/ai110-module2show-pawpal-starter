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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```
What the tests cover (`tests/test_pawpal.py`) — see [Smarter Scheduling](#-smarter-scheduling) below for how each behavior actually works:

- **Task basics** — marking a task complete, adding a task to a pet.
- **Sorting correctness** — `Scheduler.get_schedule()`.
- **Recurrence logic** — `Scheduler.complete_task()`.
- **Conflict detection** — `Scheduler.detect_conflicts()`, including a no-conflicts case.

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

### Main UI features (`app.py`)

- **Owner** — set the pet owner's name.
- **Add a Pet** — add a pet by name, species, and age; duplicate names (case-insensitive) are rejected.
- **Schedule a Task** — attach a task (title, notes, date, time, frequency) to a specific pet.
- **Conflict Check** — automatically flags scheduling problems: 🚫 a single pet double-booked at the same time, 👥 different pets both needing attention at once, or ✅ a clean schedule.
- **Current tasks** — filter the task list by pet and/or hide completed tasks, and check off a task as done.
- **Build Schedule** — generate the full task list sorted chronologically.

### Example workflow

1. Set the owner's name (e.g., "Alex") and add two pets, "Rex" (dog) and "Milo" (cat).
2. Schedule "Walk" for Rex at 08:00 and "Feed" for Milo at the same date and time.
3. The Conflict Check panel immediately flags "Multiple pets need attention at ... : Milo, Rex" since both need care at once.
4. Click "Generate schedule" to see every task sorted earliest to latest, regardless of the order they were added.
5. Check off "Walk" as done — since it's a `"daily"` task, `complete_task()` automatically schedules a new "Walk" task for the next day.

### Key Scheduler behaviors shown

Steps 4 and 3/5 above exercise sorting and conflict detection/recurrence, respectively — see [Smarter Scheduling](#-smarter-scheduling) for how `get_schedule()`, `filter_tasks()`, `detect_conflicts()`, and `complete_task()` work under the hood.

### Sample CLI output (`python main.py`)

`main.py` exercises the same `Scheduler` behind a plain terminal script — it adds tasks out of order on purpose, then prints the sorted schedule and two filtered views:

```
Today's Schedule (sorted by time)
----------------------------------------
2026-07-07 08:00 - Rex: Walk
2026-07-07 12:30 - Milo: Feed
2026-07-07 16:00 - Rex: Vet visit
2026-07-08 09:00 - Milo: Brush

Filtered: Rex's tasks only
----------------------------------------
2026-07-07 08:00 - Walk
2026-07-07 16:00 - Vet visit

Filtered: incomplete tasks only
----------------------------------------
2026-07-07 08:00 - Rex: Walk
2026-07-07 12:30 - Milo: Feed
2026-07-08 09:00 - Milo: Brush
```
