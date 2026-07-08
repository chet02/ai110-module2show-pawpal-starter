from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex")

dog = Pet("Rex", "Dog", 3)
cat = Pet("Milo", "Cat", 2)
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Walk", "Morning walk around the block", "2026-07-07", "08:00", "daily"))
cat.add_task(Task("Feed", "Wet food, half a can", "2026-07-07", "12:30", "daily"))
dog.add_task(Task("Vet visit", "Annual checkup", "2026-07-07", "16:00", "none"))

scheduler = Scheduler(owner)
schedule = scheduler.get_schedule()

print("Today's Schedule")
print("-" * 20)
for task in schedule:
    print(f"{task.time} - {task.pet.name}: {task.title}")
