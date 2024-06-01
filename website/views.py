from . import db
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Booking
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Заметка должна быть больше 1 символа', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Заметка добавлена', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/get-time-intervals', methods=['POST'])
def get_time_intervals():
    time_intervals = {10:13, 13:16, 16:19}
    weekday = json.loads(request.data)
    weekDayDifference = weekday['weekDayDifference']
    is_intervals = [False, False, False]
    cur_date = datetime.now()
    cur_time = cur_date.time()
    cur_time_h = cur_time.hour
    cur_time_m = cur_time.minute
    cur_weekday = cur_date.weekday() + 1
    if not current_user.is_anonymous:
        if current_user.id == 0:
            available_intervals_idx = []
            not_available_intervals_idx = []
            for idx in range(len(is_intervals)):
                not_available_intervals_idx.append(idx)
            return jsonify({"available_intervals_idx": available_intervals_idx, "not_available_intervals_idx": not_available_intervals_idx})
    selected_weekday = cur_weekday + weekDayDifference
    bookings = Booking.query.filter_by(is_expired=False, is_booked=False, weekday=selected_weekday, is_online=True)
    print(bookings)
    for booking in bookings:
        if (weekDayDifference == 0):
            time_index = 0
            temp_time_intervals = time_intervals.copy()
            for time_start in temp_time_intervals.keys():
                if (time_start <= booking.time_start_h and booking.time_start_h < time_intervals[time_start]):
                    if (cur_time_h <= booking.time_start_h):
                        if (booking.time_start_h - cur_time_h == 0):
                            if (booking.time_start_m - cur_time_m >= 2):
                                is_intervals[time_index] = True
                                del time_intervals[time_start]
                        elif (booking.time_start_h - cur_time_h == 1):
                            if (60 - cur_time_m + booking.time_start_m >= 2):
                                is_intervals[time_index] = True
                                del time_intervals[time_start]
                        else:
                            is_intervals[time_index] = True
                            del time_intervals[time_start]
                time_index += 1
        else:
            time_index = 0
            temp_time_intervals = time_intervals.copy()
            for time_start in temp_time_intervals.keys():
                if (time_start <= booking.time_start_h and booking.time_start_h < time_intervals[time_start]):
                    is_intervals[time_index] = True
                    del time_intervals[time_start]
                time_index += 1

    idx = 0
    available_intervals_idx = []
    not_available_intervals_idx = []
    for is_interval in is_intervals:
        if is_interval:
            available_intervals_idx.append(idx)
        else:
            not_available_intervals_idx.append(idx)
        idx += 1
    print(available_intervals_idx)
    print(not_available_intervals_idx)
    return jsonify({"available_intervals_idx": available_intervals_idx,
                    "not_available_intervals_idx": not_available_intervals_idx})

@views.route('/booking', methods=['GET', 'POST'])
def booking():
    date = datetime.now()
    cur_time = date.time()
    cur_time_h = cur_time.hour
    cur_time_m = cur_time.minute
    # cur_weekday = date.weekday() + 1
    # cur_weekday = 1
    booking_dict = {}
    bookings = Booking.query.filter_by(is_booked=False)
    for booking in bookings:
        if cur_time_h < booking.time_start_h or\
            cur_time_h == booking.time_start_h and cur_time_m < booking.time_start_m:
            if not booking_dict.get(booking.time_start_h):
                booking_dict[booking.time_start_h] = []
            booking_dict[booking.time_start_h].append(booking)

    # if current_user.id == 0:
    #     booking = Booking.query.filter_by(is_booked=False, weekday=cur_weekday)
    # else:
    #     booking = Booking.query.filter_by(is_booked=False, is_online=True)

    # if current_user.number_booked == 0:
    #     if current_user.number_of_violations == 0:
    #         if current_user.number_of_violations == 0:
    #             booking = Booking.query.filter_by(is_booked=False, weekday=cur_weekday, is_online=True)
    #         else:
    #
    #     elif current_user.ban_time < cur_time:
    #         if current_user.number_of_violations > 0:
    #
    #
    # else:
    return render_template("booking.html", user=current_user, booking_dict=booking_dict,
                           cur_time_h=cur_time_h, cur_time_m=cur_time_m)
