# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Three core actions a user should be able to perform: 

    For PawPal+, the three core actions I identified are adding a pet, scheduling a care task, and viewing today's schedule. Adding a pet allows the owner to keep track of each animal they care for. Scheduling a task lets the owner create reminders for important routines like feeding, walks, medication, or vet visits. Viewing today's schedule helps the owner see all tasks in one place so they can stay organized and avoid missing important care responsibilities.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    My initial UML design includes four main classes: Owner, Pet, Task, and Scheduler.

    The Owner class is responsible for managing multiple pets and providing access to all of their information. The Pet class stores details about each pet, such as its name, type, and the list of care tasks assigned to it. The Task class represents individual activities like feeding, walking, medication, or vet appointments, and stores information such as the description, scheduled time, frequency, and completion status. The Scheduler class is responsible for organizing tasks, retrieving schedules, sorting tasks by time, filtering tasks, detecting scheduling conflicts, and managing recurring tasks.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
