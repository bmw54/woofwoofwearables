import pyrebase
#import config
class RPi2Firebase:

  def __init__(self):
    config = {

    "apiKey": "M3daySH0pEM5DcBgLbw8LVYJakBh2M8anFkDXq0I",

    "authDomain": "woof-woof-wearables.firebaseapp.com",

    "databaseURL": "https://woof-woof-wearables-default-rtdb.firebaseio.com",

    "storageBucket": "woof-woof-wearables.appspot.com"

    }
    firebase = pyrebase.initialize_app(config)
    self.db = firebase.database()
    self.storage = firebase.storage()


  def send_data_to_firebase(self, data, data_name):
    print("Sending Data to Firebase Using Raspberry Pi")
    print("—————————————-")
    print()
    self.db.child(data_name).child("1-set").set(data)

  def send_timeseries_to_firebase(self, data, folder_name, direction, data_name):
    print("Sending TimeSeries to Firebase Using Raspberry Pi")
    print("—————————————-")
    print()
    self.db.child(folder_name).child("2-push").child(data_name).child(direction).push(data)
  
  def send_image_to_firebase(self, path, image_name):
    print("Sending Image to Firebase Using Raspberry Pi")
    print("—————————————-")
    print()
    self.storage.child(image_name).put(path)
    storage_url = self.storage.child(image_name).get_url(None)
    self.db.child("images").child("1-set").set(storage_url)
    self.db.child("images").child("2-push").push(storage_url)
    
    







