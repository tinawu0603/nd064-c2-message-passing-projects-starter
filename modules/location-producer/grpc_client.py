import grpc
import location_pb2
import location_pb2_grpc

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30003")
stub = location_pb2_grpc.LocationServiceStub(channel)

location1 = location_pb2.LocationMessage(
    person_id=5,
    latitude=100,
    longitude=100
)

location2 = location_pb2.LocationMessage(
    person_id=6,
    latitude=100,
    longitude=100
)

response1 = stub.Create(location1)
response2 = stub.Create(location2)

print("Responses")
print(response1)
print(response2)
