from datetime import datetime, timedelta


class Owner:
    def __init__(self, name):
        """Create an owner with a name and an empty list of pets."""
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove the first pet matching the given name."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                break

    def get_all_tasks(self):
        """Return a combined list of tasks from all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Pet:
    _next_id = 1

    def __init__(self, name, species, age):
        """Create a pet with a unique id, name, species, age, and an empty task list."""
        self.id = Pet._next_id
        Pet._next_id += 1
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        """Link a task to this pet and add it to the pet's task list."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task_title):
        """Remove the first task matching the given title."""
        for task in self.tasks:
            if task.title == task_title:
                self.tasks.remove(task)
                break

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks


class Task:
    _next_id = 1

    def __init__(self, title, notes, date, time, frequency, pet=None):
        """Create a task with a unique id, its details, and completed set to False."""
        self.id = Task._next_id
        Task._next_id += 1
        self.title = title
        self.notes = notes
        self.date = date
        self.time = time
        self.frequency = frequency
        self.completed = False
        self.pet = pet

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def get_datetime(self):
        """Return this task's date and time combined into one datetime object."""
        return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")


class Scheduler:
    _FREQUENCY_DELTAS = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
        "monthly": timedelta(days=30),  # approximation, not calendar-accurate
    }

    def __init__(self, owner):
        """Create a scheduler tied to one owner."""
        self.owner = owner

    def get_schedule(self):
        """Return all of the owner's tasks sorted by time."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def sort_by_time(self, tasks):
        """Return the given tasks sorted from earliest to latest."""
        return sorted(tasks, key=lambda task: task.get_datetime())

    def filter_tasks(self, tasks, pet_name=None, completed=None):
        """Return only the tasks matching the given pet name and/or completed status."""
        filtered = tasks
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet and task.pet.name == pet_name]
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        return filtered

    def detect_conflicts(self, tasks):
        """Return pairs of tasks that are scheduled at the exact same date and time."""
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                if sorted_tasks[i].get_datetime() != sorted_tasks[j].get_datetime():
                    break
                conflicts.append((sorted_tasks[i], sorted_tasks[j]))
        return conflicts

    def generate_recurring_instances(self, task, count=1):
        """Create the next 'count' future occurrences of a recurring task."""
        delta = self._FREQUENCY_DELTAS.get(task.frequency)
        if delta is None:
            return []

        instances = []
        next_datetime = task.get_datetime()
        for _ in range(count):
            next_datetime += delta
            instances.append(Task(
                title=task.title,
                notes=task.notes,
                date=next_datetime.strftime("%Y-%m-%d"),
                time=next_datetime.strftime("%H:%M"),
                frequency=task.frequency,
                pet=task.pet,
            ))
        return instances
