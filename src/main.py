from src.organizador import organizar_anotacao

def main():
    print("ORGANIZADOR DE ANOTAÇÕES")

    anotacao = input("\nDigite sua anotação:\n")

    try:
        resultado = organizar_anotacao(anotacao)

        print("\nANOTAÇÃO ORGANIZADA:")
        print(resultado)

    except ValueError as erro:
        print(f"\nErro: {erro}")

    except RuntimeError as erro:
        print(f"\nErro: {erro}")

    except Exception:
        print("\nErro inesperado durante a execução.")

if __name__ == "__main__":
    main()
