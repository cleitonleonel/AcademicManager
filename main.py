from academic_manager.core import AcademicManager


def main():
    """
    The main entry point of the application.

    This function initializes an `AcademicManager` instance and starts its execution
    flow. It is designed to handle the `KeyboardInterrupt` exception gracefully,
    providing feedback to the user when the application is interrupted manually.

    :raises KeyboardInterrupt: When the user manually interrupts the application
        by pressing a keyboard combination (e.g., Ctrl+C).
    """
    try:
        AcademicManager().run()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")


if __name__ == "__main__":
    main()
