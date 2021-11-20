import server
import bottle
import App

#ssh -i edenmac.pem ubuntu@ec2-3-144-135-150.us-east-2.compute.amazonaws.com

bottle.run(host="localhost", port = 8080, debug = True)
