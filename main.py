import sys
from academic_manager.core import AcademicManager


def main():
    """
    The main entry point of the application.

    Modes:
      python main.py - Interactive CLI mode.
      python main.py --web - Start the FastAPI web server.

    :raises KeyboardInterrupt: When the user manually interrupts the CLI with Ctrl+C.
    """
    if "--web" in sys.argv:
        import uvicorn
        print("🌐 Iniciando Academic Manager no modo Web...")
        print("   Acesse: http://localhost:8000")
        print("   Docs:   http://localhost:8000/docs")
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
        return

    try:
        AcademicManager().run()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")


if __name__ == "__main__":
    main()
