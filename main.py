import random

#wprowadzanie przedmitow przez uzytkownika
def load_items_from_user():
    items = []
    print("Wpisz 'stop' jako nazwę, aby zakończyć dodwanie przedmiotów. Wpisz 'generuj' jako nazwę przedmiotu, aby automatycznie stworzyć przedmioty.\n")

    while True:
        name = input("Nazwa przedmiotu: ")
        if name.lower() == "stop":
            break
        if name.lower() == "generuj":
            dolna_waga = int(input("Najmniejsza waga dla przedmiotu: "))
            górna_waga = int(input("Największa waga dla przedmiotu: "))
            dolna_wartość = int(input("Najmniejsza wartość dla przedmiotu: "))
            górna_wartość = int(input("Największa wartość dla przedmiotu: "))
            ile_przedmiotów = int(input("Ile przedmiotów wygenerować: "))

            for i in range(1, ile_przedmiotów + 1):
                items.append({
                    "name": f"Przedmiot_ID_{i}",
                    "weight": int(random.uniform(dolna_waga, górna_waga)),
                    "value": int(random.uniform(dolna_wartość, górna_wartość))
                })

            print(f"\nWygenerowano {ile_przedmiotów} przedmiotów!\n")
            continue

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
                      crossover_rate=0.8, mutation_rate=0.2,
                      print_every=1):
    gene_count = len(items)
    population = create_initial_population(population_size, gene_count)

    best_solution = None
    best_fitness = -1
    bet_generation_number = 0

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
                best_generation_number = gen
            if fit>population_best:
                population_best = fit

        if gen % print_every == 0:
            print(f"Pokolenie numer: {gen} - Najlepszy fitness tego pokolenia: {population_best}. Najlepsze pokolenie ogólnie: {best_generation_number} - Najlepszy fitness ogólny: {best_fitness}")
    return best_solution, best_fitness, best_generation_number


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

    best_chrom, best_fit, best_gen = genetic_algorithm(items, capacity, generations=how_many_generations, print_every=print_how)

    print("\nWYNIK:")
    print("Najlepszy chromosom: ", best_chrom)
    print("Najlepsze pokolenie: ", best_gen)
    print("Najlepszy fitness:", best_fit)
    print("Wybrane przedmioty:")
    total_weight = 0
    for gene, item in zip(best_chrom, items):
        if gene == 1:
            print(f" - {item['name']} (waga {item['weight']}, wartość {item['value']})")
            total_weight += item["weight"]
    print("Łączna waga:", total_weight)
    if total_weight > capacity:
        print("Uwaga! Nie znaleziono chromosomu spełniajacego wymagania plecaka.")

input("\nNaciśnij Enter, aby zakończyć.")
