# it will have all the views like home page etc that dont need authentication

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates
import os

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
# blueprint- it has a bunch of routes inside it.

from flask_login import login_required, current_user
# this is used to hide the home and others when the user is logged in or not logged in
from datetime import datetime


from .models import Trackers
# from .models import Trackerdata

from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# this will run when we go to the home page or /url
@login_required
# graph needed for redirect(done)
def home():
    if request.method == 'POST':
        idz = request.form.get('idz')
        user = current_user

        if request.form['b1'] == 'b1':
            # graph start

            for i in user.trackers:
                if i.tracker_name == idz and i.tracker_type is not None:
                    x = i.tracker_type
                    if x == 'Multiple Choice':
                        d = {}
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)

                        for j in values:
                            if j not in d:
                                d[j] = 0
                            d[j] += 1
                        mood = list(d.keys())
                        val = list(d.values())

                        fig = plt.figure()

                        # creating the bar plot
                        plt.bar(mood, val, color='blue',
                                width=0.4)

                        plt.xlabel("given choices")
                        plt.ylabel("no of input of each")
                        plt.title("bar chart representation")

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Boolean':
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)
                        y = 0
                        n = 0
                        v = []
                        m = ['Yes', 'No']
                        for j in values:
                            if j == 'Yes':
                                y += 1
                            elif j == 'No':
                                n += 1
                            else:
                                pass
                        v.append(y)
                        v.append(n)

                        # Creating plot
                        fig = plt.figure()
                        plt.pie(v, labels=m)

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Numerical':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('scatter plot')
                        plt.xlabel('Date')
                        plt.ylabel('value')

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Time Duration':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('performance')
                        plt.xlabel('Date')
                        plt.ylabel('minutes')

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                      
                    else:
                      pass

            # graph end
            return redirect(url_for('views.tracker1', idz=idz))
        elif request.form['b1'] == 'b2':
            return redirect(url_for('views.tracker1log', idz=idz))
        elif request.form['b1'] == 'bd':
            Trackers.query.filter_by(
                tracker_name=f'{idz}', user_id=f'{current_user.id}').delete()
            db.session.commit()
            return redirect(url_for('views.home', user=current_user))
        elif request.form['b1'] == 'be':
            return redirect(url_for('views.trackeredit', user=current_user, idz=idz))
        else:
            pass
    return render_template("home.html", user=current_user)

# ok


@views.route('/addtracker', methods=["GET", "POST"])
# graph not needed
def addtracker():
    if request.method == 'POST':
        tracker_name = request.form.get('tracker_name')
        description = request.form.get('description')
        tracker_type = request.form.get('tracker_type')
        settings = request.form.get('settings')

        if len(tracker_name) == 0:
            flash('enter name', category='error')
        elif len(description) == 0:
            flash('enter a description', category='error')
        elif len(tracker_type)==0:
            flash('select a tracker type',category='error')
        elif (tracker_type)=='Multiple Choice' and len(settings)==0:
            flash('enter your choices', category='error')
        else:
            new_tracker = Trackers(tracker_name=tracker_name, settings=settings,
                                   tracker_type=tracker_type, description=description, user_id=current_user.id)

            db.session.add(new_tracker)
            db.session.commit()
            flash('tracker added', category='success')
            return redirect(url_for('views.home'))

    return render_template("addtracker.html", user=current_user)


@views.route('/tracker1log', methods=["GET", "POST"])
# graph not needed.
def tracker1log():
    idz = request.args.get('idz', None)
    if request.method == 'POST':
        time_stamp = request.form.get('time_stamp')
        value = request.form.get('value')
        note = request.form.get('note')

        time_old = time_stamp.replace('T', ' ')
        time_new = datetime.strptime(time_old, '%Y-%m-%d %H:%M')

        if len(time_stamp) == 0:
            flash('enter date and time', category='error')
        elif len(value) == 0:
            flash('enter a value', category='error')
        else:
            new_log = Trackers(time_stamp=time_new, value=value,
                               note=note, tracker_name=idz, user_id=current_user.id)
            db.session.add(new_log)
            db.session.commit()
            flash('log added', category='success')
            user = current_user

            return redirect(url_for('views.home'))

    return render_template("tracker1log.html", user=current_user, idz=idz)

# ok


@views.route('/tracker1', methods=['GET', 'POST'])
# graph needed at delete(done)
def tracker1():
    idz = request.args.get('idz', None)
    user = current_user
    # graph start

    # graph end
    if request.method == 'POST':
        tid = request.form.get('tid')
        if request.form['c1'] == 'd':
            Trackers.query.filter_by(id=f'{tid}').delete()
            db.session.commit()
            # graph start
            for i in user.trackers:
                if i.tracker_name == idz and i.tracker_type is not None:
                    x = i.tracker_type
                    if x == 'Multiple Choice':
                        d = {}
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)

                        for j in values:
                            if j not in d:
                                d[j] = 0
                            d[j] += 1
                        mood = list(d.keys())
                        val = list(d.values())

                        fig = plt.figure()

                        # creating the bar plot
                        plt.bar(mood, val, color='blue',
                                width=0.4)

                        plt.xlabel("given choices")
                        plt.ylabel("no of input of each")
                        plt.title("bar chart representation")

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Boolean':
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)
                        y = 0
                        n = 0
                        v = []
                        m = ['Yes', 'No']
                        for j in values:
                            if j == 'Yes':
                                y += 1
                            elif j == 'No':
                                n += 1
                            else:
                                pass
                        v.append(y)
                        v.append(n)

                        # Creating plot
                        fig = plt.figure()
                        plt.pie(v, labels=m)

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Numerical':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('performance')
                        plt.xlabel('Date')
                        plt.ylabel('value')

                        plt.tight_layout()
                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Time Duration':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('performance')
                        plt.xlabel('Date')
                        plt.ylabel('minutes')

                        plt.tight_layout()
                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    else:
                      pass
                          

            # graph end
            return redirect(url_for('views.tracker1', user=current_user, idz=idz))

        elif request.form['c1'] == 'e':
            return redirect(url_for('views.logedit', user=current_user, tid=tid, idz=idz))

        else:
            pass
    return render_template("tracker1.html", user=current_user, idz=idz)


@views.route('/trackeredit', methods=['GET', 'POST'])
# graph not needed
def trackeredit():
    idz = request.args.get('idz', None)
    if request.method == 'POST':
        tracker_ename = request.form.get('tracker_ename')
        edescription = request.form.get('edescription')

        if len(tracker_ename) == 0:
            flash('enter name', category='error')
        elif len(edescription) == 0:
            flash('enter a description', category='error')
        else:
            pass
            Trackers.query.filter_by(tracker_name=f'{idz}', user_id=f'{current_user.id}').update(
                dict(tracker_name=tracker_ename, description=edescription))
            db.session.commit()
            return redirect(url_for('views.home', user=current_user))

            # flash('tracker added',category='success')
            # return redirect(url_for('views.home'))

    return render_template("trackeredit.html", user=current_user, idz=idz)


@views.route('/logedit', methods=['GET', 'POST'])
# graph needed during redirect
def logedit():
    idz = request.args.get('idz', None)
    tid = request.args.get('tid', None)
    if request.method == 'POST':
        time_stampe = request.form.get('time_stampe')
        valuee = request.form.get('valuee')
        notee = request.form.get('notee')

        time_old = time_stampe.replace('T', ' ')
        time_new = datetime.strptime(time_old, '%Y-%m-%d %H:%M')

        if len(time_stampe) == 0:
            flash('enter date and time', category='error')
        elif len(valuee) == 0:
            flash('enter a value', category='error')
        else:
            Trackers.query.filter_by(id=f'{tid}').update(
                dict(time_stamp=time_new, value=valuee, note=notee))
            db.session.commit()

            user = current_user
            # graph start
            for i in user.trackers:
                if i.tracker_name == idz and i.tracker_type is not None:
                    x = i.tracker_type
                    if x == 'Multiple Choice':
                        d = {}
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)

                        for j in values:
                            if j not in d:
                                d[j] = 0
                            d[j] += 1
                        mood = list(d.keys())
                        val = list(d.values())

                        fig = plt.figure()

                        # creating the bar plot
                        plt.bar(mood, val, color='blue',
                                width=0.4)

                        plt.xlabel("given choices")
                        plt.ylabel("no of input of each")
                        plt.title("bar chart representation")

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Boolean':
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                values.append(i.value)
                        y = 0
                        n = 0
                        v = []
                        m = ['Yes', 'No']
                        for j in values:
                            if j == 'Yes':
                                y += 1
                            elif j == 'No':
                                n += 1
                            else:
                                pass
                        v.append(y)
                        v.append(n)

                        # Creating plot
                        fig = plt.figure()
                        plt.pie(v, labels=m)

                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Numerical':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('performance')
                        plt.xlabel('Date')
                        plt.ylabel('value')

                        plt.tight_layout()
                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    elif x == 'Time Duration':
                        dates = []
                        values = []
                        for i in user.trackers:
                            if i.tracker_name == idz and i.tracker_type is None:
                                dt = i.time_stamp
                                x = dt.strftime('%Y-%m-%d')
                                dates.append(x)
                                values.append(int(i.value))

                        dts = matplotlib.dates.datestr2num(dates)
                        fig = plt.figure()
                        plt.plot_date(dts, values)
                        plt.gcf().autofmt_xdate()
                        plt.title('performance')
                        plt.xlabel('Date')
                        plt.ylabel('minutes')

                        plt.tight_layout()
                        if os.path.exists("website/static/1.png"):
                            os.remove("website/static/1.png")
                            plt.savefig('website/static/1.png')
                        else:
                            plt.savefig('website/static/1.png')
                    else:
                      pass

            # graph end
            return redirect(url_for('views.tracker1', user=current_user, idz=idz))

    return render_template("logedit.html", user=current_user, tid=tid, idz=idz)
