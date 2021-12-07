import server
import bottle
import App

#ssh -i edenmac.pem ec2-user@ec2-3-145-10-169.us-east-2.compute.amazonaws.com

bottle.run(host="localhost", port = 8080, debug = True, reloader = True)