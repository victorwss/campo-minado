from typing import List
import random

class JaAcabou(Exception): pass
class JaAbriu(Exception): pass

class CampoMinado:

    def __init__(self, largura: int, altura: int, bombas: int, tabuleiro: str) -> None:
        self.__tabuleiro: str = tabuleiro
        self.__largura = largura
        self.__altura = altura
        self.__bombas = bombas

    @staticmethod
    def novo(largura: int, altura: int, bombas: int) -> 'CampoMinado':
        if largura <= 0 or altura <= 0 or bombas > largura * altura - 1:
            raise ValueError()
        return CampoMinado(largura, altura, bombas, ("|" + (" " * largura) + "|\n") * altura)

    @property
    def altura(self) -> int:
        return self.__altura

    @property
    def largura(self) -> int:
        return self.__largura

    @property
    def bombas(self) -> int:
        return self.__bombas

    @property
    def explodiu(self) -> int:
        return 'B' in self.__tabuleiro

    @property
    def ganhou(self) -> int:
        return not self.explodiu and self.faltam == 0

    @property
    def desconhecidos(self) -> int:
        r: int = 0
        for z in self.__tabuleiro:
            if z in ' *':
                r += 1
        return r

    @property
    def faltam(self) -> int:
        return self.desconhecidos - self.bombas

    @property
    def acabou(self) -> int:
        return self.ganhou or self.explodiu

    def __check_x_y(self, x: int, y: int) -> None:
        if x < 0 or y < 0 or x >= self.largura or y >= self.altura:
            raise ValueError()

    def __str__(self) -> str:
        r: str = self.__tabuleiro
        if not self.acabou: r = r.replace('*', '.')
        return r.replace(' ', '.').replace('0', ' ')

    def abrir_local(self, x: int, y: int) -> 'CampoMinado':

        def idx(xn: int, yn: int) -> int:
            return yn * (self.largura + 3) + xn + 1

        self.__check_x_y(x, y)
        novo: str = self.__tabuleiro

        def get(xn: int, yn: int) -> str:
            return novo[idx(xn, yn)]

        if self.acabou: raise JaAcabou()
        ot: str = get(x, y)
        if ot in '012345678': raise JaAbriu()

        def set(xn: int, yn: int, v: str) -> None:
            nonlocal novo
            self.__check_x_y(xn, yn)
            if v not in ' B*012345678':
                raise ValueError()
            novo = novo[:idx(xn, yn)] + v + novo[idx(xn, yn) + 1:]

        def contar_bombas_proximas(xn: int, yn: int) -> int:
            b: int = 0
            for j in range(yn - 1, yn + 2):
                if j >= 0 and j < self.altura:
                    for i in range(xn - 1, xn + 2):
                        if i >= 0 and i < self.largura and (i != 0 or j != 0) and get(i, j) in '*B':
                            b += 1
            return b

        def interno(xn: int, yn: int) -> None:
            if xn < 0 or yn < 0 or xn >= self.largura or yn >= self.altura or get(xn, yn) != ' ':
                return
            proximas: int = contar_bombas_proximas(xn, yn)
            set(xn, yn, str(proximas))
            if proximas != 0:
                return

            for j in range(yn - 1, yn + 2):
                for i in range(xn - 1, xn + 2):
                    interno(i, j)

        if ot == '*':
            set(x, y, 'B')
        else:
            if '*' not in self.__tabuleiro:
                for i in range(0, self.bombas):
                    a: int = x
                    b: int = y
                    while (a == x and b == y) or get(a, b) == '*':
                        a = int(random.random() * self.largura)
                        b = int(random.random() * self.altura)
                    set(a, b, '*')
            interno(x, y)
        return CampoMinado(self.largura, self.altura, self.bombas, novo)