import random

def generate_instance(filename_prefix, n, set_size, min_coef, max_coef, use_int_coef):
  subsets = []
  universe = set(range(1, n + 1))
  covered_elements = set()

  filename = "in/" + filename_prefix + f"_{n}.txt"

  for _ in range(n):
    current_set = set(random.sample(range(1, n + 1), random.randint(1, n // 2) if set_size == 0 else set_size))
    subsets.append(current_set)
    covered_elements.update(current_set)

  if len(covered_elements) < n:
    missing_elements = list(universe - covered_elements)
    print(f"Atenção: Nem todos os elementos do universo foram cobertos. Adicionando {len(missing_elements)} elementos faltantes.")
    for element in missing_elements:
      random_subset_index = random.randint(0, n - 1)
      subsets[random_subset_index].add(element)

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
  generate_instance("teste", n, 0, -10, 10, False)