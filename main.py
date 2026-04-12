import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from frontend.login_window import LoginWindow

if __name__ == "__main__":
    app = LoginWindow()
    app.run()