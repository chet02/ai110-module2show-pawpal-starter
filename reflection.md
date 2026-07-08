# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Three core actions a user should be able to perform:

For PawPal+, the three core actions I identified are adding a pet, scheduling a care task, and viewing today's schedule. Adding a pet allows the owner to keep track of each animal they care for. Scheduling a task lets the owner create reminders for important routines like feeding, walks, medication, or vet visits. Viewing today's schedule helps the owner see all tasks in one place so they can stay organized and avoid missing important care responsibilities.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design includes four main classes: Owner, Pet, Task, and Scheduler.

- The Owner class is responsible for managing multiple pets and providing access to all of their information.
- The Pet class stores details about each pet, such as its name, type, and the list of care tasks assigned to it.
- The Task class represents individual activities like feeding, walking, medication, or vet appointments, and stores information such as the description, scheduled time, frequency, and completion status.
- The Scheduler class is responsible for organizing tasks, retrieving schedules, sorting tasks by time, filtering tasks, detecting scheduling conflicts, and managing recurring tasks.

**b. Design changes**

- Did your design change during implementation?

Yes

- If yes, describe at least one change and why you made it.

After reviewing my class skeleton, the AI suggested a few improvements to make the design more reliable and easier to extend.

First, I added unique ID attributes to the Pet and Task classes. This allows each pet and task to be uniquely identified, even if multiple pets have the same name or multiple tasks have the same title.

Second, I added a reference from each Task back to its associated Pet. This makes it easier for the Scheduler to determine which pet a task belongs to when sorting, filtering, or detecting scheduling conflicts.

Finally, I added a placeholder method named `generate_recurring_instances()` to the Scheduler class. Since the project requires recurring tasks later, adding this method now makes it clear that the Scheduler will be responsible for creating future task instances.

I decided to keep the overall class structure the same because I felt the original design was already organized and easy to understand. The AI's suggestions improved the relationships between the classes without making the design more complicated.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The main constraint my scheduler considers is time. Every task has a date and a time, and `Scheduler.get_schedule()` combines them into a real `datetime` (via `Task.get_datetime()`) so tasks can always be sorted earliest to latest, no matter what order they were entered in. When two tasks land on the exact same date and time, I use the pet's name as a tiebreaker so the ordering is stable and predictable instead of arbitrary.

The second constraint is pet identity — which pet a task belongs to. This matters for two things: filtering (`Scheduler.filter_tasks()` can narrow the schedule down to one pet), and conflict detection (`Scheduler.detect_conflicts()` groups same-time tasks by pet to tell the difference between one pet being double-booked versus two different pets both needing attention at once). Completion status is a third, smaller constraint, used only for filtering out finished tasks.

I decided time and pet identity mattered most because they map directly to what a busy pet owner actually needs from this app: a correct chronological plan, and a warning when two things can't realistically both happen. I did not implement priority or task duration as constraints — the `Task` class doesn't have those fields. Given the scope of this project, I chose to spend my effort making the time-based logic (sorting, filtering, conflict detection, recurrence) work correctly and be well-tested, rather than adding a priority-weighting system that wasn't necessary to solve the core scheduling problem.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

During implementation, I learned that Python's `timedelta` supports fixed units such as days and weeks, but not months because calendar months have different numbers of days. I considered using the `dateutil.relativedelta` library, which can accurately handle monthly recurrence by accounting for different month lengths and leap years. However, I decided to keep the simpler `timedelta(days=30)` approach because it met the project requirements, kept the implementation easier to understand, and avoided introducing an additional dependency. While this means monthly recurring tasks are an approximation rather than calendar-accurate, I felt it was an appropriate tradeoff for a beginner-level project.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI throughout the project, not just at the design stage: reviewing my `pawpal_system.py` code for behaviors worth testing, writing the actual test functions in `tests/test_pawpal.py`, updating `app.py`'s display logic to use `Scheduler` methods with clearer Streamlit components, debugging issues I ran into while using the live app, and keeping the README and UML diagram in sync with what I'd actually built.

The most helpful prompts were the specific ones. Asking the AI to "draft the test functions" and naming the exact behaviors I wanted covered — sorting correctness, recurrence logic, conflict detection — produced tests that matched what I actually needed, instead of generic ones. The least helpful pattern was reporting a bug vaguely; it took a couple of follow-up questions from the AI before we found the real cause.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I saw a confusing message in the Conflict Check section (raw text like `<pawpal_system.Task object at 0x...>` instead of a real warning), the AI's first instinct was that this had to be a bug in `detect_conflicts()`. Rather than accept that and start rewriting the method, I asked it to verify first. It actually ran the exact same conflict scenario directly against my `pawpal_system.py` in a plain Python script, and the warnings came out clean — no raw object text at all. That told us the bug wasn't in the code I'd written.

The AI then suggested the real cause was probably a stale Streamlit process that hadn't picked up recent changes. I didn't just take that explanation either. I confirmed it by checking whether I'd actually restarted the server (I hadn't) and whether both tasks had really been saved with the same date and time. Only after restarting the server and re-testing did the conflict warning show up correctly, which confirmed the AI's second hypothesis was the right one and that my original scheduling logic was fine all along.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

My test suite (`tests/test_pawpal.py`) covers six behaviors: marking a task complete, adding a task to a pet, sorting tasks into chronological order across multiple pets, completing a `"daily"` task automatically creating its next occurrence, conflict detection flagging both a single pet double-booked and two different pets needing attention at the same time, and conflict detection correctly reporting no warnings when task times don't overlap.

These were the tests that mattered most because they're the behaviors the whole app depends on. If sorting were wrong, the schedule itself would be useless. If conflict detection had false positives or false negatives, the owner would either be warned about non-problems or miss a real double-booking. Testing the "no conflicts" case alongside the "conflicts exist" case was important too, since a conflict detector that always returns warnings would technically "pass" a test that only checks for the positive case.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'd rate my confidence at 3 out of 5 stars. All 6 tests pass, and I trust the core features — sorting, filtering, recurrence, and conflict detection. I'm less sure about one edge case I haven't tested yet, but can reach through the UI: monthly recurrence uses a flat 30-day jump, so it can drift away from real calendar months (e.g., a task due January 31st would next be due March 2nd, not February 28th). This is the edge case I'd test next if I had more time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the Conflict Check feature in the UI. It would have been easy to just show every warning from `detect_conflicts()` as the same generic message, but instead I split them by severity: a 🚫 error when one pet is double-booked (physically impossible, needs a reschedule) versus a 👥 warning when two different pets need attention at once (harder, but doable with help). That distinction makes the app actually more useful to a pet owner deciding what to do, not just technically correct.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd add a way to actually remove a pet or task from the UI — right now `remove_pet()` and `remove_task()` exist in `pawpal_system.py` but there's no button that calls them, so they're untested by real use. I'd also swap the 30-day `timedelta` approximation for `dateutil.relativedelta` so monthly recurrence lands on the correct calendar date instead of drifting.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that a single design decision early on can simplify everything downstream. Adding the `Task.pet` back-reference felt like a small change at the time, but it's what made `filter_tasks()`, `detect_conflicts()`, and `complete_task()` all straightforward to write later — without it, the `Scheduler` would have needed to search through every pet's task list just to figure out who owned what. Good class design pays off far past the class itself.
