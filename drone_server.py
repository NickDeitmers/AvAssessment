from concurrent import futures #Allows you to see number of workers on your server
import time 
import grpc
import drones_pb2
import drones_pb2_grpc 
import random
import logging
import sys

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("drone_server.log")
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

class DroneServicer(drones_pb2_grpc.GreeterServicer):
    
    def register(self, request, context):
        #Unary 
        logger.info("Registration Request received: \n{request}".format(request=request))
        registration_response = drones_pb2.RegistrationResponse(id=request.name)
        return registration_response
    
    def listen_waypoint(self, request, context):
        #Unary
        logger.info("Waypoint Request received: \n{request}".format(request=request))
        lat = float(random.randint(1, 10))
        lon = float(random.randint(1, 10))
        waypoint_response = drones_pb2.WaypointResponse(latitude=lat, longitude=lon)
        return waypoint_response
    
    def send_position(self, request_iterator, context):
        #Server streaming
        logger.debug("Before iterating")
        for request in request_iterator:
            logger.debug("Received request")
            logger.info(request)
            
        position_response = drones_pb2.PositionResponse(status="Arrived at location.")
        return position_response
        
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #Sets the server with a maximum of 10 threads
    drones_pb2_grpc.add_GreeterServicer_to_server(DroneServicer(), server) #Adds the DroneServicer to the server
    server.add_insecure_port("localhost:50051") #Set port 50051 to call on when you connect to the server
    server.start() #Starts the server
    server.wait_for_termination() #Lets server run until you hit Ctrl + z in terminal
    
if __name__ == "__main__":
    serve()

