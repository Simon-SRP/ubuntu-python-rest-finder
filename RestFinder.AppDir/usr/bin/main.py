import sys
from app.gui import RestFinderApp

if __name__ == "__main__":
    app = RestFinderApp(sys.argv)
    sys.exit(app.run())