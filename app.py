"""Streamlit UI for PawPal+: add pets and tasks, then sort, filter, and
detect scheduling conflicts via the Scheduler class in pawpal_system.py."""

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner)
scheduler = st.session_state.scheduler

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    if owner.add_pet(Pet(pet_name, species, int(age))):
        st.success(f"Added {pet_name} to {owner.name}'s pets.")
    else:
        st.error(f"{pet_name} already exists for {owner.name}.")

if owner.pets:
    st.write("Current pets:")
    st.table([{"Name": p.name, "Species": p.species, "Age": p.age} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
st.caption("Tasks are attached to a specific pet.")

if not owner.pets:
    st.info("Add a pet before scheduling tasks.")
else:
    pet_lookup = {pet.name: pet for pet in owner.pets}
    selected_pet_name = st.selectbox("Pet", list(pet_lookup.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_date = st.date_input("Date")
    with col3:
        task_time = st.time_input("Time")

    task_notes = st.text_input("Notes", value="")
    task_frequency = st.selectbox("Frequency", ["none", "daily", "weekly", "monthly"])

    if st.button("Add Task"):
        selected_pet = pet_lookup[selected_pet_name]
        selected_pet.add_task(
            Task(
                task_title,
                task_notes,
                task_date.strftime("%Y-%m-%d"),
                task_time.strftime("%H:%M"),
                task_frequency,
            )
        )
        st.success(f"Added '{task_title}' for {selected_pet.name}.")

all_tasks = scheduler.get_schedule()

st.subheader("Conflict Check")
conflict_warnings = scheduler.detect_conflicts(all_tasks)
if not conflict_warnings:
    st.success("✅ No scheduling conflicts — you're all set.")
else:
    for warning in conflict_warnings:
        if "double-booked" in warning:
            # Same pet needed in two places at once: physically impossible, needs a reschedule.
            st.error(f"🚫 {warning}")
        elif "Skipped" in warning:
            # Not a real conflict — bad data hid a task from the conflict scan entirely.
            st.warning(f"🛠️ {warning}")
        else:
            # Different pets need attention at once: doable with help, but plan ahead.
            st.warning(f"👥 {warning}")

st.write("Current tasks:")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
with filter_col2:
    hide_completed = st.checkbox("Hide completed")

visible_tasks = scheduler.filter_tasks(
    all_tasks,
    pet_name=None if pet_filter == "All" else pet_filter,
    completed=False if hide_completed else None,
)

if visible_tasks:
    header = st.columns([0.6, 1.5, 2, 2, 1.3])
    for col, label in zip(header, ["Done", "Pet", "Title", "Date / Time", "Frequency"]):
        col.markdown(f"**{label}**")

    for task in visible_tasks:
        row = st.columns([0.6, 1.5, 2, 2, 1.3])
        with row[0]:
            done = st.checkbox(
                "Done",
                value=task.completed,
                disabled=task.completed,
                key=f"complete_{task.id}",
                label_visibility="collapsed",
            )
            if done and not task.completed:
                scheduler.complete_task(task)
                st.rerun()
        row[1].write(task.pet.name if task.pet else "")
        row[2].write(task.title)
        row[3].write(f"{task.date} {task.time}")
        row[4].write(task.frequency)
else:
    st.info("No tasks match this filter.")

st.divider()

st.subheader("Build Schedule")
st.caption("Shows all tasks sorted chronologically by date and time.")

if st.button("Generate schedule"):
    schedule = scheduler.get_schedule()
    if schedule:
        st.success(f"✅ Sorted {len(schedule)} task(s) chronologically.")
        st.table(
            [
                {
                    "Date": task.date,
                    "Time": task.time,
                    "Pet": task.pet.name if task.pet else "",
                    "Task": task.title,
                    "Status": "✅ Done" if task.completed else "⏳ Pending",
                }
                for task in schedule
            ]
        )
    else:
        st.info("No tasks to schedule yet.")
