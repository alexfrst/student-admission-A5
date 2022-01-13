# Projet : student admission

**Groupe :** 

- FORESTIER Alexandre
- SENEJKO Morgane

**Sujet :**

L'objectif du projet est de comparer deux solveurs d'optimisation sur le thème d'admissions d'étudiants.

Les jeux de données générés sont constitués de notes d'étudiants sur différentes matières. Selon ces notes, et à l'aide des coefficients pour chaque matière ainsi qu'un seuil d'admissibilité, les étudiants appartiennent à une certaine classe (par exemple: Admis ou Refusé dans le cas ce 2 classes).

La première partie du projet est l'implémentation du Inv-MR-Sort à l'aide d'un solveur d'optimisation (Gurobi).
La deuxième partie est l'implémentation du Inv-NCS à l'aide d'un solveur SAT (Gophersat).


**Structure des fichiers :**

Pour la première partie : le notebook final se nomme part1_gurobi_k_criteres.ipynb.

**Modules à importer :**

- gurobipy
- numpy
