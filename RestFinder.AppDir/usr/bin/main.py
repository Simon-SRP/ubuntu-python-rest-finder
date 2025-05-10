# #!/usr/bin/env python3
# from app.gui import RestFinderApp
# import sys
#
# if __name__ == "__main__":
#     app = RestFinderApp(sys.argv)
#     app.run()

#!/usr/bin/env python3
import sys
from app.gui import RestFinderApp

if __name__ == "__main__":
    app = RestFinderApp(sys.argv)
    sys.exit(app.run())