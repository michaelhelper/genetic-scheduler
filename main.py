#simple schedule fitness test run
#imports
from itertools import permutations
from operator import index
import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import pandas as pd
import time

#timer for fun
t0 = time.time()

#create teachers with classes and students with classes
bob_classes = ['debate', 'ak_studies', 'ak_studies', 'steller_101', 'hs_eng', 'conf']
allison_classes = ['world_lit', 'adv_Comp', 'health', 'ms_eng', 'world _lit', 'conf']
ashley_classes = ['us_lit', 'steller_101', 'int_comp', 'ms_eng', 'hs_eng', 'conf']
leighanne_classes = ['hs_ss_elective', 'seminar', 'seminar', 'gov/econ', 'gov/econ', 'conf']
joe_classes = ['world history', 'world_history', 'us_history', 'ms_ss', 'us_history', 'conf']
jason_classes = ['algebra_2', 'ms_ss', 'ms_ss', 'calc', 'algebra_2', 'conf']
sarah_classes = ['math_8', 'algebra_1', 'math_8', 'ms_sci', 'ms_sci', 'conf']
marla_classes = ['math_7', 'stats', 'geometry', 'math' , 'geometry', 'conf']
mike_classes = ['ms_sci', 'ms_sci', 'ms_sci', 'chem', 'chem', 'conf']
philip_classes = ['biology', 'biology', 'biology', 'art', 'art', 'conf']
brian_classes = ['physics', 'algebra_1', 'algebra_1', 'astronomy', 'computer_science', 'conf']
rosa_classes = ['spanish_3', 'spanish_2', 'spanish_2', 'spanish_1', 'spanish_1', 'conf']
troy_classes = ['pe', 'pe', 'pe', 'pe', 'pe', 'conf']
teachers_ = [bob_classes, allison_classes, ashley_classes, leighanne_classes, joe_classes, jason_classes, sarah_classes, marla_classes, mike_classes, philip_classes, brian_classes, rosa_classes, troy_classes]
teachers_strings = ['bob_classes', 'allison_classes', 'ashley_classes', 'leighanne_classes', 'joe_classes', 'jason_classes', 'sarah_classes', 'marla_classes', 'mike_classes', 'philip_classes', 'brian_classes', 'rosa_classes', 'troy_classes']

grade_7_1 = ['steller_101', 'ms_ss', 'math_7', 'ms_sci', 'pe', 'band/orchestra']
grade_7_2 = ['steller_101', 'ms_ss', 'math_7', 'ms_sci', 'pe', 'art']
grade_7_3 = ['steller_101', 'ms_ss', 'math_7', 'ms_sci', 'pe', 'spanish_1']
grade_8_1 = ['seminar', 'seminar', 'ms_sci', 'math_8', 'pe', 'art']
grade_8_2 = ['seminar', 'seminar', 'ms_sci', 'math_8', 'pe', 'band/orchestra']
grade_8_3 = ['seminar', 'seminar', 'ms_sci', 'math_8', 'pe', 'spanish_1']
grade_8_4 = ['seminar', 'seminar', 'ms_sci', 'math_8', 'pe', 'spanish_2']
grade_8_5 = ['health', 'ms_ss', 'ms_eng', 'ms_sci', 'math_8', 'art']
grade_8_6 = ['health', 'ms_ss', 'ms_eng', 'ms_sci', 'math_8', 'band/orchestra']
grade_8_7 = ['health', 'ms_ss', 'ms_eng', 'ms_sci', 'math_8', 'spanish_1']
grade_8_8 = ['health', 'ms_ss', 'ms_eng', 'ms_sci', 'math_8', 'spanish_2']
grade_9_1 = []
grade_9_2 = []
grade_9_3 = []
grade_9_4 = []
grade_9_5 = []
grade_9_6 = []
grade_9_7 = []

students_ = [grade_7_1, grade_7_2, grade_7_3, grade_8_1, grade_8_2, grade_8_3, grade_8_4, grade_8_5, grade_8_6, grade_8_7, grade_8_8]
student_strings = ['grade_7_1', 'grade_7_2', 'grade_7_3', 'grade_8_1', 'grade_8_2', 'grade_8_3', 'grade_8_4', 'grade_8_5', 'grade_8_6', 'grade_8_7', 'grade_8_8']

#! Beware changing these values will sacrifice the overall schedule optimization in favor of optimizing for a few students and may produce worse overall results. 
student_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 

#create all permutations of student schedules
def create_all_permutations(students):
    new_students = []
    for student in students:
        student_list = []
        student_list = list(permutations(student))
        new_students.append(student_list)
        new_students = copy.deepcopy(new_students)
    return new_students

#creates initial population of n schedules by shuffling the schedule of each teacher n times
def initial_population(teachers_list, population_size):
    schedule_list_population = {}
    for i in range(0, population_size):
        shuffled_teachers = []
        schedule_list_population[i] = [teacher for teacher in teachers_list]
        schedule_list_population = copy.deepcopy(schedule_list_population)
        for teacher in schedule_list_population[i]:
            np.random.shuffle(teacher)
            shuffled_teachers.append(teacher)
        schedule_list_population[i] = shuffled_teachers
    return schedule_list_population

#loop through all possible student schedules and check to see which one is the best return its' score
def current_offspring_fitness(students_list, teachers_lists, fitness_weights):
    all_fitnesses = []
    all_weighted_fitnesses = []
    all_top_students = {}
    for x in range(len(teachers_lists)):
        current_teacher_list = teachers_lists[x]
        total_list_fitness = 0
        total_list_weighted_fitness = 0
        list_of_top_students = []
        counter = len(students_list)
        for students in students_list:
            counter -= 1
            top_fitness = 0
            top_student_schedule = []
            for student in students:
                fitness = 0
                for i in range(len(student)):
                    for teacher in current_teacher_list:
                        if teacher[i] == student[i]:
                            fitness += 1
                            break
                if fitness > top_fitness:
                    top_fitness = fitness * fitness_weights[counter]
                    top_student_schedule = student
            list_of_top_students.append(top_student_schedule)
            total_list_weighted_fitness += top_fitness
            total_list_fitness += 10 ** top_fitness
        all_top_students[x] = list_of_top_students
        all_weighted_fitnesses.append(total_list_weighted_fitness)
        all_fitnesses.append(total_list_fitness)
    return all_fitnesses, all_top_students, all_weighted_fitnesses
def crossover (offspring, offspring_fitness):
    # adds all offspring es and divides each offspring individual fitness by total of all 
    # offspring fitnesses to get "percent of fitness" for each offspring
    new_offspring_dict = {}
    fitness_by_percent = []
    fitness_sum = sum(offspring_fitness)
    x = 0
    for i in range(len(offspring_fitness)):
        x += offspring_fitness[i] / fitness_sum
        fitness_by_percent.append(x)
    iterations = len(offspring_fitness)
    #roulette to determine which offspring shout become parents uses offspring fitness and generates number between 0  and 1
    while iterations >= 0:
        random_num_1 = random.random()
        random_num_2 = random.random()
        parent_1 = None
        parent_2 = None
        counter = 0
        for a in range(len(fitness_by_percent)):
            if random_num_1 < fitness_by_percent[a]:
                parent_1 = offspring[counter]
                continue
            counter += 1
        counter = 0
        for a in range(len(fitness_by_percent)):
            if random_num_2 < fitness_by_percent[a]:
                parent_2 = offspring[counter]
                continue
            counter += 1
        new_offspring = []
        for i in range(len(parent_1)):
            number = random.choice([1, 2])
            if number == 1:
                first_parent = parent_1[i]
                second_parent = parent_2[i]
            else:
                first_parent = parent_2[i]
                second_parent = parent_1[i]
            rand_length = random.randint(1, len(first_parent))
            randIndex = random.sample(range(len(first_parent)), rand_length)
            randIndex.sort()
            new_teacher_offspring = [first_parent[i] for i in randIndex]
            indices_list = []
            count = 0 
            temp_range = len(first_parent)
            for a in range(0,temp_range):
                indices_list.append(count)
                count += 1
            for a in randIndex:
                for x in indices_list:
                    if a == x:
                        indices_list.remove(x)
            second_parent_copy = second_parent.copy()
            for a in range(len(randIndex)):
                remove_class = second_parent[a]
                second_parent_copy.remove(remove_class)
            count = 0
            new_new_teacher_offspring = []
            for x in range(len(first_parent)):
                new_new_teacher_offspring.append(x)
            for a in range(len(new_new_teacher_offspring)):
                for x in randIndex:
                    if x == a:
                        new_new_teacher_offspring[a] = new_teacher_offspring[0]
                        to_remove = new_teacher_offspring[0]
                        new_teacher_offspring.remove(to_remove)
                for x in indices_list:
                    if x ==  a:
                        new_new_teacher_offspring[a] = second_parent_copy[0]
                        to_remove = second_parent_copy[0]
                        second_parent_copy.remove(to_remove)
            new_offspring.append(new_new_teacher_offspring)
        new_offspring_dict[iterations] = new_offspring
        iterations -= 1
    return new_offspring_dict

def hall_of_fame(offspring, offspring_fitness, top_students):
    top_offspring = []
    top_fitness = 0
    index = 0
    for i in range(len(offspring_fitness)):
        if offspring_fitness[i] > top_fitness:
            top_fitness = offspring_fitness[i]
            top_offspring = offspring[i]
            students_classes = top_students[i]
            index = i
    return top_offspring, students_classes, index

def mutation(offspring, mutation_chance, n):
    new_offspring_dict = {}
    count = n
    while count > 0:
        new_offspring = []
        schedule = offspring[count]
        for i in range(len(schedule)):
            current_teacher = schedule[i]
            current_teacher_copy = []
            random_number = random.random()
            if mutation_chance > random_number:
                indicy_1 = random.randrange(0,6)
                indicy_2 = random.randrange(0,6)
                current_teacher_copy = current_teacher.copy()
                current_teacher_copy[indicy_1] = current_teacher[indicy_2]
                current_teacher_copy[indicy_2] = current_teacher[indicy_1]
            else:
                current_teacher_copy = current_teacher.copy()
            new_offspring.append(current_teacher_copy)
        new_offspring_dict[count] = new_offspring
        new_offspring_dict = copy.deepcopy(new_offspring_dict)
        count -= 1
    new_offspring_dict_ = copy.deepcopy(new_offspring_dict)
    return new_offspring_dict_

def absolute_fitness(top_dog, students_list, fitnesses, index):
    total_list_fitness = 0
    for students in students_list:
        top_fitness = 0
        for student in students:
            fitness = 0
            for i in range(len(student)):
                for teacher in top_dog:
                    if teacher[i] == student[i]:
                        fitness += 1
                        break
            if fitness > top_fitness:
                top_fitness = fitness
        total_list_fitness += top_fitness
        weighted_fitness = fitnesses[index]
    return total_list_fitness, weighted_fitness

#big daddy function
def genetic_algorithm_function(generations, students, teachers, mutation_chance, number_of_offspring, print_results, graph_results, fitness_weights):
    x_points = []
    y_points = []
    all_students = create_all_permutations(students)
    current_offspring = initial_population(teachers, number_of_offspring)
    weights = False
    max_abs_fitness = 0
    for weight in fitness_weights:
        if weight != 1:
            weights = True
    for student in students:
        for i in student:
            max_abs_fitness += 1
    counter = generations
    while counter > 0:
        fitness, top_students_dict, weighted_fitnesses = current_offspring_fitness(all_students, current_offspring, fitness_weights)
        top_doggie, top_doggie_students, index = hall_of_fame(current_offspring, fitness, top_students_dict)
        new_population = crossover(current_offspring, fitness)
        new_mutated_population = mutation(new_population, mutation_chance, number_of_offspring)
        current_offspring = new_mutated_population
        current_offspring = copy.deepcopy(current_offspring)
        current_offspring[0] = top_doggie
        current_offspring[1] = top_doggie
        current_offspring = copy.deepcopy(current_offspring)
        top_doggie_fitness, top_doggie_fitness_weighted = absolute_fitness(top_doggie, all_students, weighted_fitnesses, index)
        counter -= 1
        gen = generations - counter
        if print_results == True:
            cool = 1
            print('Gen #', gen, 'Absolute Fitness:', top_doggie_fitness, '/', max_abs_fitness, end="")
            if weights == True:
                print('|', 'Weighted Fitness:', round(top_doggie_fitness_weighted, 1)) 
            print(' Top Doggie:', top_doggie)
        if graph_results == True:
            x_points.append(gen)
            y_points.append(top_doggie_fitness)
        if max_abs_fitness == top_doggie_fitness:
            break
    indexes = []
    students_ = {}
    for x in range(len(teachers_[0])):
        name = student_strings[x]
        students_[name] = top_doggie_students[x]
        current_period = 'Period: ' + str(x+1)
        indexes.append(current_period)
    data = {}
    for i in range(len(top_doggie)):
        name = teachers_strings[i]
        schedule = top_doggie[i]
        data[name] = schedule
    df = pd.DataFrame(data, index=indexes)
    df.to_excel(r'C:\Users\micha\Documents\teachers_data.xlsx', index=True, header=True)
    df = pd.DataFrame(students_, index=indexes)
    df.to_excel(r'C:\Users\micha\Documents\students_data.xlsx', index=True, header=True)
    if weights == True:
        print('|', 'weighted Fitness', round(top_doggie_fitness_weighted, 1))
    if print_results == True:
        print(' Teacher Schedules', top_doggie, '\n', 'Students Schedules:',  top_doggie_students)
        print('Best Individual, Absolute Fitness:', top_doggie_fitness, '/', max_abs_fitness, end="")
    t1 = time.time()
    total_time = t1-t0
    print(generations-counter, 'Generations and', total_time, 'seconds needed')
    if graph_results == True:
        x = np.array(x_points)
        y = np.array(y_points)
        plt.plot(x, y)
        plt.xlabel("Number of Generations")
        plt.ylabel("Absolute Fitness")
        plt.show()


#call the genetic algorithm with #of generations, list of students, list of teachers, chance of mutation 0-1(can be a decimal),
# #of offspring per generation, should it print the top individual from every gen?
genetic_algorithm_function(20, students_, teachers_, 0.4, 20, False, True, student_weights)

# TODO TO-DO LIST BELOW

# TODO easier tasks
# TODO write some code comments about export to excell

# TODO harder tasks
# TODO change crossover function to try index first the we can add from append list  **set values to null
# TODO start on creating HTML Form shell to take students, teachers information and display terminal output. 
# TODO add support for part time students and teachers


#* Patch Notes Below:

#* Added the ability to assign students importance using weights. 
#* If you choose to weight students the weighted fitnesses now print to the terminal next to absolute fitnesses


#IGNORE LEFT OVER FROM TESTING BUT I WANT TO KEEP IT INCASE I NEED TO TEST IN THE FUTURE
#-------------------------------------------------------------------------------------------------------------------------------------------------
#run functions
#n_ = 40
#new_students = create_all_permutations(students_)
#current_offspring_ = initial_population(teachers_, n_)
#population_fitness = current_offspring_fitness(new_students, current_offspring_)
#new_population_ = crossover(current_offspring_, population_fitness)
#top_dawg = hall_of_fame(current_offspring_, population_fitness)
#new_population_mutated = mutation(new_population_, 1, n_, top_dawg)
#print(new_population_mutated)