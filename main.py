import random

#wprowadzanie przedmitow przez uzytkownika
def load_items_from_user():
    items = []
    print("Wprowadzaj przedmioty. Wpisz 'stop' jako nazwę, aby zakończyć.\n")

    while True:
        name = input("Nazwa przedmiotu: ")
        if name.lower() == "stop":
            break

        try:
            weight = float(input("Waga: "))
            value = float(input("Wartość: "))
        except ValueError:
            print("Błąd: waga i wartość muszą być liczbami.\n")
            continue

        items.append({
            "name": name,
            "weight": weight,
            "value": value
        })

    return items


#funckja fitness dla wszystkich chromosomow
def fitness(chromosome, items, capacity):
    total_weight = 0
    total_value = 0

    for gene, item in zip(chromosome, items):
        if gene == 1:
            total_weight += item["weight"]
            total_value += item["value"]

    if total_weight > capacity:
        return 0

    return total_value


#populacja startowa
def random_chromosome(gene_count):
    return [random.randint(0, 1) for _ in range(gene_count)]

def create_initial_population(size, gene_count):
    return [random_chromosome(gene_count) for _ in range(size)]

#ruletka
def roulette_selection(population, items, capacity):
    fitness_values = [fitness(ch, items, capacity) for ch in population]
    total_fitness = sum(fitness_values)

    if total_fitness == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fitness)
    current = 0

    for chromosome, fit in zip(population, fitness_values):
        current += fit
        if current >= pick:
            return chromosome

    return population[-1]

#krzyzowanie
def crossover(parent1, parent2):
    if len(parent1) < 2:
        return parent1[:], parent2[:]

    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

#mutacja
def mutate(chromosome, mutation_rate):
    new_ch = []
    for gene in chromosome:
        if random.random() < mutation_rate:
            new_ch.append(1 - gene)
        else:
            new_ch.append(gene)
    return new_ch


#algorytm genetyczny
def genetic_algorithm(items, capacity, population_size=50, generations=200,
                      crossover_rate=0.8, mutation_rate=0.02, #tu jest 0.02, bo nie dzialalo sensownie z mutation_rate 0.2 (mozna zmienic na 0.2, jesli bylaby taka potrzeba)
                      print_every=1):
    gene_count = len(items)
    population = create_initial_population(population_size, gene_count)

    best_solution = None
    best_fitness = -1

    for gen in range(generations):
        population_best = 0
        new_population = []

        while len(new_population) < population_size:

            parent1 = roulette_selection(population, items, capacity)
            parent2 = roulette_selection(population, items, capacity)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
        for chrom in population:
            fit = fitness(chrom, items, capacity)
            if fit > best_fitness:
                best_fitness = fit
                best_solution = chrom

            if fit>population_best:
                population_best = fit

        if gen % print_every == 0:
            print(f"Pokolenie numer: {gen} - Najlepszy fitness tego pokolenia: {population_best} - Najlepszy fitness ogólny: {best_fitness}")

    return best_solution, best_fitness


#start programu
if __name__ == "__main__":
    items = load_items_from_user()

    if not items:
        print("Błąd: nie podano żadnych przedmiotów.")
        exit()

    try:
        capacity = float(input("\nPodaj pojemność plecaka: "))
    except ValueError:
        print("Błąd: pojemność musi być liczbą.")
        exit()

    try:
        how_many_generations = int(input("\nPodaj liczbę generacji (domyślnie 200): ") or 200)
    except ValueError:
        how_many_generations = 200

    try:
        print_how = int(input("Co ile generacji program ma pokazywać wynik (domyślnie co każdą generację): ") or 1)
    except ValueError:
        print_how = 1

    best_chrom, best_fit = genetic_algorithm(items, capacity, generations=how_many_generations, print_every=print_how)

    print("\nWYNIK:")
    print("Najlepszy chromosom: ", best_chrom)
    print("Najlepszy fitness:", best_fit)
    print("Wybrane przedmioty:")
    total_weight = 0
    for gene, item in zip(best_chrom, items):
        if gene == 1:
            print(f" - {item['name']} (waga {item['weight']}, wartość {item['value']})")
            total_weight += item["weight"]
    print("Łączna waga:", total_weight)
