import pyrebase

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