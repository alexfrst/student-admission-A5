import subprocess
from itertools import combinations, chain

from generate_dataset import convert_dataset, generate_dataset


class MaxSatSolver():
    def _build_variables(self, subjects_count, classes_count):
        """
        Construit toutes les variables utilisées pour résoudre le problème.
        @param subjects_count: {int} Nombre de matières dans le problème.
        @param classes_count: {int} Nombre de classes dans le problème.
        @return: {(np.array[],Dict(tuple:int),Dict(tuple:int);Dict(int:tuple),List())} Variables related objects.
        """

        # Variables binaires x(i, h, k) = True ssi la note k sur le critère i est au-dessus de la frontière h
        x = []
        for mark in range(0, 21):
            for subject in range(subjects_count):
                for student_class in range(classes_count):
                    x.append((subject, student_class, mark))

        # Ensemble des critères
        I = list(range(subjects_count))
        # Variables binaires yB = True ssi la la coalition de matières de B est suffisante
        yB = []
        for n in range(subjects_count + 1):
            yB.append([i for i in combinations(I, n)])
        yB = list(chain.from_iterable(yB))

        # Traduction des variables en dictionnaires pour le solveur SAT
        x2i = {v: i + 1 for i, v in enumerate(x)}  # numérotation qui commence à 1
        y2i = {v: i + len(x2i) + 1 for i, v in enumerate(yB)}  # numérotation qui commence à taille de x2i + 1
        variables = x + yB

        # Traduction inverse
        i2variables = {i + 1: v for i, v in enumerate(variables)}
        return x, x2i, y2i, yB, i2variables, variables

    # Clause 1 : x(i,h,k') ∨ ¬x(i,h,k) (avec k<k')
    def _generate_clause1(self, classes_count, subjects_count, x2i):
        """
        Génère les clauses associées à l'ascendance des échelles.
        @param classes_count: {int} Nombre de classes dans le problème.
        @param subjects_count: {int} Nombre de matières dans le problème.
        @param x2i: {Dict(Tuple,int)} Mapping d'une variable à son numéro.
        @return: {List()} Clauses générées.
        """
        clauses_ascending_scales = []
        # On parcourt les matières i
        for i in range(subjects_count):
            # On parcourt les frontières de classe h
            for h in range(classes_count):
                # On parcourt les différentes notes possibles (jusqu'à 19 pour pouvoir réaliser k+1)
                for k in range(0, 20):
                    # On parcourt les notes supérieures à k
                    for k_sup in range(k + 1, 21):
                        clauses_ascending_scales.append([x2i[(i, h, k_sup)], -x2i[(i, h, k)]])

        return clauses_ascending_scales

    # Clause 2 : x(i,h,k) ∨ ¬x(i,h',k) (avec 0<=h<h'<p-1)
    def _generate_clause2(self, classes_count, subjects_count, x2i):
        """
        Génère les clauses associées à la hiérarchie des profils.
        @param classes_count: {int} Nombre de classes dans le problème.
        @param subjects_count: {int} Nombre de matières dans le problème.
        @param x2i: {Dict(Tuple,int)} Mapping d'une variable à son numéro.
        @return: {List()} Clauses générées.
        """
        clauses_hierarchy_profiles = []
        # On parcourt les matières i
        for i in range(subjects_count):
            # On parcourt les frontières de classe h (jusqu'à h-1 pour pouvoir réaliser h+1)
            for h in range(classes_count - 1):
                # On parcourt les frontières de classe supérieures à h
                for h_sup in range(h + 1, classes_count):
                    # On parcourt toutes les notes de 0 à 20
                    for k in range(0, 21):
                        clauses_hierarchy_profiles.append([x2i[(i, h, k)], -x2i[(i, h_sup, k)]])

        return clauses_hierarchy_profiles

    def _generate_clause3(self, yB, y2i):
        """
        Génère les clauses associées à la force des coallitions.
        @param yB: {List()} Liste des coalitions.
        @param y2i: {Dict(List,Int)} Mapping des coallition à leur numéro.
        @return: {List()} Clauses générées.
        """
        clauses_coalition_strength = []

        # On parcourt les différentes coalitions
        for index, coalition in enumerate(yB):
            variable_1 = y2i[coalition]
            # On parcourt les coalitions plus petites
            coalitions_inf = []
            for i in range(index):
                # si elle est inclue dans notre coalition
                if set(yB[i]).issubset(coalition):
                    coalitions_inf.append(yB[i])

            for coalition_inf in coalitions_inf:
                variable_2 = y2i[coalition_inf]

                if ([variable_1, -variable_2] not in clauses_coalition_strength):
                    clauses_coalition_strength.append([variable_1, -variable_2])

        return clauses_coalition_strength

    # Clause 4 : Vi∈B(¬x(i,h,ui)) ∨ ¬yB
    def _generate_clause4(self, classes_count, X, yB, y2i, x2i):
        """
        Génère les clauses qui assurent l'unicité d'une classe par rapport aux classes supérieures.
        @param classes_count: {int} Nombre de classes dans le problème.
        @param X: {np.array()[]} Matrice des notes des élèves.
        @param yB: {List()} Matrice des notes des élèves.
        @param y2i: {Dict(Tuple,Int)} Mapping d'une coalition à son index.
        @param x2i: {Dict(Tuple,Int)} Mapping d'une variable à son index.
        @return: {List()} Clauses générées.
        """
        clauses4 = []

        # On parcourt les coalitions
        for coalition in yB:
            variable_1 = y2i[coalition]

            # On parcourt les classes
            for h in range(1, classes_count):

                # On parcourt les étudiants qui appartiennent à cette classe
                for student in X[h - 1]:
                    variables_list = [-variable_1]

                    # On parcourt les matières
                    for i in coalition:
                        variable_2 = x2i[(i, h, student[i])]
                        variables_list.append(-variable_2)

                    clauses4.append(variables_list)

        return clauses4

    # Clause 5 : Vi∈B(x(i,h,ai)) ∨ yN\B
    def _generate_clause5(self, classes_count, X, yB, y2i, x2i, subjects_count):
        """
        Génère les clauses qui assurent l'unicité d'une classe par rapport aux classes inférieures.
        @param classes_count: {int} Nombre de classes dans le problème.
        @param X: {np.array()[]} Matrice des notes des élèves.
        @param yB: {List()} Liste des coalitions.
        @param y2i: {Dict(Tuple,Int)} Mapping d'une coalition à son index.
        @param x2i: {Dict(Tuple,Int)} Mapping d'une variable à son index.
        @param subjects_count: {int} Nombre de matières dans le problème.
        @return: {List()} Clauses générées.
        """
        clauses5 = []

        # On parcourt les coalitions
        for coalition in yB:

            # Le complémentaire de cette coalition :
            coalition_comp = [elem for elem in yB if
                              set(elem).isdisjoint(coalition) and set((*elem, *coalition)).issuperset(
                                  set(range(subjects_count)))][0]

            variable_1 = y2i[coalition_comp]

            # On parcourt les classes
            for h in range(1, classes_count):

                # On parcourt les étudiants qui appartiennent à cette classe
                for student in X[h]:

                    variables_list = [variable_1]

                    # On parcourt les matières
                    for i in coalition:
                        variable_2 = x2i[(i, h, student[i])]

                        variables_list.append(variable_2)

                    clauses5.append(variables_list)

        return clauses5

    def _clauses_to_dimacs(self, clauses, numvar):
        """
        Converti les clauses générées précédemment dans le format dimacs.
        @param clauses: {List(clauses_struct,clauses_dataset)} Clauses générées précedemment.
        @param numvar: {Int} Nombre de variables.
        @return: {str}
        """
        clauses_struct, clauses_dataset = clauses

        dimacs = 'c This is it\np wcnf ' + str(numvar) + ' ' + str(len(clauses_struct) + len(clauses_dataset)) + '\n'
        for clause in clauses_struct:
            dimacs += str(100) + ' '
            for atom in clause:
                dimacs += str(atom) + ' '
            dimacs += '0\n'

        for clause in clauses_dataset:
            dimacs += str(1) + ' '
            for atom in clause:
                dimacs += str(atom) + ' '
            dimacs += '0\n'

        return dimacs

    def _write_dimacs_file(self, dimacs, filename):
        """
        Ecrit les clauses en format dimacs dans un fichier.
        @param dimacs: {str} Clauses encodées dans le format dimacs.
        @param filename: {str} Nom du fichier.
        @return: None
        """
        with open(filename, "w", newline="") as cnf:
            cnf.write(dimacs)

    # Attention à utiliser la vesion du solveur compatible avec votre système d'exploitation, mettre le solveur dans le même dossier que ce notebook

    def _solve(self, clauses, variables, i2variables, filename, cmd="./gophersat/gophersat-1.1.6.exe"):
        """
        Résoud le problème formalisé avec les clauses précédentes .
        @param clauses: {List(clauses_struct,clauses_dataset)} Clauses générées précedemment.
        @param variables: {List()} Liste des variables du problème.
        @param i2variables: {Dict(Int, Tuple)} Mapping d'un numéro à la variable correspondante.
        @param filename: {str} Nom du fichier wcnf.
        @param cmd:{str} Chemin vers l'executable gophersat.
        @return: {bool,int,List(Int),Dict(Tuble, bool)}
        """

        myDimacs = self._clauses_to_dimacs(clauses, len(variables))

        self._write_dimacs_file(myDimacs, "workingfile.wcnf")

        result = subprocess.run([cmd, filename], stdout=subprocess.PIPE, check=True, encoding="utf8", timeout=10)
        string = str(result.stdout)
        lines = string.splitlines()

        if lines[2] != "s OPTIMUM FOUND":
            return False, "o ", [], {}

        model = lines[3][3:].replace("x", "").split(" ")

        return True, lines[1], [int(x) for x in model[:-1] if int(x) != 0], {i2variables[abs(int(v))]: int(v) > 0 for v
                                                                             in model
                                                                             if v != ""}

    def solve(self, S, y):
        """
        Résoud le dataset donné en paramètre.
        @param S: {np.array[]} Matrice des notes des etudiants.
        @param y: {np.array} Classification des étudiants.
        @return: {bool,int,List(Int),Dict(Tuble, bool)}
        """
        classes_count = len(set(y))
        subjects_count = S.shape[1]
        x, x2i, y2i, yB, i2variables, variables = self._build_variables(subjects_count, classes_count)
        X = convert_dataset(S, y, classes_count)

        classes_count = len(X)
        params1 = {"subjects_count": subjects_count, "x2i": x2i, "classes_count": classes_count}
        params2 = {"yB": yB, "y2i": y2i}
        params3 = {"X": X, "yB": yB, "y2i": y2i, "x2i": x2i, "classes_count": classes_count}
        clauses_struct = self._generate_clause1(**params1) + self._generate_clause2(**params1) + self._generate_clause3(
            **params2)
        clauses_dataset = self._generate_clause4(**params3) + self._generate_clause5(
            **{"subjects_count": subjects_count, **params3})

        return self._solve([clauses_struct, clauses_dataset], variables, i2variables, "workingfile.wcnf")


if __name__ == "__main__":
    students_count = 20
    subjects_count = 5  # les différentes matières (critères)
    classes_count = 3  # Si classe = 2 : Accepté ou refusé par exemple

    S, y = generate_dataset(students_count, subjects_count, classes_count, verbose=1)

    print(S)

    solver = MaxSatSolver()
    print(solver.solve(S, y))
