# Projet : student admission

**Groupe :** 

- FORESTIER Alexandre
- SENEJKO Morgane

# Sujet :

L'objectif du projet est de comparer deux solveurs d'optimisation sur le thème d'admissions d'étudiants.

Les jeux de données générés sont constitués de notes d'étudiants sur différentes matières. Selon ces notes, et à l'aide des coefficients pour chaque matière ainsi qu'un seuil d'admissibilité, les étudiants appartiennent à une certaine classe (par exemple: Admis ou Refusé dans le cas ce 2 classes).

La première partie du projet est l'implémentation du Inv-MR-Sort à l'aide d'un solveur d'optimisation (Gurobi).
La deuxième partie est l'implémentation du Inv-NCS à l'aide d'un solveur SAT (Gophersat).


# Structure du projet :

## Structure des fichiers

Ce répertoire GIT suit la structure suivante:

```dir
│   generate_dataset.py
│   part1_gurobi_2_criteres.ipynb
│   part2_sat.ipynb
│   README.md
│
├───gophersat
│       gophersat-1.1.6.exe
│
└───graphs
        gurobi_duration_students.png
        gurobi_duration_subjects.png
        gurobi_perf_students.png
        gurobi_perf_subjects.png
```

**`./gophersat/gophersat-1.1.6.exe` is where the gophersat solver is located**

`generate_dataset.py` Contient des fonctions de génération et de manipulation des datasets.

`part1_gurobi_2_criteres.ipynb` Résolution et évaluation des performance d'un modèle MR-Sort. Vous pouvez exécuter le notebook entier, la dernière partie est assez longue car elle calcule les performances du modèle sur divers datasets.

`part2_sat.ipynb` Résolution d'un modèle NCS. Vous pouvez exécuter le notebook entier.

`/graphs` Stockage statique des graphes.


## Modules utilisés

- gurobipy
- numpy
- plotly (Dataviz)
- kaleido (Export statique des graphes)

# Résultats MR-Sort 

| Parameter      | Duration                                 | Performance                          |
|----------------|------------------------------------------|--------------------------------------|
| Students count | ![](graphs/gurobi_duration_students.png) | ![](graphs/gurobi_perf_students.png) |
| Subjects count | ![](graphs/gurobi_duration_subjects.png) | ![](graphs/gurobi_perf_subjects.png) |



# Résultats Solveur-Sat

| Parameter      | Duration                              | Performance                       |
|----------------|---------------------------------------|-----------------------------------|
| Students count | ![](graphs/sat_duration_students.png) | ![](graphs/sat_perf_students.png) |
| Subjects count | ![](graphs/sat_duration_subjects.png) | ![](graphs/sat_perf_subjects.png) |

# Sensibilité au bruit

| Solveur MR-Sort                   | Solveur SAT                       |
|-----------------------------------|-----------------------------------|
| ![](graphs/gurobi_perf_noise.png) | ![](graphs/sat_perf_noise.png)    |


# Solveur Maxat

| Nombre de variables ignorée          | Performance                       |
|--------------------------------------|-----------------------------------|
| ![](graphs/maxsat_ignored_noise.png) | ![](graphs/maxsat_perf_noise.png) |