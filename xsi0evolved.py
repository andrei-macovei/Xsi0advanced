import statistics
import sys
import time
import copy

import pygame

ADANCIME_MAX = 4


def elem_identice(lista):
    if len(set(lista)) == 1:
        castigator = lista[0]
        if castigator != Joc.GOL:
            return castigator
    return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 0
    NR_LINII = 0
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None, matrice_vecini_jmin=None, matrice_vecini_jmax=None):  # Joc()
        if tabla is not None:
            self.matr = tabla
            self.matrice_vecini_jmin = matrice_vecini_jmin
            self.matrice_vecini_jmax = matrice_vecini_jmax
        else:
            matrice = []
            for i in range(self.NR_LINII):
                linie = []
                for j in range(self.NR_COLOANE):
                    linie.append(Joc.GOL)
                matrice.append(linie)
            self.matr = matrice

            matrice_vecini_jmin = []
            for i in range(self.NR_LINII):
                linie = []
                for j in range(self.NR_COLOANE):
                    linie.append(0)
                matrice_vecini_jmin.append(linie)
            self.matrice_vecini_jmin = matrice_vecini_jmin

            matrice_vecini_jmax = []
        for i in range(self.NR_LINII):
            linie = []
            for j in range(self.NR_COLOANE):
                linie.append(0)
            matrice_vecini_jmax.append(linie)
        self.matrice_vecini_jmax = matrice_vecini_jmax

    @classmethod
    def jucator_opus(cls, jucator):
        if jucator == cls.JMIN:
            return cls.JMAX
        else:
            return cls.JMIN

    def castigator(self):
        stare_finala = True
        for i in range(self.NR_LINII):
            if self.GOL in self.matr[i]:
                stare_finala = False
                break
        if stare_finala:
            nr_x = 0
            nr_0 = 0
            for i in range(0, self.NR_LINII):
                for j in range(0, self.NR_COLOANE):
                    if self.matr[i][j] == 'x':
                        nr_x += 1
                    elif self.matr[i][j] == '0':
                        nr_0 += 1
            if nr_0 > nr_x:
                return '0'
            else:
                return 'x'
        return 'necastigator'

    # def verifica_vecini_recursiv(self, matr, linie, coloana):
    #     jucator = matr[linie][coloana]
    #
    #     for i in range(linie - 1, linie + 2):
    #         for j in range(coloana - 1, coloana + 2):
    #             if i == linie and j == coloana:
    #                 continue
    #             if matr[i][j] == jucator:
    #                 pass

    # def verifica_vecini(self, jucator):
    #     matrice_nr_vecini = []
    #     for i in range(0, self.NR_LINII):
    #         linie = []
    #         for j in range(0, self.NR_COLOANE):
    #             linie.append(0)
    #         matrice_nr_vecini.append(linie)
    #
    #     for i in range(0, self.NR_LINII):
    #         for j in range(0, self.NR_COLOANE):
    #             if self.matr[i][j] == jucator:
    #                 for y in range(max(0, i - 1), min(self.NR_LINII, i + 2)):
    #                     for z in range(max(0, j - 1), min(self.NR_COLOANE, j + 2)):
    #                         if y == i and z == j:
    #                             continue
    #                         if self.matr[y][z] == jucator:
    #                             matrice_nr_vecini[y][z] += 1

    # return matrice_nr_vecini

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []

        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] == Joc.GOL:
                    copie_matrice = copy.deepcopy(self.matr)
                    if jucator == Joc.JMIN:
                        copie_vecini = copy.deepcopy(self.matrice_vecini_jmin)
                        copie_vecini_opus = copy.deepcopy(self.matrice_vecini_jmax)
                    elif jucator == Joc.JMAX:
                        copie_vecini = copy.deepcopy(self.matrice_vecini_jmax)
                        copie_vecini_opus = copy.deepcopy(self.matrice_vecini_jmin)
                    copie_matrice[i][j] = jucator

                    matrice, vecini, vecini_opus = \
                        refresh_joc(i, j, jucator, copie_matrice, copie_vecini, copie_vecini_opus)
                    if jucator == Joc.JMIN:
                        l_mutari.append(Joc(matrice, vecini, vecini_opus))
                    elif jucator == Joc.JMAX:
                        l_mutari.append(Joc(matrice, vecini_opus, vecini))

        return l_mutari

    def estimeaza_scor(self, adancime):
        t_final = self.castigator()
        # if (adancime==0):
        if t_final == self.JMAX:  # self.__class__ referinta catre clasa instantei
            return 99 + adancime
        elif t_final == self.JMIN:
            return -99 - adancime
        else:
            # return self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN)
            scor = 0
            for i in range(0, self.NR_LINII):
                for j in range(0, self.NR_COLOANE):
                    scor += self.matrice_vecini_jmax[i][j]
                    scor -= self.matrice_vecini_jmin[i][j]
            return scor

    def __str__(self):
        sir = "  |"
        for i in range(self.NR_COLOANE):
            sir += str(i) + " "
        sir += "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_LINII):
            sir += str(i) + " |"
            for j in range(self.NR_COLOANE):
                sir += self.matr[i][j] + ' '
            sir += '\n'
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        juc_opus = Joc.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucator curent:" + self.j_curent + ")\n"
        return sir


# def verifica_vecini(matr, jucator):
#     matrice_nr_vecini = []
#     for i in range(0, Joc.NR_LINII):
#         linie = []
#         for j in range(0, Joc.NR_COLOANE):
#             linie.append(0)
#         matrice_nr_vecini.append(linie)
#
#     for i in range(0, Joc.NR_LINII):
#         for j in range(0, Joc.NR_COLOANE):
#             if matr[i][j] == jucator:
#                 for y in range(max(0, i - 1), min(Joc.NR_LINII, i + 2)):
#                     for z in range(max(0, j - 1), min(Joc.NR_COLOANE, j + 2)):
#                         if y == i and z == j:
#                             continue
#                         if matr[y][z] == jucator or matr[y][z] == Joc.GOL:
#                             matrice_nr_vecini[y][z] += 1
#
#         return matrice_nr_vecini


""" Algoritmul MinMax """


def min_max(stare):
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime == 0 or stare.tabla_joc.castigator() != 'necastigator':
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x) for x in
                        stare.mutari_posibile]  # expandez(constr subarb) fiecare nod x din mutari posibile

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.castigator() != 'necastigator':
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.castigator()
    if final != 'necastigator':
        print("A castigat jucatorul " + final)
        return True
    return False


def deseneaza_grid(display, tabla):
    w_gr = h_gr = 50

    x_img = pygame.image.load('ics.png')
    x_img = pygame.transform.scale(x_img, (w_gr, h_gr))
    zero_img = pygame.image.load('zero.png')
    zero_img = pygame.transform.scale(zero_img, (w_gr, h_gr))
    patratele = []
    for linie in range(len(tabla)):
        l_patratele = []
        for coloana in range(len(tabla[linie])):
            patratel = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
            l_patratele.append(patratel)
            pygame.draw.rect(display, (255, 255, 255), patratel)
            if tabla[linie][coloana] == 'x':
                display.blit(x_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            elif tabla[linie][coloana] == '0':
                display.blit(zero_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
        patratele.append(l_patratele)
    pygame.display.flip()
    return patratele


def refresh_joc(linie, coloana, jucator, matrice, matrice_vecini, matrice_vecini_oponent):
    for i in range(max(0, linie - 1), min(Joc.NR_LINII, linie + 2)):
        for j in range(max(0, coloana - 1), min(Joc.NR_COLOANE, coloana + 2)):
            if i == linie and j == coloana:
                matrice_vecini[i][j] = 4
                matrice_vecini_oponent[i][j] = 0
            if matrice[i][j] == jucator or matrice[i][j] == Joc.GOL:  # refresh matrice vecini
                if matrice_vecini[i][j] < 4:
                    matrice_vecini[i][j] += 1

    for i in range(max(0, linie - 1), min(Joc.NR_LINII, linie + 2)):
        for j in range(max(0, coloana - 1), min(Joc.NR_COLOANE, coloana + 2)):
            if matrice_vecini[i][j] == 4 and matrice[i][j] == Joc.GOL:
                matrice[i][j] = jucator  # refresh matrice joc
                matrice_vecini_oponent[i][j] = 0  # refresh matrice vecini oponent
                matrice, matrice_vecini, matrice_vecini_oponent = \
                    refresh_joc(i, j, jucator, matrice, matrice_vecini, matrice_vecini_oponent)

    return matrice, matrice_vecini, matrice_vecini_oponent


def main():
    t_initial = int(round(time.time() * 1000))

    nr_linii = 8
    nr_coloane = 8
    adancime = 2

    Joc.NR_LINII = nr_linii
    Joc.NR_COLOANE = nr_coloane
    Joc.JMIN = 'x'
    Joc.JMAX = '0'

    # initializare tabla
    tabla_curenta = Joc()  # apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', adancime)

    # setari interfata grafica
    pygame.init()
    pygame.display.set_caption("x si 0 evolved")
    ecran = pygame.display.set_mode(
        size=(Joc.NR_COLOANE * 50 + Joc.NR_COLOANE - 1, Joc.NR_LINII * 50 + Joc.NR_LINII - 1))

    patratele = deseneaza_grid(ecran, tabla_curenta.matr)

    mutari_jmin = 0
    mutari_jmax = 0
    br = False
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # muta jucatorul
            brr = False
            if br:
                break
            # print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    t_inainte = int(round(time.time() * 1000))
                    pos = pygame.mouse.get_pos()
                    for i in range(len(patratele)):
                        if br or brr:
                            break
                        for j in range(len(patratele[i])):
                            if patratele[i][j].collidepoint(pos):
                                if stare_curenta.tabla_joc.matr[i][j] == Joc.GOL:
                                    stare_curenta.tabla_joc.matr[i][j] = Joc.JMIN  # adaugare in matrice

                                    stare_curenta.tabla_joc.matr, stare_curenta.tabla_joc.matrice_vecini_jmin, stare_curenta.tabla_joc.matrice_vecini_jmax = refresh_joc(i, j, Joc.JMIN, stare_curenta.tabla_joc.matr, stare_curenta.tabla_joc.matrice_vecini_jmin, stare_curenta.tabla_joc.matrice_vecini_jmax)

                                    print("\nTabla dupa mutarea jucatorului")
                                    # for linie in nr_vecini_jmin:
                                    #     print(linie)
                                    print(str(stare_curenta.tabla_joc))
                                    patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)
                                    mutari_jmin += 1
                                    # testez daca jocul a ajuns intr-o stare finala
                                    # si afisez un mesaj corespunzator in caz ca da
                                    if afis_daca_final(stare_curenta):
                                        br = True
                                        break

                                    # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                    brr = True
                                    break
        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            mutari_jmax += 1

            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

    t_final = int(round(time.time() * 1000))
    print("Timpul total de executie este de " + str(t_final - t_initial) + " ms")


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
