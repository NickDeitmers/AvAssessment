import drones_pb2_grpc
import drones_pb2
import grpc
import random
import logging
import sys
import time

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("drone_client.log")
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

def stream_position(latitude: float, longitude: float, altitude: float, stub):
        print("In function before call")
        position_request = drones_pb2.PositionRequest(latitude, longitude, altitude)
        position_response = stub.send_position(position_request)
        print(position_request)
        return position_response

def run():
    #Runs the client
    with grpc.insecure_channel("localhost:50051") as channel: #Creates channel that you can connect to grpc
        stub = drones_pb2_grpc.GreeterStub(channel) #Will be used to call grpc calls
        drone_name = input("State the drone's name: ") #Gets user input for drones name (int)
        
        registration_request = drones_pb2.RegistrationRequest(name=int(drone_name)) 
        registration_response = stub.register(registration_request)
        logger.info("Registration Response received: \n{response}".format(response=registration_response))
        
        waypoint_request = drones_pb2.WaypointRequest(id=registration_response.id) #Saves requested waypoint 
        waypoint_response = stub.listen_waypoint(waypoint_request)
        logger.info("Waypoint Response received: \n{response}".format(response=waypoint_response))
        
        live_lat = 0
        live_lon = 0
        req_list = []
        for _ in range(2):
            time.sleep(5)
            live_lat += waypoint_response.latitude / 2
            live_lon += waypoint_response.longitude / 2
            live_alt = float(random.randint(1, 100))
            logger.debug("Before call")
            #position_response = stream_position(stub=stub, latitude=live_lat, longitude=live_lon, altitude=live_alt)
            position = [live_lat, live_lon, live_alt]
            position_request = drones_pb2.PositionRequest(position=position)
            logger.debug("In between")
            req_list.append(position_request)
            logger.debug("after call")
        position_response = stub.send_position(req_list)
        logger.debug(position_response)

        
        
    
if __name__ == "__main__":
    run() 
        
         