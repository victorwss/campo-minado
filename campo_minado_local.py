from campo_minado_model import CampoMinado, JaAbriu

def jogar():
    c: CampoMinado
    while True:
        try:
            largura: int = int(input(f"Largura: "))
            altura: int = int(input(f"Altura: "))
            bombas: int = int(input(f"Bombas: "))
            c = CampoMinado.novo(largura, altura, bombas)
            break;
        except Exception as z:
            print('Entrada inválida. Tente novamente.')

    while not c.acabou:
        print(c)

        print(f"Há {c.desconhecidos} espaços desconhecidos. Você deve abrir os {c.faltam} em branco e evitar as {c.bombas} bombas.")

        x: int
        y: int
        try:
            x = int(input(f"X [0 - {c.largura - 1}]: "))
            y = int(input(f"Y [0 - {c.altura - 1}]: "))
        except Exception as z:
            print('Entrada inválida.')
        else:
            try:
                c = c.abrir_local(x, y)
            except ValueError as z:
                print('Entrada inválida.')
            except JaAbriu as z:
                print('Você já tinha aberto essa posição antes.')

    if c.ganhou:
        print('Parabéns!')
    else:
        print('BUUUUM!')

    print(c)

jogar()