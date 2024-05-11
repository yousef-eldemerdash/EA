# University timetable scheduling problem is a CONSTRAINED OPTIMIZATION type problem

import numpy as np
import random
import Classes
import Data
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


class Timetable:
    def __init__(self, position, w, c1, c2):
        self.current_position = position
        self.velocity = np.zeros_like(self.current_position)
        self.personal_best_position = self.current_position.copy()
        self.personal_best_fitness = float('inf')
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def update_current_position(self):
        new_position = self.current_position + self.velocity
        new_position = np.clip(new_position, 0, len(Classes.Course.courses)-1)
        new_position = np.floor(new_position)
        self.current_position = new_position
        return new_position

    def update_velocity(self, swarm_best_position):
        r1 = np.random.rand(len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms))
        r2 = np.random.rand(len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms))
        cognitive_component = self.c1 * r1 * (self.personal_best_position-self.current_position)
        social_component = self.c2 * r2 * (swarm_best_position-self.current_position)
        new_velocity = self.w * self.velocity + cognitive_component + social_component
        self.velocity = new_velocity

    def update_personal_best_position(self, new_best_position):
        self.personal_best_position = new_best_position

    def update_personal_best_fitness(self, new_fitness):
        self.personal_best_fitness = new_fitness

    def calculate_fitness(self, current_position):
        penalties = 0

        # Initialize dictionaries to keep track of course and instructor occurrences
        course_count_per_week = {course.code: 0 for course in Classes.Course.courses}
        timeslot = 0

        for timeslot_idx in range(current_position.shape[0]):
            course_count_per_timeslot = {course.code: 0 for course in Classes.Course.courses}
            instructor_count_per_timeslot = {instructor.name: 0 for instructor in Classes.FacultyMember.faculty_members}
            department_count_per_timeslot = {course.department: 0 for course in Classes.Course.courses}
            timeslot +=1
            for classroom_idx in range(current_position.shape[1]):
                course_id = current_position[timeslot_idx, classroom_idx]
                if course_id != -1:
                    course = Classes.Course.courses[int(course_id)]
                    instructor = course.instructor.name
                    department = course.department

                    # Check if course is given more than once in a single timeslot
                    if course_count_per_timeslot[course.code] > 0:
                        penalties += 1
                    course_count_per_timeslot[course.code] += 1

                    # Check if course is given more than once in a week
                    if course_count_per_week[course.code] > 0:
                        penalties += 1
                    course_count_per_week[course.code] += 1

                    # Check if courses with similar departments appeared in the same timeslot
                    if department_count_per_timeslot[department] > 0:
                        penalties += 1
                    department_count_per_timeslot[department] += 1

                    # Check if instructor is booked more than once in the same timeslot
                    if instructor_count_per_timeslot[instructor] > 0:
                        penalties += 1
                    instructor_count_per_timeslot[instructor] += 1
        return penalties

def PSO(Pop_size, Max_itr, w, c1, c2):
    swarm_best_position = None
    swarm_best_fitness = float('inf')
    timetables = []
    best_fitnesses = []

    # Initialize a dictionary to store instructor IDs for each course
    course_ids = {course: idx for idx, course in enumerate(Classes.Course.courses)}

    # Position random initialization
    for itr in range(Pop_size):
        random_position = np.zeros((len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms)), dtype=float)

        # Initialize the timetable with course identifiers
        for i in range(len(Classes.Timeslot.timeslots)):
            for j in range(len(Classes.Classroom.classrooms)):
                # Replacing the zeros with course identifiers
                course = random.choice(Classes.Course.courses)
                course_id = course_ids[course]
                random_position[i, j] = course_id
        random_timetable = Timetable(random_position, w, c1, c2)
        timetables.append(random_timetable)

        # Fitness update
        fitness = random_timetable.calculate_fitness(random_position)

        if fitness < swarm_best_fitness:
            swarm_best_fitness = fitness
            swarm_best_position = random_position
        if fitness < random_timetable.personal_best_fitness:
            random_timetable.update_personal_best_fitness(fitness)
            random_timetable.update_personal_best_position(random_position)

    # Velocity random Initialization
    for timetable in timetables:
        random_velocity = np.zeros((len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms)),dtype=float)

        for i in range(len(Classes.Timeslot.timeslots)):
            for j in range(len(Classes.Classroom.classrooms)):
                course = random.choice(Classes.Course.courses)
                course_id = course_ids[course]
                random_velocity[i, j] = course_id

        timetable.velocity = random_velocity

    # optimization loop
    for itr in range(Max_itr):
        for timetable in timetables:
            # updating particle's velocity:
            timetable.update_velocity(swarm_best_position)
            # updating particle's position:
            position = timetable.update_current_position()
            # Evaluate particle's fitness:
            fitness = timetable.calculate_fitness(position)
            if fitness < timetable.personal_best_fitness:
                timetable.update_personal_best_fitness(fitness)
                timetable.update_personal_best_position(position)
            if fitness < swarm_best_fitness:
                swarm_best_fitness = fitness
                swarm_best_position = position

        best_fitnesses.append(swarm_best_fitness)

    # Table printing with it's fitness
    print(f"Swarm best fitness: {swarm_best_fitness} (AKA total number of clashes)")
    for day_idx, day in enumerate(Data.days):
        for timeslot_idx, start_time in enumerate(Data.start_times):
            for classroom_idx, cell in enumerate(swarm_best_position[timeslot_idx + (day_idx * len(Data.start_times))]):
                course_id = int(cell)
                course_name = Classes.Course.courses[course_id]
                classroom = Classes.Classroom.classrooms[classroom_idx]
                print(
                    f"Day: {day}, Time Slot: {start_time}-{Data.end_times[timeslot_idx]}, Lecture Hall: {classroom.room_number}, Course: {course_name.title.ljust(40)}, Instructor: {course_name.instructor.name}")
            print("-" * 80)

    plt.plot(best_fitnesses)
    plt.title('Best Fitness Value Evolution')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness Value')
    plt.show()



# Create GUI for inputting PSO parameters
def run_PSO_from_gui():
    try:
        Pop_size = int(entry_pop_size.get())
        Max_itr = int(entry_max_itr.get())
        w = float(entry_w.get())
        c1 = float(entry_c1.get())
        c2 = float(entry_c2.get())
        
        PSO(Pop_size, Max_itr, w, c1, c2)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for all parameters.")

root = tk.Tk()
root.title("PSO Parameters")

tk.Label(root, text="Population Size").grid(row=0, column=0, padx=5, pady=5)
entry_pop_size = tk.Entry(root)
entry_pop_size.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Maximum Iterations").grid(row=1, column=0, padx=5, pady=5)
entry_max_itr = tk.Entry(root)
entry_max_itr.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Inertia Weight").grid(row=2, column=0, padx=5, pady=5)
entry_w = tk.Entry(root)
entry_w.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Cognitive Coefficient").grid(row=3, column=0, padx=5, pady=5)
entry_c1 = tk.Entry(root)
entry_c1.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Social Coefficient").grid(row=4, column=0, padx=5, pady=5)
entry_c2 = tk.Entry(root)
entry_c2.grid(row=4, column=1, padx=5, pady=5)

btn_run = tk.Button(root, text="Run PSO", command=run_PSO_from_gui)
btn_run.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
