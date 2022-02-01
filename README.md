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
│   maxsat_solver_evaluation.ipynb
│   part1_gurobi_2_criteres.ipynb
│   part2_maxsat_k_classes.py
│   part2_sat_k_classes.py
│   README.md
│   sat_solver_evaluation.ipynb
└───gophersat
       gophersat-1.1.6.exe
```

**`./gophersat/gophersat-1.1.6.exe` is where the gophersat solver is located**

`generate_dataset.py` Contient des fonctions de génération et de manipulation des datasets.

`part1_gurobi_2_criteres.ipynb` Résolution et évaluation des performance d'un modèle MR-Sort. Vous pouvez exécuter le notebook entier, la dernière partie est assez longue car elle calcule les performances du modèle sur divers datasets.

`part2_sat_k_classes.py` Résolution d'un`problème avec modèle NCS.

`sat_solver_evaluation.ipynb` Evaluation du modèle NCS avec solveur SAT.

`part2_maxsat_k_classes.py` Résolution d'un problème avec modèle NCS à l'aide d'un solveur MaxSat.

`maxsat_solver_evaluation.ipynb` Evaluation du modèle NCS avec solveur MaxSat.

`/graphs` Stockage statique des graphes.


## Modules utilisés

- gurobipy
- numpy
- plotly (Dataviz)
- kaleido (Export statique des graphes)
- sklearn (Calcul des matrices de confusion)
- numpy

# Résultats MR-Sort 

| Parameter      | Duration                                 | Performance                          |
|----------------|------------------------------------------|--------------------------------------|
| Students count | ![](graphs/gurobi_duration_students.png) | ![](graphs/gurobi_perf_students.png) |
| Subjects count | ![](graphs/gurobi_duration_subjects.png) | ![](graphs/gurobi_perf_subjects.png) |



# Résultats NCS

| Parameter      | Duration                              | Performance                       |
|----------------|---------------------------------------|-----------------------------------|
| Students count | ![](graphs/sat_duration_students.png) | ![](graphs/sat_perf_students.png) |
| Subjects count | ![](graphs/sat_duration_subjects.png) | ![](graphs/sat_perf_subjects.png) |

# Sensibilité au bruit des modèles NCS et MR-SORT

| Solveur MR-Sort                   | Solveur SAT                       |
|-----------------------------------|-----------------------------------|
| ![](graphs/gurobi_perf_noise.png) | ![](graphs/sat_perf_noise.png)    |


# Modèle NCS avec solveur MaxSat

| Nombre de variables ignorée          | Performance                       |
|--------------------------------------|-----------------------------------|
| ![](graphs/maxsat_ignored_noise.png) | ![](graphs/maxsat_perf_noise.png) |