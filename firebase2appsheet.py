import os
from datetime import datetime
from multiprocessing import Process
from flask import Flask, request, jsonify
import logging as log

from apiauth import require_apikey

from route_contents import contentsroute

app = Flask(__name__)
app.register_blueprint(contentsroute)

# template that you can copy from
app.register_blueprint(yournewcollectionsroute)

# disable the next line if you don't want to use the built-in demo tables/collections
import initialize as init


@app.route('/oaspec', methods=['GET'])
@require_apikey		
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':

	# comment the next two lines to disable our heartbeat event generator
	# otherwise, we are starting this on a seperate process
	#heartbeat_process = Process(target=heartbeat)
	#heartbeat_process.start()

	# comment out the next line if you don't want this demo creating a single
	# record per firestore collection
	#runfirsttime = init.initialize()

	log.info(f"Some log here") 
	app.run(threaded=True, host='0.0.0.0', port=8080)



