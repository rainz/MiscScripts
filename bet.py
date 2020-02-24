import sys

countries = [
        "Brazil",
        "France",
        "England",
        "Belgium",
        "Croatia",
        "Uruguay",
        "Russia",
        "Sweden"
]
bet_rates = [
        [5, 2],
        [4, 1],
        [9, 2],
        [11, 2],
        [13, 2],
        [12, 1],
        [20, 1],
        [20, 1]
]

validate_sum = 0.0
num_countries = len(countries)
for i in range(0, num_countries):
    r = bet_rates[i]
    p = float(r[0])/r[1]
    validate_sum += 1.0/p
    print "{}: {}".format(countries[i], validate_sum)

