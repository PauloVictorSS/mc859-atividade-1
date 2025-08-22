import random

def generate_instance(filename_prefix, n, set_size, min_coef, max_coef, use_int_coef):
  """
  Gera uma instância de tamanho n, com subconjuntos de tamanho set_size, matriz com
  coeficientes variando entre min_coef e max_coef. Se use_int_coef for False, usa
  coeficientes reais, se True, usa coeficientes inteiros. Se set_size for igual a 0,
  gera subconjuntos de tamanho variando entre 1 e n / 2. Salva instância em 
  in/filename_prefix_n.txt.
  """
  subsets = [set() for _ in range(n)]
  universe = set(range(1, n + 1))
  filename = "in/" + filename_prefix + f"_{n}.txt"

  # Garante que cada elemento do universo pertença a um subconjunto
  for element in universe:
    while True:
      idx = random.randint(0, n - 1)
      if element not in subsets[idx] and (set_size == 0 or len(subsets[idx]) < set_size):
        subsets[idx].add(element)
        break

  # Garante que cada subconjunto obedeça ao tamanho exigido (ou sorteado)
  for subset in subsets:
    random_size = random.randint(1, n // 2)
    while len(subset) < set_size or (set_size == 0 and len(subset) < random_size):
      random_element = random.randint(1, n)
      if random_element not in subset:
        subset.add(random_element)

  # Geração de coeficientes
  coefficients = {}
  for i in range(1, n + 1):
    for j in range(i, n + 1):
      coefficients[(i, j)] = random.randint(min_coef, max_coef) if use_int_coef else random.uniform(min_coef, max_coef)

  # Criação de arquivo de entrada
  with open(filename, 'w') as f:
    f.write(f"{n}\n")
    
    sizes = [str(len(s)) for s in subsets]
    f.write(" ".join(sizes) + "\n")

    for s in subsets:
      f.write(" ".join(map(str, sorted(list(s)))) + "\n")

    for i in range(1, n + 1):
      row_str = " ".join([str(coefficients[(i, j)]) for j in range(i, n + 1)])
      f.write(row_str + "\n")
      
  print(f"Instância gerada com sucesso: {filename}")

# Gerando todas as instâncias
for n in [25, 50, 100, 200, 400]:
  generate_instance("size_3_range10_intcoeff", n, 3, -10, 10, True)
  generate_instance("size_n_over_2_range1000_intcoeff", n, n // 2, -1000, 1000, True)
  generate_instance("size_random_range10_floatcoeff", n, 0, -10, 10, False)