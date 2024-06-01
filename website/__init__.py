from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hfjksf;jjdksjkjwndmznkjhdkjdhw12jf1jf8dsfh8d3af[snfwf' # Любая строка, ни на что не влияет
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    # url_prefix='/' - означет что добавить к url, '/' - ничего не добавлять
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            init_database(db)
        print('Created database!')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def init_database(db):
    db.create_all()

    init_user_table(db)
    init_booking_table(db)

    from .models import User, Booking
    users = User.query.all()
    bookings = Booking.query.all()
    for user in users:
        print(user.id, end=' ')
        print(user.email, end=' ')
        print(user.password, end=' ')
        print(user.first_name, end=' ')
        print(user.number_of_violations, end=' ')
        print(user.ban_time, end=' ')
        print(user.number_booked)
    for booking in bookings:
        print(booking.id, end=' ')
        print(booking.time_start_h, end=' ')
        print(booking.time_start_m, end=' ')
        print(booking.time_end_h, end=' ')
        print(booking.time_end_m, end=' ')
        print(booking.weekday, end=' ')
        print(booking.is_booked, end=' ')
        print(booking.is_online, end=' ')
        print(booking.is_scanned, end=' ')
        print(booking.is_in_progress, end=' ')
        print(booking.is_ready, end=' ')
        print(booking.is_expired, end=' ')
        print(booking.date, end=' ')
        print(booking.user_id)

def init_user_table(db):
    from .models import User
    # password = 'hfjks@hfh#ufhi!#h238hf93hfh92h39fkld'
    # print(generate_password_hash(password, method='pbkdf2'))
    user_admin = User(id=0, email='admin', first_name='admin',
                      password='pbkdf2:sha256:600000$RpnpAsCnLyftsFkQ$e1983c28aba854e94284f9fa672df6ca22da7627e3936f817644cf4f4c8f9aa6')
    db.session.add(user_admin)
    db.session.commit()

def init_booking_table(db):
    import json
    from .models import Booking
    import datetime
    # Opening JSON file
    with open('website/static/booking_json.txt') as json_file:
        bookingList = []
        for jsonObj in json_file:
            if jsonObj != '':
                bookingDict = json.loads(jsonObj)
                bookingList.append(bookingDict)
        for booking_dict in bookingList:
            time_start_string_arr = booking_dict['time_start'].split(":")
            time_start_h = int(time_start_string_arr[0])
            time_start_m = int(time_start_string_arr[1])
            time_end_string_arr = booking_dict['time_end'].split(":")
            time_end_h = int(time_end_string_arr[0])
            time_end_m = int(time_end_string_arr[1])
            is_booked = booking_dict['is_booked'] == 1
            is_online = booking_dict['is_online'] == 1
            is_scanned = booking_dict['is_scanned'] == 1
            is_in_progress = booking_dict['is_in_progress'] == 1
            is_ready = booking_dict['is_ready'] == 1
            is_expired = booking_dict['is_expired'] == 1
            dd, mm, yyyy = map(int, booking_dict['date'].split("/"))
            date = datetime.date(yyyy, mm, dd)
            weekday = date.weekday() + 1
            booking = Booking(time_start_h=time_start_h, time_start_m=time_start_m,
                              time_end_h=time_end_h, time_end_m=time_end_m,
                              weekday=weekday, is_booked=is_booked, is_online=is_online,
                              is_scanned=is_scanned, is_in_progress=is_in_progress,
                              is_ready=is_ready, is_expired=is_expired, date=date, user_id=0)
            db.session.add(booking)
    db.session.commit()