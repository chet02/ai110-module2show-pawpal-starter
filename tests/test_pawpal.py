from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Feed", "Wet food", "2026-07-07", "12:30", "daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Rex", "Dog", 3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Walk", "Morning walk", "2026-07-07", "08:00", "daily"))

    assert len(pet.tasks) == 1


def test_get_schedule_returns_tasks_in_chronological_order():
    owner = Owner("Alex")
    dog = Pet("Rex", "Dog", 3)
    cat = Pet("Milo", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Added out of order on purpose to prove sorting actually happens.
    dog.add_task(Task("Vet visit", "Annual checkup", "2026-07-07", "16:00", "none"))
    cat.add_task(Task("Feed", "Wet food", "2026-07-07", "12:30", "daily"))
    dog.add_task(Task("Walk", "Morning walk", "2026-07-07", "08:00", "daily"))
    cat.add_task(Task("Brush", "Quick brushing", "2026-07-08", "09:00", "none"))

    scheduler = Scheduler(owner)
    schedule = scheduler.get_schedule()

    assert [task.title for task in schedule] == ["Walk", "Feed", "Vet visit", "Brush"]


def test_completing_daily_task_creates_next_day_instance():
    owner = Owner("Alex")
    dog = Pet("Rex", "Dog", 3)
    owner.add_pet(dog)

    task = Task("Walk", "Morning walk", "2026-07-07", "08:00", "daily")
    dog.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.complete_task(task)

    assert task.completed is True
    assert len(dog.tasks) == 2

    new_task = dog.tasks[-1]
    assert new_task.title == "Walk"
    assert new_task.completed is False
    assert new_task.time == "08:00"
    assert new_task.date != task.date


def test_detect_conflicts_flags_tasks_at_duplicate_times():
    owner = Owner("Alex")
    dog = Pet("Rex", "Dog", 3)
    cat = Pet("Milo", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Same pet, double-booked at the same time.
    dog.add_task(Task("Walk", "Morning walk", "2026-07-07", "08:00", "daily"))
    dog.add_task(Task("Vet visit", "Checkup", "2026-07-07", "08:00", "none"))

    # Different pets both needing attention at the same time.
    cat.add_task(Task("Feed", "Wet food", "2026-07-07", "08:00", "daily"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(scheduler.get_schedule())

    assert any("Rex is double-booked" in warning for warning in warnings)
    assert any("Multiple pets need attention" in warning for warning in warnings)


def test_detect_conflicts_no_warnings_for_distinct_times():
    owner = Owner("Alex")
    dog = Pet("Rex", "Dog", 3)
    owner.add_pet(dog)

    dog.add_task(Task("Walk", "Morning walk", "2026-07-07", "08:00", "daily"))
    dog.add_task(Task("Vet visit", "Checkup", "2026-07-07", "16:00", "none"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(scheduler.get_schedule())

    assert warnings == []
