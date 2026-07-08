class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def remove_pet(self, pet_name):
        pass

    def get_all_tasks(self):
        pass


class Pet:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        pass

    def remove_task(self, task_title):
        pass

    def get_tasks(self):
        pass


class Task:
    def __init__(self, title, notes, date, time, frequency):
        self.title = title
        self.notes = notes
        self.date = date
        self.time = time
        self.frequency = frequency
        self.completed = False

    def mark_complete(self):
        pass


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_schedule(self):
        pass

    def sort_by_time(self, tasks):
        pass

    def filter_tasks(self, tasks, pet_name, completed):
        pass

    def detect_conflicts(self, tasks):
        pass
