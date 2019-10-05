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

    def getCurrentGPS(self):
        lat = self.db.child(self.active_player).child('latitude').get().val()
        lon = self.db.child(self.active_player).child('longitude').get().val()
        self.longitude = lon
        self.latitude = lat

    def stream_handler(self, message):
        if message['data']:
            for k, v in message['data'].items():
                if k == 'longitude':
                    self.longitude = float(v)
                if k == 'latitude':
                    self.latitude = float(v)
                if not self.is_ready:
                    self.is_ready = True

    def __init__(self, active_player) -> None:
        super().__init__()
        self.active_player = active_player
        self.longitude = None
        self.latitude = None
        self.is_ready = False
        self.getCurrentGPS()
        self.db.child(active_player).stream(self.stream_handler)


