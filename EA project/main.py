import numpy as np
import random
import Classes
import Data

class Timetable:
    def __init__(self, position):
        self.current_position = position
        self.velocity = np.zeros_like(self.current_position)
        self.personal_best_position = self.current_position.copy()
        self.personal_best_fitness = float('inf')

    def update_current_position(self):
        new_position = self.current_position + self.velocity
        new_position = np.clip(new_position, 0, len(Classes.Course.courses)-1)
        new_position = np.floor(new_position)
        self.current_position = new_position
        return new_position

    def update_velocity(self, swarm_best_position):
        r1 = np.random.rand(len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms))
        r2 = np.random.rand(len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms))
        c1 = 1.2
        c2 = 1.2
        w = 0.8
        cognitive_component = c1 * r1 * (self.personal_best_position-self.current_position)
        social_component = c2 * r2 * (swarm_best_position-self.current_position)
        new_velocity = w * self.velocity + cognitive_component + social_component
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

        # Iterate over each timeslot in the timetable
        for timeslot_idx in range(current_position.shape[0]):
            course_count_per_timeslot = {course.code: 0 for course in Classes.Course.courses}
            instructor_count_per_timeslot = {instructor.name: 0 for instructor in Classes.FacultyMember.faculty_members}
            department_count_per_timeslot = {course.department: 0 for course in Classes.Course.courses}
            timeslot +=1
            for classroom_idx in range(current_position.shape[1]):
                course_id = current_position[timeslot_idx, classroom_idx]
                if course_id != -1:  # -1 indicates an empty slot
                    course = Classes.Course.courses[int(course_id)]
                    instructor = course.instructor.name
                    department = course.department

                    # Constraint 1: Check if course is given more than once in a single timeslot
                    if course_count_per_timeslot[course.code] > 0:
                        penalties += 1
                    course_count_per_timeslot[course.code] += 1

                    # Constraint 2: Check if course is given more than once in a week
                    if course_count_per_week[course.code] > 0:
                        penalties += 1
                    course_count_per_week[course.code] += 1

                    if department_count_per_timeslot[department] > 0:
                        penalties += 1
                    department_count_per_timeslot[department] += 1

                    # Constraint 3: Check if instructor is booked more than once in the same timeslot
                    if instructor_count_per_timeslot[instructor] > 0:
                        penalties += 1
                    instructor_count_per_timeslot[instructor] += 1


        return penalties



def PSO(Pop_size, Max_itr):
    swarm_best_position = None
    swarm_best_fitness = float('inf')
    timetables = []

    # Initialize a dictionary to store instructor IDs for each course
    course_ids = {course: idx for idx, course in enumerate(Classes.Course.courses)}
    instructor_ids = {instructor: idx for idx, instructor in enumerate(Classes.FacultyMember.faculty_members)}

    # Position random initialization
    for itr in range(Pop_size):
        random_position = np.zeros((len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms)), dtype=float)

        # Initialize the timetable with course identifiers
        for i in range(len(Classes.Timeslot.timeslots)):
            for j in range(len(Classes.Classroom.classrooms)):
                # Replacing the zeros with the course identifiers
                course = random.choice(Classes.Course.courses)
                course_id = course_ids[course]
                random_position[i, j] = course_id

        random_timetable = Timetable(random_position)
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
        random_velocity = np.zeros((len(Classes.Timeslot.timeslots), len(Classes.Classroom.classrooms)), dtype=float)

        for i in range(len(Classes.Timeslot.timeslots)):
            for j in range(len(Classes.Classroom.classrooms)):
                course = random.choice(Classes.Course.courses)
                course_id = course_ids[course]
                random_velocity[i, j] = course_id

        timetable.velocity = random_velocity


    # Optimization loop
    for itr in range(Max_itr):
        for timetable in timetables:

            # updating particle's velocity:
            timetable.update_velocity(swarm_best_position)
            # updating particle's position:
            position = timetable.update_current_position()
            # Evaluate particle's fitness:
            fitness = timetable.calculate_fitness(position)

            # Update personal best fitness:
            if fitness < timetable.personal_best_fitness:
                timetable.update_personal_best_fitness(fitness)
                timetable.update_personal_best_position(position)

            # Update the swarm best fitness:
            if fitness < swarm_best_fitness:
                swarm_best_fitness = fitness
                swarm_best_position = position


    return swarm_best_position, swarm_best_fitness


Max_iterations = 100
Population_size = 100

swarm_best_position, swarm_best_fitness = PSO(Population_size, Max_iterations)
print(f"Swarm best fitness: {swarm_best_fitness}")
for row in swarm_best_position:
    for cell in row:
        # Extract course and instructor information from the tuple in the cell
        course_id = int(cell)

        # Get course name and instructor name using the IDs
        course_name = Classes.Course.courses[course_id]

        # Print course name and instructor name
        print(f"Course: {course_name.title},           Instructor: {course_name.instructor.name}")

    # Print a separator between rows for better visualization
    print("-" * 50)
print("hey")




