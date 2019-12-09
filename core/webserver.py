import time
import api.analyze
from flask import Flask
def webserver():
    app = Flask(__name__)
    @app.route('/map')
    def nima():
        a = api.analyze.analyze_suricata("files/suricata/eve.json",data="xy",language="en")
        while(a == []):
            time.sleep(1)
        astr = str(a)
        return astr
    app.run()
