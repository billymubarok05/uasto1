import random
import numpy as np

# ===================== DATA =====================
cityNames = [
    "Jogja",
    "Sunan Gunung Jati (Cirebon)",
    "Sunan Kudus",
    "Sunan Giri (Gresik)",
    "Sunan Kalijaga (Demak)",
    "Sunan Gresik",
    "Sunan Ampel (Surabaya)",
    "Sunan Drajat (Lamongan)",
    "Sunan Bonang (Tuban)",
    "Sunan Muria (Kudus)"
]

distance = np.array([
    [0,360,185,335,160,340,334,362,163,204],
    [360,0,293,579,269,601,583,610,370,318],
    [185,293,0,405,261,408,409,202,80.6,21.4],
    [335,579,405,0,313,4,24,56.5,164,241],
    [160,269,261,313,0,383,382,225,104,45.8],
    [340,601,408,4,383,0,22.5,56.5,164,244],
    [334,583,409,24,382,22.5,0,75.9,181,336],
    [362,610,202,56.5,225,56.5,75.9,0,120,200],
    [163,370,80.6,164,104,164,181,120,0,80.9],
    [204,318,21.4,241,45.8,244,336,200,80.9,0]
])

# ===================== PARAMETER ACO =====================
Q = 100
rho = 0.05
antSize = 17
tmax = 35

alpha = 1
beta = 2

n = len(cityNames)
pheromone = np.ones((n, n))
best_route = None
best_distance = float("inf")

# ===================== ACO PROCESS =====================
for iteration in range(tmax):
    all_routes = []
    all_distances = []

    for ant in range(antSize):
        visited = [0]  # start from Jogja
        current = 0

        while len(visited) < n:
            probabilities = []
            for city in range(n):
                if city not in visited:
                    prob = (pheromone[current][city] ** alpha) * ((1 / distance[current][city]) ** beta)
                else:
                    prob = 0
                probabilities.append(prob)

            probabilities = np.array(probabilities)
            probabilities = probabilities / probabilities.sum()
            next_city = np.random.choice(range(n), p=probabilities)

            visited.append(next_city)
            current = next_city

        visited.append(0)  # return to Jogja
        total_distance = sum(distance[visited[i]][visited[i+1]] for i in range(len(visited)-1))

        all_routes.append(visited)
        all_distances.append(total_distance)

        if total_distance < best_distance:
            best_distance = total_distance
            best_route = visited

    # ===================== UPDATE FEROMON =====================
    pheromone *= (1 - rho)

    for route, dist in zip(all_routes, all_distances):
        for i in range(len(route)-1):
            pheromone[route[i]][route[i+1]] += Q / dist

    print(f"Iterasi {iteration+1} | Jarak terbaik: {best_distance:.2f} km")

# ===================== OUTPUT =====================
print("\nRUTE TERPENDEK ZIARAH WALI SONGO")
for city in best_route:
    print(cityNames[city])

print(f"\nTotal jarak: {best_distance:.2f} km")