import random

import numpy as np


def check_class(student, w, frontiers_list, lambdou):
    """
    Retourne la classe d'un étudiant
    :param student: {np.array} Notes d'un élève donné
    :param w: {np.array} Coefficients des matières
    :param frontiers_list: {np.array[]} Frontières des notes pour chaque matière
    :param lambdou: {int} Seuil de majorité
    :return: {int} Retourne la classe d'un étudiant (ex: 0 pour refusé, 1 pour accepté)
    """
    # On part de la classe 0 et on incrémente à chaque fois que la somme des coeffs des matières que l'élève valide pour un niveau donné dépasse lambda
    student_class = 0

    # frontiers_list contient une liste de notes frontières pour chaque matières
    # on transforme pour avoir une liste de frontières des matières pour chaque classe
    frontiers_t = frontiers_list.T

    for frontiers in frontiers_t:
        coeffs_sum = ((student >= frontiers) * w).sum()
        if coeffs_sum >= lambdou:
            student_class += 1
        else:
            break

    return student_class


def convert_dataset(S, y, classes_count):
    """
    :param S: {np.array[]} Notes des élèves
    :param y: {list} Classe des élèves
    :param classes_count: {int} Nombre de classes dans le dataset
    :return: {list(np.array()[]} Liste de classes_count matrices de notes
    """
    X = [[] for i in range(classes_count)]

    for i in range(len(y)):
        student_class = y[i]
        X[student_class].append(list(S[i]))

    return [np.array(matrix) for matrix in X]


def generate_dataset(students_count, subjects_count, classes_count, verbose=1):
    """
    Crée un dataset de notes d'étudiant et de leur classe attribuée
    :param students_count: {int} Nombre d'étudiants
    :param subjects_count: {int} Nombre de matières
    :param classes_count:  {int} Nombre de classes (ex: 2 pour {Accepté, Refusé})
    :param verbose: {int} Niveau de débogage (1: debug, 0: pas de debug)
    :return: {list(np.array()[]} Liste de classes_count matrices de notes
    """

    assert students_count > classes_count
    # On génère les coefficients des différentes matières, dont la somme vaut 1
    w_ects = np.random.randint(0, 30, subjects_count)
    w = w_ects / w_ects.sum()
    if verbose != 0:
        print("\nLes coeffs sont = ", w)

    # Les frontières entre chaque classe (si 2 classes A et R, seulement 1 frontière)
    frontiers_list = np.zeros((subjects_count, classes_count - 1))
    for i in range(subjects_count):
        frontiers = np.sort(random.sample(list(range(1, 21)), classes_count - 1))
        frontiers_list[i,] = frontiers

    if verbose != 0:
        print("\nLes frontières sont = ", frontiers_list)

    # La somme des coeffs minimales à avoir pour être dans une classe donnée
    lambdou = random.uniform(0.5, 1)
    if verbose != 0:
        print("\nlambda = ", lambdou)

    y = []
    S = []
    while len(set(y)) != classes_count:
        y = []
        # On génère les notes des élèves (1 ligne par élève)
        S = np.random.randint(0, 21, (students_count, subjects_count))

        # On regarde à quelle classe est associé chaque élève en fonction de ses notes

        for student in S:
            student_class = check_class(student, w, frontiers_list, lambdou)
            y.append(student_class)

    if verbose != 0:
        print("\nLes notes des élèves :")
        print(S)
        print("\nLes classes des élèves :")
        print(y)

    return S, y
