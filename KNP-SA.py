import json
import random
import time

#code = '1_100_1000_1'
#code = '1_200_1000_1'
code = '1_500_1000_1'
#code = '1_1000_1000_1'
#code = '1_2000_1000_1'
#code = '1_5000_1000_1'

# Ler dados de entrada
def read_weights_and_costs(file_name='instances/knapPI_' + code):
    count = 1
    weights = {}
    costs = {}
    
    file = open(file_name, "r")
    data = file.readlines()
    
    number_of_things = int(data[0].split()[0])
    capacity = int(data[0].split()[1])
    

    for i in range(1, number_of_things + 1):
        
        costs[count] = int(data[i].split()[0])
        weights[count] = int(data[i].split()[1])
        count = count + 1

    return weights, costs, number_of_things, capacity

# Criar solução inicial
def create_solution(weights, costs, number_of_things, capacity):
    
    total_weight = 0
    total_cost = 0
    
    rc = number_of_things
    solution = []
    list_of_things = list(range(1, rc+1))
    
    # inserir elementos na mochila enquanto ela suportar
    while(total_weight <= capacity):
        # Criar uma solução inicial com pelo menos 1 item
        if total_weight == 0:
            control = True
            while control:
                # Escolha de item aleatório
                random_thing_index = random.randint(0, rc-1)
                random_item = list_of_things[random_thing_index]
                
                if weights[random_item] <=  capacity:
                    control = False
        else:  
            random_thing_index = random.randint(0, rc-1)
            random_item = list_of_things[random_thing_index]
        
        # Inserir item na mochila, e remover da lista de itens fora da mochila
        solution.append(random_item)
        list_of_things.remove(random_item)
        # Atualizar o peso e o custo atual
        total_weight = total_weight + weights[random_item]
        total_cost = total_cost + costs[random_item]
        
        rc = rc - 1
    
    # O último item inserido na mochila(dentro do loop) faz seu peso ultrapassar a capacidade
    # Por isso é preciso remove-lo
    if total_weight > capacity:
        solution.remove(random_item)

        total_weight = total_weight - weights[random_item]
        total_cost = total_cost - costs[random_item]
        
    return solution, total_weight, total_cost
 
# Criar solução candidata
def create_new_solution(initial_solution, num_of_things, weights, costs, total_weight, total_cost):
    t_weight = total_weight
    t_cost = total_cost
    rc = number_of_things
 
    list_of_things = list(range(1, rc+1))  
    # Remover todos os itens da solução inicial, da lista de itens fora da mochila
    for item in initial_solution:
        list_of_things.remove(item)
        rc = rc - 1

    new_solution = list(initial_solution)

    # Remover um item da mochila e atualiza o custo e o peso
    random_thing_index = random.randint(0, len(initial_solution)-1)
    random_item = initial_solution[random_thing_index]
    new_solution.remove(random_item)
    t_weight = t_weight - weights[random_item]
    t_cost = t_cost - costs[random_item]

    # inserir elementos na mochila enquanto ela suportar
    while(t_weight <= capacity):
        random_thing_index = random.randint(0, rc-1)
        random_item = list_of_things[random_thing_index]

        new_solution.append(random_item)
        list_of_things.remove(random_item)
        t_weight = t_weight + weights[random_item]
        t_cost = t_cost + costs[random_item]

        rc = rc - 1

    # O último item inserido na mochila(dentro do loop) faz seu peso ultrapassar a capacidade
    # Por isso é preciso remove-lo
    if t_weight > capacity:
        new_solution.remove(random_item)
        t_weight = t_weight - weights[random_item]
        t_cost = t_cost - costs[random_item]
        
    return new_solution, t_weight, t_cost
    

# SA
def SimulatedAnnealing(initial_solution, num_of_things, weights, costs, initial_weight, initial_cost, temperature):

    k = 0 # iteração sem mudança na solução
    LIST_OF_SOLUTIONS = []
    best_solution = None
    best_solution_cost = None
    
    # Itera enquanto a solução não melhorar em k iterações
    while k < number_iterations_solution_is_not_improved:
        # Conjunto de soluções vizinhas locais a serem exploradas
        for l in range(iterations_each_temperature):
            
            # Gera solução candidata
            candidate_solution, candidate_weight, candidate_cost = create_new_solution(initial_solution, num_of_things, weights, costs, initial_weight, initial_cost)


            delta_C = initial_cost - candidate_cost
            
            # Compara se a solução candidata é melhor do que a solução inicial
            if delta_C < 0:
                initial_solution = candidate_solution
                initial_cost = candidate_cost
                initial_weight = candidate_weight
            # Se não for ainda existe possibilidade de aceitação da solução conforme a variação da temperatura
            else:
                variable_control = random.random()
                
                expo = (-1 * delta_C)/temperature
                # Solução degradada é aceita    
                if variable_control <= pow(EULER, expo):
                    initial_solution = candidate_solution
                    initial_cost = candidate_cost
                    initial_weight = candidate_weight

        #Atualização da temperatura
        temperature = temperature*alpha
        

        print('Best Solution Cost --> ', initial_cost, 'k: ', k, 'T: ', temperature)
        
        # A melhor solução em cada valor de temperatura é guardada
        if best_solution == None:
            best_solution = initial_solution
            best_solution_cost = initial_cost
            best_solution_weight = initial_weight
        else:
            if initial_cost > best_solution_cost:
                best_solution = initial_solution
                best_solution_cost = initial_cost
                best_solution_weight = initial_weight
                k = 0
            else:
                k = k + 1
                
        LIST_OF_SOLUTIONS.append(initial_cost)
        
    record_solutions(solutions=LIST_OF_SOLUTIONS)

    return best_solution, best_solution_weight, best_solution_cost
 
# Gravar soluções em arquivo
def record_solutions(solutions, code=code):
        with open('saidas/SA/' + code  + '_solution.csv', 'a') as file:
            file.write('Solution\n')
            for item in solutions:
                file.write(str(item) + '\n')
                

if __name__ == '__main__':
    
    start = time.time()
    
    EULER = 2.718281828459
    temperature = 1000
    alpha = 0.98
    iterations_each_temperature = 500
    number_iterations_solution_is_not_improved = 100

    weights, costs, number_of_things, capacity = read_weights_and_costs()
    
    
    
    initial_solution, initial_weight, initial_cost = create_solution(weights, costs, number_of_things, capacity)
    
    print('FIRST SOLUTION', initial_solution, initial_weight, initial_cost, capacity)
    
    
    final_solution, final_weight, final_cost = SimulatedAnnealing(initial_solution, number_of_things, weights, costs, 
                                        initial_weight, initial_cost, temperature)
    
    print(final_solution)
    final = time.time()
    
    print('Final Solution: ', final_solution, '\nCost: ', final_cost, '\nWeight', final_weight)
    print('Time: ', final-start)
    
    
            
    
    
    
    
    
    