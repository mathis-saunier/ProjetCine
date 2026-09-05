import os
import sys

REPERTOIRE_SRC = os.path.dirname(os.path.abspath(__file__))
if REPERTOIRE_SRC not in sys.path:
    sys.path.insert(0, REPERTOIRE_SRC)


def main() -> None:
    """
    Point d'entrée de l'application web.

    Lance Uvicorn sur toutes les interfaces, port 8000.
    """
    import uvicorn

    uvicorn.run(
        "webPackage.applicationWeb:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
