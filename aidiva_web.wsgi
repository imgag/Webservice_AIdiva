python_home = "/var/www/html/AIdiva/venv"

activate_this = python_home + "/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


import sys
sys.path.insert(0, "/var/www/html/AIdiva/Webservice_AIdiva/")

from app import create_app


application = create_app()
