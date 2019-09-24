import pyrebase

class GPS:
    firebaseConfig = {
        "apiKey": "AIzaSyB-U_I8SF5gEP8X7qsK25kaYdutvChfqiw",
        "authDomain": "gps-raspberry-fb0c1.firebaseapp.com",
        "databaseURL": "https://gps-raspberry-fb0c1.firebaseio.com",
        "projectId": "gps-raspberry-fb0c1",
        "storageBucket": "gps-raspberry-fb0c1.appspot.com",
        "messagingSenderId": "801324388112",
        "appId": "1:801324388112:web:640f4dbd916edff3a99f95"
    };

    firebase = pyrebase.initialize_app(firebaseConfig)

    db = firebase.database()

    def stream_handler(self, message):
        if message['data']:
            for k, v in message['data'].items():
                if k == 'longitude':
                    self.longitude = v
                if k == 'latitude':
                    self.latitude = v
                if not self.is_ready:
                    self.is_ready = True

    def __init__(self) -> None:
        super().__init__()
        self.longitude = None
        self.latitude = None
        self.is_ready = False
        self.db.child('gps').stream(self.stream_handler)

gps_tracker = GPS()

