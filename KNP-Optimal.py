import json
from docplex.mp.model import Model
import time

#code = '1_100_1000_1'
#code = '1_200_1000_1'
#code = '1_500_1000_1'
#code = '1_1000_1000_1'
#code = '1_2000_1000_1'
code = '1_5000_1000_1'

# Leitura de dados
def read_weights_and_values(file_name='instances/knapPI_' + code):
    count = 1
    weights = {}
    values = {}
    
    file = open(file_name, "r")
    data = file.readlines()
    
    number_of_things = int(data[0].split()[0])
    capacity = int(data[0].split()[1])
    
    print(number_of_things, capacity)
    
    for i in range(1, number_of_things + 1):
        
        values[count] = int(data[i].split()[0])
        weights[count] = int(data[i].split()[1])
        count = count + 1
    
        
    return weights, values, number_of_things, capacity
    
    fp = open(file_name)
    distances = json.load(fp)

    return (distances['cities'], distances['distances'])


if __name__ == '__main__':
    start = time.time()

    weights, values, number_of_things, capacity = read_weights_and_values()
    # Criação do modelo
    mdl = Model(name='KNP', log_output=True)
    mdl.parameters.mip.tolerances.absmipgap = 1
    
    ## Criação de variáveis de decisão 
    key = [i for i in range(1,number_of_things+1)]
    mdl.x = mdl.binary_var_dict(keys=key, name='x')
    
    ## Função  objetivo
    total_cost = mdl.sum(mdl.x[(i)]*values[i] for i in range(1,number_of_things+1))
    mdl.maximize(total_cost)
    
    
    ## Capacidade da mochila
    mdl.add_constraint(mdl.sum(mdl.x[i]*weights[i] for i in range(1,number_of_things+1))<=capacity)
        
    ## Resolver modelo
    mdl.solve()
    final = time.time()
    ## Imprimir solução
    for item in key:
        if mdl.x[item].solution_value > 0:
            print("x{} -> {}".format(item, mdl.x[item].solution_value))
            
    print("FO: {}".format(mdl.solution.get_objective_value()))
    print('Time: ', final-start)    
        
        
        
   
    

    
    
    
    
    
    