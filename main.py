import server
import bottle
import App

#ssh -i edenmac.pem ec2-user@ec2-3-145-10-169.us-east-2.compute.amazonaws.com
#ssh -i edenmac.pem ec2-user@ec2-18-220-134-19.us-east-2.compute.amazonaws.com

bottle.run(host="0.0.0.0", port = 8080, debug = True, reloader = True)