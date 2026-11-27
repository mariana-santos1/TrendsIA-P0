from src.organizer import organize_note

def main():
    print("ORGANIZADOR DE ANOTAÇÕES")

    note = input("\nDigite sua anotação:\n")

    try:
        result = organize_note(note)

        print("\nANOTAÇÃO ORGANIZADA:")
        print(result)

    except ValueError as error:
        print(f"\nErro: {error}")

    except RuntimeError as error:
        print(f"\nErro: {error}")

    except Exception:
        print("\nErro inesperado durante a execução.")

if __name__ == "__main__":
    main()
