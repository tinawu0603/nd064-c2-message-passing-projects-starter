from concurrent import futures
import json
import os
import time
from kafka import KafkaProducer
import grpc
import location_pb2
import location_pb2_grpc

# Add environment variables in deployment
kafka_host = os.environ["KAFKA_HOST"]
kafka_topic = os.environ["KAFKA_TOPIC"]
kafka_producer = KafkaProducer(bootstrap_servers=kafka_host)

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("Received a location!")

        request_value = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude)
        }
        print(request_value)
        kafka_data = json.dumps(request_value).encode()
        kafka_producer.send(kafka_topic, kafka_data)
        kafka_producer.flush()
        return location_pb2.LocationMessage(**request_value)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
