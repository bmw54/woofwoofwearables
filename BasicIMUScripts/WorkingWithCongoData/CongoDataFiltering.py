import json

with open("woof-woof-wearables-default-rtdb-2-push-export.json", "r") as read_file:
    data = json.load(read_file)
    print(type(data))
    print("keys:")
    print(data.keys())

    accl = data['accel']
    gyro = data['gyro']
    mag = data['mag']
    print("accel keys:")
    print(accl.keys())
    # print("\n\nvalues:")
    # print(data.values())
    # print(data)

