import gurobipy as gp
from gurobipy import GRB

def solve_max_sc_qbf_linearized(instance_file):
  """
  Lê uma instância do MAX-SC-QBF, modela e resolve usando o Gurobi,
  usando a formulação linearizada.
  """
  try:
    # 1. Ler os dados da instância
    with open("in/" + instance_file, 'r') as f:
      lines = f.readlines()

    # n: número de variáveis
    n = int(lines[0].strip())

    # Subconjuntos Si
    subsets = [[] for _ in range(n)]
    for i in range(n):
      elements = list(map(int, lines[i+2].strip().split()))
      subsets[i] = elements

    # Matriz de coeficientes A (triangular superior)
    a = {}
    line_idx = n + 2
    for i in range(n):
      row_coeffs = list(map(int, lines[line_idx + i].strip().split()))
      for j_idx in range(len(row_coeffs)):
        j = i + j_idx
        a[(i, j)] = row_coeffs[j_idx]

    # 2. Criar o modelo Gurobi
    model = gp.Model("MAX-SC-QBF_Linearizado")

    # 3. Adicionar as variáveis de decisão x (para os subconjuntos)
    x = model.addVars(n, vtype=GRB.BINARY, name="x")

    # 4. Adicionar as variáveis de linearização y_ij
    y = model.addVars(n, n, vtype=GRB.BINARY, name="y")

    # 5. Definir a função objetivo linearizada
    obj = gp.LinExpr()
    for i in range(n):
      for j in range(i, n):
        if (i, j) in a:
          obj += a[(i, j)] * y[i, j]
    model.setObjective(obj, GRB.MAXIMIZE)

    # 6. Adicionar restrições de linearização (várias para cada y_ij)
    # As restrições de linearização para y_ij = x_i * x_j são:
    # y_ij <= x_i
    # y_ij <= x_j
    # y_ij >= x_i + x_j - 1
    for i in range(n):
      for j in range(i, n):
        model.addConstr(y[i, j] <= x[i], name=f"lin_yij_le_xi_{i}_{j}")
        model.addConstr(y[i, j] <= x[j], name=f"lin_yij_le_xj_{i}_{j}")
        model.addConstr(y[i, j] >= x[i] + x[j] - 1, name=f"lin_yij_ge_sum_{i}_{j}")

    # 7. Adicionar restrições de cobertura de conjuntos (as mesmas do modelo original)
    for k in range(1, n + 1):
      covering_subsets = []
      for i in range(n):
        if k in subsets[i]:
          covering_subsets.append(i)
    
      if covering_subsets:
        model.addConstr(sum(x[i] for i in covering_subsets) >= 1, name=f"cover_{k}")

    # 8. Configurar parâmetros de otimização
    model.setParam('TimeLimit', 600)

    # 9. Otimizar o modelo
    model.optimize()

    # 10. Coletar e imprimir os resultados
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
      with open("out/" + instance_file, 'w') as f:
        solucao_selecionada = [i for i in range(n) if x[i].X > 0.5]
        f.write(f"Subconjuntos selecionados (indices): {solucao_selecionada}\n")
        f.write(f"Valor da Solucao: {model.ObjVal}\n")
        f.write(f"Gap de Otimalidade: {model.MIPGap * 100:.2f}%\n")
        f.write(f"Tempo de Execucao: {model.Runtime:.2f} segundos\n")
        if model.status == GRB.TIME_LIMIT:
          f.write("Limite de tempo atingido")
    else:
      with open("out/" + instance_file, 'w') as f:
        f.write("Não foi possível encontrar uma solução.")
          
  except gp.GurobiError as e:
    print('Ocorreu um erro no Gurobi: ' + str(e.args[0]))
  except IOError as e:
    print('Ocorreu um erro de I/O ao ler o arquivo: ' + str(e))

# Exemplo de uso
solve_max_sc_qbf_linearized("instance_fixed_set_size_25.txt")
solve_max_sc_qbf_linearized("instance_fixed_set_size_50.txt")
solve_max_sc_qbf_linearized("instance_fixed_set_size_100.txt")
solve_max_sc_qbf_linearized("instance_fixed_set_size_200.txt")
solve_max_sc_qbf_linearized("instance_fixed_set_size_400.txt")