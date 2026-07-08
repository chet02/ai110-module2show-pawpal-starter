from pawpal_system import Pet, Task


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
