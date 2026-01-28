import random

class GeneticAlgorithm:
    def __init__(self, parameters, products, budget):
        # Inisialisasi parameter algoritma genetik
        self.numOfChromosome = parameters['numOfChromosome']  # Jumlah populasi dalam satu generasi
        self.numOfDimension = len(products)                   # Panjang kromosom (jumlah jenis produk)
        self.cr = parameters['crossoverRate']                 # Probabilitas persilangan
        self.mr = parameters['mutationRate']                  # Probabilitas mutasi
        self.maxGeneration = parameters['maxGen']             # Batas maksimal iterasi (generasi)
        self.budget = budget                                  # Batas uang yang dimiliki
        self.products = products                              # Daftar nama dan harga produk
        self.prices = [p[1] for p in products]                # Hanya mengambil list harganya saja

    # =========================================================
    # OBJECTIVE FUNCTION (Fungsi Tujuan)
    # Menghitung selisih budget dengan total belanja. 
    # Semakin kecil selisih (mendekati 0), semakin bagus.
    # =========================================================
    def parcelObjective(self, chromosome):
        # Chromosome berisi biner [0, 1, 0...]. 1 berarti beli, 0 tidak.
        total = sum(chromosome[i] * self.prices[i] for i in range(len(chromosome)))
        
        if total <= self.budget:
            # Jika masuk budget, nilai objective adalah sisa uang (ingin diminimalkan)
            return self.budget - total
        else:
            # Jika melebihi budget, diberi pinalti sangat besar agar tidak terpilih
            return 10**9 

    # =========================================================
    # FITNESS FUNCTION
    # Mengubah nilai objective menjadi nilai fitness.
    # GA mencari fitness TERTINGGI. 1/(1+0) = 1 (terbaik).
    # =========================================================
    def calcFitnessValue(self, objectiveValue):
        return 1 / (1 + objectiveValue)

    # =========================================================
    # SELEKSI ROULETTE WHEEL
    # Memilih induk berdasarkan proporsi nilai fitnessnya.
    # Semakin tinggi fitness, semakin besar peluang terpilih.
    # =========================================================
    def selectRoletteWheelChromosome(self, fitnessValues, chromosomes):
        totalFitness = sum(fitnessValues)
        probCumulatives = []
        c = 0
        for f in fitnessValues:
            c += f / totalFitness
            probCumulatives.append(c)

        r = random.uniform(0, 1)
        for i in range(len(probCumulatives)):
            if r <= probCumulatives[i]:
                return chromosomes[i]
        return chromosomes[-1]

    def generatedRandomValues(self):
        # Menentukan indeks kromosom mana saja yang akan melakukan crossover
        return [i for i in range(self.numOfChromosome) if random.uniform(0, 1) < self.cr]

    # =========================
    # MAIN GENETIC ALGORITHM
    # =========================
    def mainGA(self):
        # Langkah 1: Inisialisasi Populasi Awal secara acak
        chromosomes = [
            [random.randint(0, 1) for _ in range(self.numOfDimension)]
            for _ in range(self.numOfChromosome)
        ]

        for gen in range(self.maxGeneration):
            # Langkah 2 & 3: Evaluasi Objective dan Fitness
            objectiveValues = [self.parcelObjective(c) for c in chromosomes]
            fitnessValues = [self.calcFitnessValue(o) for o in objectiveValues]

            # Langkah 4: Seleksi Orang Tua (Selection)
            selectedParents = [
                self.selectRoletteWheelChromosome(fitnessValues, chromosomes)
                for _ in range(self.numOfChromosome)
            ]

            # Langkah 6: Crossover (Persilangan)
            # Menggabungkan gen dari dua induk untuk membuat variasi baru
            offspring = []
            randomIndexValues = self.generatedRandomValues()
            
            # Memastikan minimal ada 2 individu untuk dikawinkan
            if len(randomIndexValues) > 1:
                for i in range(0, len(randomIndexValues)-1, 2):
                    p1 = selectedParents[randomIndexValues[i]]
                    p2 = selectedParents[randomIndexValues[i+1]]

                    # Single point crossover
                    cut = random.randint(1, self.numOfDimension - 1)
                    child = p1[:cut] + p2[cut:]
                    offspring.append(child)

            # Langkah 7: Survival Selection (Elitism)
            # Menggabungkan populasi lama + anak, lalu ambil yang terbaik saja
            allChromosomes = chromosomes + offspring
            scored = []
            for c in allChromosomes:
                o = self.parcelObjective(c)
                f = self.calcFitnessValue(o)
                scored.append([f, c])

            # Sortir berdasarkan fitness tertinggi
            scored.sort(reverse=True, key=lambda x: x[0])
            chromosomes = [scored[i][1] for i in range(self.numOfChromosome)]

            # Langkah 8: Mutasi
            # Mengubah satu gen secara acak untuk menjaga keberagaman genetik
            numOfMutation = round(self.mr * self.numOfChromosome * self.numOfDimension)
            for _ in range(numOfMutation):
                idx = random.randint(0, self.numOfChromosome - 1)
                genIdx = random.randint(0, self.numOfDimension - 1)
                # Flip bit: 0 jadi 1, 1 jadi 0
                chromosomes[idx][genIdx] = 1 - chromosomes[idx][genIdx]

            bestFitness = scored[0][0]
            if (gen + 1) % 10 == 0: # Print setiap 10 generasi agar rapi
                print(f"Generasi {gen+1} | Best Fitness: {bestFitness:.6f}")

        # OUTPUT AKHIR
        bestChromosome = chromosomes[0]
        total = sum(bestChromosome[i] * self.prices[i] for i in range(self.numOfDimension))

        print("\n=== HASIL REKOMENDASI PARCEL (ALFAMART) ===")
        for i in range(self.numOfDimension):
            if bestChromosome[i] == 1:
                print(f"- {self.products[i][0]:<25} : Rp {self.products[i][1]:>6,}")

        print("-" * 45)
        print(f"Total Harga Belanja  : Rp {total:,}")
        print(f"Budget Anda          : Rp {self.budget:,}")
        print(f"Sisa (Kembalian)     : Rp {self.budget - total:,}")

# =========================
# KONFIGURASI DATA
# =========================
parameters = {
    'numOfChromosome': 30,
    'crossoverRate': 0.8,
    'mutationRate': 0.01,
    'maxGen': 100
}

# Budget diatur menjadi 125.000 (sesuai kode awal kamu)
budget = 125000

# Data produk berdasarkan gambar katalog yang diunggah
products = [
    ("Bear Brand Gold 189ml", 9900),
    ("Vidoran Smart Milk 700g", 49400),
    ("Vidoran Smart UHT 115ml", 10900),
    ("So Good Siap Makan", 5500), # Estimasi harga satuan dari promo beli 2 gratis 1
    ("Indomie Nyemek/Aceh", 5900),
    ("Richeese Wafer/Ahhh", 10000),
    ("Herbakof Syrup 100ml", 20000),
    ("So Fresh Minyak Angin", 12500),
    ("Sosoft Detergent 700ml", 16500),
    ("Bagus Fresh Air", 10900),
    ("Bebek Pembersih Kloset", 19900),
    ("Plossa Press & Soothe", 14900),
    ("SpongeBob Buddies Figure", 29900),
    ("Gabby's Dollhouse Ad", 24900),
    ("Apolo Boneka", 29900),
    ("Apolo Majestic Sand", 37900),
    ("Barbie Fashionistas", 49900),
    ("Hot Wheels Car", 59900)
]

ga = GeneticAlgorithm(parameters, products, budget)
ga.mainGA()