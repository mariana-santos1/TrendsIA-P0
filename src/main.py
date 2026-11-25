from src.organizador import organizar_anotacao

def main():
    print("ORGANIZADOR DE ANOTAÇÕES")

    anotacao = input("\nDigite sua anotação:\n")

    if not anotacao:
        print("\nErro: a anotação não pode estar vazia!")
        return

    resultado = organizar_anotacao(anotacao)

    print("\nANOTAÇÃO ORGANIZADA:")
    print(resultado)

if __name__ == "__main__":
    main()
