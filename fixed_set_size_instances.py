import random

def generate_instance(filename_prefix, n, set_size, min_coef, max_coef, use_int_coef):
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


  # covered_elements = set()

  # for _ in range(n):
  #   current_set = set(random.sample(range(1, n + 1), random.randint(1, n // 2) if set_size == 0 else set_size))
  #   subsets.append(current_set)
  #   covered_elements.update(current_set)
  # 
  # if len(covered_elements) < n:
  #   missing_elements = list(universe - covered_elements)
  #   print(f"Atenção: Nem todos os elementos do universo foram cobertos. Adicionando {len(missing_elements)} elementos faltantes.")
  #   for element in missing_elements:
  #     random_subset_index = random.randint(0, n - 1)
  #     subsets[random_subset_index].add(element)

  coefficients = {}
  for i in range(1, n + 1):
    for j in range(i, n + 1):
      coefficients[(i, j)] = random.randint(min_coef, max_coef) if use_int_coef else random.uniform(min_coef, max_coef)

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


for n in [25, 50, 100, 200, 400]:
  generate_instance("teste", n, 0, -10, 10, True)