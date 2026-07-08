from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex")

dog = Pet("Rex", "Dog", 3)
cat = Pet("Milo", "Cat", 2)
owner.add_pet(dog)
owner.add_pet(cat)

# Added out of chronological order on purpose, to prove sort_by_time actually sorts them.
dog.add_task(Task("Vet visit", "Annual checkup", "2026-07-07", "16:00", "none"))
cat.add_task(Task("Feed", "Wet food, half a can", "2026-07-07", "12:30", "daily"))
dog.add_task(Task("Walk", "Morning walk around the block", "2026-07-07", "08:00", "daily"))
cat.add_task(Task("Brush", "Quick brushing session", "2026-07-08", "09:00", "none"))

dog.get_tasks()[0].mark_complete()  # mark "Vet visit" complete to demo the status filter

scheduler = Scheduler(owner)
schedule = scheduler.get_schedule()

print("Today's Schedule (sorted by time)")
print("-" * 40)
for task in schedule:
    print(f"{task.date} {task.time} - {task.pet.name}: {task.title}")

print()
print("Filtered: Rex's tasks only")
print("-" * 40)
for task in scheduler.filter_tasks(schedule, pet_name="Rex"):
    print(f"{task.date} {task.time} - {task.title}")

print()
print("Filtered: incomplete tasks only")
print("-" * 40)
for task in scheduler.filter_tasks(schedule, completed=False):
    print(f"{task.date} {task.time} - {task.pet.name}: {task.title}")
