from flask import Flask, flash, render_template, request, redirect, url_for, session
from Forms import CreateAppointmentUserForm, CreateAppointmentCustomerForm, CreateAppointmentMainForm, CreateMedicalStaff, CreateRating, LoginForm, CreateUserForm
import shelve, UserAppointment, CustomerAppointment, Main, Medicalstaff, Rating
import urllib.request
import os
from werkzeug.utils import secure_filename
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = 'any_random_string'

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)
        user.set_email(update_user_form.email.data)
        user.set_date_joined(update_user_form.date_joined.data)
        user.set_address(update_user_form.address.data)
        user.set_remarks(update_user_form.remarks.data)
        user.set_phone(update_user_form.phone.data)
        user.set_birth(update_user_form.birth.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))
    else:
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()
        update_user_form.email.data = user.get_email()
        update_user_form.date_joined.data = user.get_date_joined()
        update_user_form.address.data = user.get_address()
        update_user_form.remarks.data = user.get_remarks()
        update_user_form.phone.data = user.get_phone()
        update_user_form.birth.data = user.get_birth()
        update_user_form.password.data = user.get_password()

        return render_template('updateUser.html', form=update_user_form)

@app.route('/Dashboard')
def customer_graph():
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    total = 0
    total1 = 0
    total2 = 0
    total3 = 0
    total4 = 0
    total5 = 0
    total6 = 0
    today = date.today()
    todaystr = today.strftime("%Y-%m-%d")
    backday = today - timedelta(days=1)
    backdaystr = backday.strftime("%Y-%m-%d")
    backday1 = today - timedelta(days=2)
    backdaystr1 = backday1.strftime("%Y-%m-%d")
    backday2 = today - timedelta(days=3)
    backdaystr2 = backday2.strftime("%Y-%m-%d")
    backday3 = today - timedelta(days=4)
    backdaystr3 = backday3.strftime("%Y-%m-%d")
    backday4 = today - timedelta(days=5)
    backdaystr4 = backday4.strftime("%Y-%m-%d")
    backday5 = today - timedelta(days=6)
    backdaystr5 = backday5.strftime("%Y-%m-%d")
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customers = customers_dict.get(key)
        customers_list.append(customers)
        if str(customers.get_date_joined()) == todaystr:
            total += 1
        if str(customers.get_date_joined()) == backdaystr:
            total1 += 1
            print(customers.get_date_joined())
        if str(customers.get_date_joined()) == backdaystr1:
            total2 += 1
        if str(customers.get_date_joined()) == backdaystr2:
            total3 += 1
        if str(customers.get_date_joined()) == backdaystr3:
            total4 += 1
        if str(customers.get_date_joined()) == backdaystr4:
            total5 += 1
        if str(customers.get_date_joined()) == backdaystr5:
            total6 += 1

    final = total + total1 + total2 + total3 + total4 + total5 + total6

    print('You have now entered the admin dashboard.')

    return render_template('Dashboard.html', todaystr=todaystr, backdaystr=backdaystr, backdaystr1=backdaystr1, backdaystr2=backdaystr2,
                           backdaystr3=backdaystr3, backdaystr4=backdaystr4, backdaystr5=backdaystr5, total=total, total1=total1, total2=total2, total3=total3
                           , total4=total4, total5=total5, total6=total6, final=final, count=len(customers_list), customers_list=customers_list)

@app.route('/retrieveUsers')
def retrieve_users():
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    rating_dict = {}
    db = shelve.open('rating.db', 'r')
    rating_dict = db['Rating']
    db.close()


    rating_list = []
    total = 0
    for key in rating_dict:
        rating = rating_dict.get(key)
        rating_list.append(rating)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list, rating_list=rating_list)

@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []

    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []

    for key in customers_dict:
        print(key)
        customer = customers_dict.get(key)
        customers_list.append(customer)
        if customer.get_email() == login_form.email.data:
            session['customer_logins'] = customer.get_customer_id()
            session['login'] = customer.get_first_name() + ' ' +customer.get_last_name()
            session['customer_email'] = customer.get_email()
            session['customer_phone'] = customer.get_phone()
            if 'login' in session:
                customername = session['login']
                print(customername)
            if 'customer_email' in session:
                customeremail = session['customer_email']
                print(customeremail)
            if 'customer_phone' in session:
                customerphone = session['customer_phone']
                print(customerphone)
            return render_template('Member_view.html', count=len(customers_list), customers_list=customers_list)
        else:
            for key2 in users_dict:
                print(key2)
                user = users_dict.get(key2)
                users_list.append(user)
                if user.get_email() == login_form.email.data:
                    session['user_login'] = user.get_first_name()
                    session['user_logins'] = user.get_user_id()
                    return redirect(url_for('customer_graph'))

    return render_template('Login.html', form=login_form)

@app.route('/staffimage')
def staff_image():
    return render_template('staffimage.html')

@app.route('/oppsimage')
def oops_image():
    return render_template('oopsimage.html')

UPLOAD_FOLDER = 'static/staffimages/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('staff_image'))
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(url_for('staff_image'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below. You can go back to the form')
        return render_template('staffimage.html', filename=filename)
    else:
        flash('Error - Allowed image types are - png')
        return redirect(url_for('staff_image'))

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='staffimages/' + filename), code=301)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/usersuccess')
def user_success():
    return render_template('usersuccess.html')

@app.route('/customersuccess')
def customer_success():
    return render_template('customersuccess.html')

@app.route('/card')
def card():
    return render_template('card.html')

@app.route('/dash')
def dash():
    session.pop('login', None)
    return render_template('dashboard.html')

@app.route('/appointmentperformance')
def appointment_performance():
    total = 0
    total1 = 0
    total2 = 0
    total3 = 0
    total4 = 0
    total5 = 0
    total6 = 0
    totald = 0
    total1d = 0
    total2d = 0
    total3d = 0
    total4d = 0
    total5d = 0
    total6d = 0
    totalm = 0
    total1m = 0
    total2m = 0
    total3m = 0
    total4m = 0
    total5m = 0
    total6m = 0
    today = date.today()
    todaystr = today.strftime("%d-%m-%Y")
    backday = today - timedelta(days=1)
    backdaystr = backday.strftime("%d-%m-%Y")
    backday1 = today - timedelta(days=2)
    backdaystr1 = backday1.strftime("%d-%m-%Y")
    backday2 = today - timedelta(days=3)
    backdaystr2 = backday2.strftime("%d-%m-%Y")
    backday3 = today - timedelta(days=4)
    backdaystr3 = backday3.strftime("%d-%m-%Y")
    backday4 = today - timedelta(days=5)
    backdaystr4 = backday4.strftime("%d-%m-%Y")
    backday5 = today - timedelta(days=6)
    backdaystr5 = backday5.strftime("%d-%m-%Y")

    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'r')
    appointmentuser_dict = db['Users']
    db.close()

    appointmentuser_list = []
    for key in appointmentuser_dict:
        appointmentuser = appointmentuser_dict.get(key)
        appointmentuser_list.append(appointmentuser)
        if appointmentuser.get_date() == todaystr:
            total += 1
            if appointmentuser.get_type() == "Appointment":
                totald += 1
            if appointmentuser.get_type() == "Massager":
                totalm += 1
        if appointmentuser.get_date() == backdaystr:
            total1 += 1
            if appointmentuser.get_type() == "Appointment":
                total1d += 1
            if appointmentuser.get_type() == "Massager":
                total1m += 1
        if appointmentuser.get_date() == backdaystr1:
            total2 += 1
            if appointmentuser.get_type() == "Appointment":
                total2d += 1
            if appointmentuser.get_type() == "Massager":
                total2m += 1
        if appointmentuser.get_date() == backdaystr2:
            total3 += 1
            if appointmentuser.get_type() == "Appointment":
                total3d += 1
            if appointmentuser.get_type() == "Massager":
                total3m += 1
        if appointmentuser.get_date() == backdaystr3:
            total4 += 1
            if appointmentuser.get_type() == "Appointment":
                total4d += 1
            if appointmentuser.get_type() == "Massager":
                total4m += 1
        if appointmentuser.get_date() == backdaystr4:
            total5 += 1
            if appointmentuser.get_type() == "Appointment":
                total5d += 1
            if appointmentuser.get_type() == "Massager":
                total5m += 1
        if appointmentuser.get_date() == backdaystr5:
            total6 += 1
            if appointmentuser.get_type() == "Appointment":
                total6d += 1
            if appointmentuser.get_type() == "Massager":
                total6m += 1
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'r')
    appointmentcustomer_dict = db['Customers']
    db.close()

    appointmentcustomer_list = []
    for key in appointmentcustomer_dict:
        appointmentcustomer = appointmentcustomer_dict.get(key)
        appointmentcustomer_list.append(appointmentcustomer)
        if appointmentcustomer.get_date() == todaystr:
            total += 1
            if appointmentcustomer.get_type() == "Appointment":
                totald += 1
            if appointmentcustomer.get_type() == "Massager":
                totalm += 1
        if appointmentcustomer.get_date() == backdaystr:
            total1 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total1d += 1
            if appointmentcustomer.get_type() == "Massager":
                total1m += 1
        if appointmentcustomer.get_date() == backdaystr1:
            total2 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total2d += 1
            if appointmentcustomer.get_type() == "Massager":
                total2m += 1
        if appointmentcustomer.get_date() == backdaystr2:
            total3 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total3d += 1
            if appointmentcustomer.get_type() == "Massager":
                total3m += 1
        if appointmentcustomer.get_date() == backdaystr3:
            total4 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total4d += 1
            if appointmentcustomer.get_type() == "Massager":
                total4m += 1
        if appointmentcustomer.get_date() == backdaystr4:
            total5 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total5d += 1
            if appointmentcustomer.get_type() == "Massager":
                total5m += 1
        if appointmentcustomer.get_date() == backdaystr5:
            total6 += 1
            if appointmentcustomer.get_type() == "Appointment":
                total6d += 1
            if appointmentcustomer.get_type() == "Massager":
                total6m += 1

    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        count = len(appointmentuser_list)  + len(appointmentcustomer_list) + len(main_list)
        if main.get_date() == todaystr:
            total += 1
            if main.get_type() == "Appointment":
                totald += 1
            if main.get_type() == "Massager":
                totalm += 1
        if main.get_date() == backdaystr:
            total1 += 1
            if main.get_type() == "Appointment":
                total1d += 1
            if main.get_type() == "Massager":
                total1m += 1
        if main.get_date() == backdaystr1:
            total2 += 1
            if main.get_type() == "Appointment":
                total2d += 1
            if main.get_type() == "Massager":
                total2m += 1
        if main.get_date() == backdaystr2:
            total3 += 1
            if main.get_type() == "Appointment":
                total3d += 1
            if main.get_type() == "Massager":
                total3m += 1
        if main.get_date() == backdaystr3:
            total4 += 1
            if main.get_type() == "Appointment":
                total4d += 1
            if main.get_type() == "Massager":
                total4m += 1
        if main.get_date() == backdaystr4:
            total5 += 1
            if main.get_type() == "Appointment":
                total5d += 1
            if main.get_type() == "Massager":
                total5m += 1
        if main.get_date() == backdaystr5:
            total6 += 1
            if main.get_type() == "Appointment":
                total6d += 1
            if main.get_type() == "Massager":
                total6m += 1
    final = total + total1 + total2 + total3 + total4 + total5 + total6
    print(total)

    rating_dict = {}
    db = shelve.open('rating.db', 'r')
    rating_dict = db['Rating']
    db.close()


    rating_list = []
    totalr = 0
    for key in rating_dict:
        rating = rating_dict.get(key)
        rating_list.append(rating)
        hello = int(rating.get_rating())
        totalr += hello
    rate = "{:.1f}".format(totalr/len(rating_list))

    return render_template('appointmentperformance.html', count = count ,todaystr = todaystr, backdaystr=backdaystr, backdaystr1=backdaystr1, backdaystr2=backdaystr2,
                           backdaystr3=backdaystr3, backdaystr4=backdaystr4, backdaystr5=backdaystr5, main_list = main_list, total = total, total1 = total1, total2 = total2, total3 = total3
                           ,total4 = total4, total5 = total5, total6 = total6, final = final, rating_list = rating_list, count1=len(rating_list), rate=rate)


@app.route('/appointmentGraph')
def retrieve_performance():
    total = 0
    total1 = 0
    total2 = 0
    total3 = 0
    total4 = 0
    total5 = 0
    total6 = 0
    today = date.today()
    todaystr = today.strftime("%d-%m-%Y")
    newday = today + timedelta(days=1)
    newdaystr = newday.strftime("%d-%m-%Y")
    backday = today - timedelta(days=1)
    backdaystr = backday.strftime("%d-%m-%Y")
    backday1 = today - timedelta(days=2)
    backdaystr1 = backday1.strftime("%d-%m-%Y")
    backday2 = today - timedelta(days=3)
    backdaystr2 = backday2.strftime("%d-%m-%Y")
    backday3 = today - timedelta(days=4)
    backdaystr3 = backday3.strftime("%d-%m-%Y")
    backday4 = today - timedelta(days=5)
    backdaystr4 = backday4.strftime("%d-%m-%Y")
    backday5 = today - timedelta(days=6)
    backdaystr5 = backday5.strftime("%d-%m-%Y")
    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'r')
    appointmentuser_dict = db['Users']
    db.close()

    appointmentuser_list = []
    for key in appointmentuser_dict:
        appointmentuser = appointmentuser_dict.get(key)
        appointmentuser_list.append(appointmentuser)
        if appointmentuser.get_date() == todaystr:
            total += 1
        if appointmentuser.get_date() == backdaystr:
            total1 += 1
        if appointmentuser.get_date() == backdaystr1:
            total2 += 1
        if appointmentuser.get_date() == backdaystr2:
            total3 += 1
        if appointmentuser.get_date() == backdaystr3:
            total4 += 1
        if appointmentuser.get_date() == backdaystr4:
            total5 += 1
        if appointmentuser.get_date() == backdaystr5:
            total6 += 1
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'r')
    appointmentcustomer_dict = db['Customers']
    db.close()

    appointmentcustomer_list = []
    for key in appointmentcustomer_dict:
        appointmentcustomer = appointmentcustomer_dict.get(key)
        appointmentcustomer_list.append(appointmentcustomer)
        if appointmentcustomer.get_date() == todaystr:
            total += 1
        if appointmentcustomer.get_date() == backdaystr:
            total1 += 1
        if appointmentcustomer.get_date() == backdaystr1:
            total2 += 1
        if appointmentcustomer.get_date() == backdaystr2:
            total3 += 1
        if appointmentcustomer.get_date() == backdaystr3:
            total4 += 1
        if appointmentcustomer.get_date() == backdaystr4:
            total5 += 1
        if appointmentcustomer.get_date() == backdaystr5:
            total6 += 1

    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        count = len(appointmentuser_list)  + len(appointmentcustomer_list) + len(main_list)
        if main.get_date() == todaystr:
            total += 1
        if main.get_date() == backdaystr:
            total1 += 1
        if main.get_date() == backdaystr1:
            total2 += 1
        if main.get_date() == backdaystr2:
            total3 += 1
        if main.get_date() == backdaystr3:
            total4 += 1
        if main.get_date() == backdaystr4:
            total5 += 1
        if main.get_date() == backdaystr5:
            total6 += 1
    final = total + total1 + total2 + total3 + total4 + total5 + total6



    return render_template('appointmentGraph.html', count = count ,todaystr = todaystr, newdaystr = newdaystr, backdaystr=backdaystr, backdaystr1=backdaystr1, backdaystr2=backdaystr2,
                           backdaystr3=backdaystr3, backdaystr4=backdaystr4, backdaystr5=backdaystr5, main_list = main_list, total = total, total1 = total1, total2 = total2, total3 = total3
                           ,total4 = total4, total5 = total5, total6 = total6, final = final)

@app.route('/thankrating')
def thank_rating():
    return render_template('thankrating.html')

@app.route('/medicalstaff')
def medicalstaff():
    return render_template('medicalstaff.html')

@app.route('/retrieveAll')
def retrieve_all():
    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'r')
    appointmentuser_dict = db['Users']
    db.close()

    appointmentuser_list = []
    for key in appointmentuser_dict:
        appointmentuser = appointmentuser_dict.get(key)
        appointmentuser_list.append(appointmentuser)
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'r')
    appointmentcustomer_dict = db['Customers']
    db.close()

    appointmentcustomer_list = []
    for key in appointmentcustomer_dict:
        appointmentcustomer = appointmentcustomer_dict.get(key)
        appointmentcustomer_list.append(appointmentcustomer)

    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        backday = today - timedelta(days=1)
        backdaystr = backday.strftime("%d-%m-%Y")

    return render_template('retrieveAll.html', appointmentuser_list=appointmentuser_list , appointmentcustomer_list = appointmentcustomer_list , main_list = main_list, todaystr = todaystr, newdaystr = newdaystr, backdaystr=backdaystr)

@app.route('/findMedicalStaff/<int:id>/', methods=['GET', 'POST'])
def find_medical(id):
    update_medical_form = CreateMedicalStaff(request.form)
    if request.method == 'POST' and update_medical_form.validate():
        medical_dict = {}
        db = shelve.open('medical.db', 'w')
        medical_dict = db['Medical']

        medical = medical_dict.get(id)
        medical.set_name(update_medical_form.name.data)
        medical.set_email(update_medical_form.email.data)
        medical.set_phonenum(update_medical_form.phonenum.data)
        medical.set_venue(update_medical_form.venue.data)
        medical.set_date(update_medical_form.date.data)
        medical.set_note(update_medical_form.note.data)

        db['Medical'] = medical_dict
        db.close()

        return redirect(url_for('retrieve_medical'))
    else:
        medical_dict = {}
        db = shelve.open('medical.db', 'r')
        medical_dict = db['Medical']
        db.close()

        medical = medical_dict.get(id)
        update_medical_form.name.data = medical.get_name()
        update_medical_form.email.data = medical.get_email()
        update_medical_form.phonenum.data = medical.get_phonenum()
        update_medical_form.venue.data = medical.get_venue()
        update_medical_form.date.data = medical.get_date()
        update_medical_form.note.data = medical.get_note()

        return render_template('findMedicalStaff.html', form=update_medical_form )


@app.route('/retrieveappointmentMainRecord')
def retrieve_main_record():
    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")

    return render_template('retrieveappointmentMainRecord.html', count=len(main_list), main_list=main_list, todaystr = todaystr, newdaystr = newdaystr)

@app.route('/retrieveFilterMain')
def retrieve_filter_main():
    variable = request.form['variable']
    main_dict = {}
    db = shelve.open('main' + ' ' + variable +'.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)

    return render_template('retrieveFilterMain.html', count=len(main_list), main_list=main_list)

@app.route('/updateappointmentMainTest/<int:id>/', methods=['GET', 'POST'])
def update_main_test(id):
    update_main_form = CreateAppointmentMainForm(request.form)
    if request.method == 'POST' and update_main_form.validate():
        main_dict = {}
        db = shelve.open('main.db','w')
        main_dict = db['Main']

        main = main_dict.get(id)
        main.set_type(update_main_form.type.data)
        main.set_doctor(update_main_form.doctor.data)
        main.set_venue(update_main_form.venue.data)
        main.set_date(update_main_form.date.data)
        main.set_time(update_main_form.time.data)
        main.set_email(update_main_form.email.data)
        main.set_phonenum(update_main_form.phonenum.data)
        main.set_name(update_main_form.name.data)

        db['Main'] = main_dict
        db.close()

        return redirect(url_for('retrieve_main'))
    else:
        main_dict = {}
        db = shelve.open('main.db', 'r')
        main_dict = db['Main']
        db.close()

        main = main_dict.get(id)
        update_main_form.type.data = main.get_type()
        update_main_form.doctor.data = main.get_doctor()
        update_main_form.venue.data = main.get_venue()
        update_main_form.date.data = main.get_date()
        update_main_form.time.data = main.get_time()
        update_main_form.email.data = main.get_email()
        update_main_form.phonenum.data = main.get_phonenum()
        update_main_form.name.data = main.get_name()
        return render_template('updateappointmentMainTest.html', form=update_main_form)

@app.route('/Adminappointments')
def retrieve_the_appointments():
    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'r')
    appointmentuser_dict = db['Users']
    db.close()

    appointmentuser_list = []
    for key in appointmentuser_dict:
        appointmentuser = appointmentuser_dict.get(key)
        appointmentuser_list.append(appointmentuser)
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'r')
    appointmentcustomer_dict = db['Customers']
    db.close()

    appointmentcustomer_list = []
    for key in appointmentcustomer_dict:
        appointmentcustomer = appointmentcustomer_dict.get(key)
        appointmentcustomer_list.append(appointmentcustomer)

    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        backday = today - timedelta(days=1)
        backdaystr = backday.strftime("%d-%m-%Y")
        count3 = len(appointmentuser_list)  + len(appointmentcustomer_list) + len(main_list)

    return render_template('Adminappointments.html', appointmentuser_list=appointmentuser_list , appointmentcustomer_list = appointmentcustomer_list , main_list = main_list, count=len(appointmentuser_list), count1=len(appointmentcustomer_list), count2=len(main_list), count3 = count3 ,todaystr = todaystr, newdaystr = newdaystr, backdaystr=backdaystr)


@app.route('/appointmentGraph')
def graph():
    return render_template('appointmentGraph.html')

@app.route('/uploadimage')
def image():
    return render_template('uploadimage.html')

@app.route('/createappointmentUser', methods=['GET', 'POST'])
def create_appointment_user():
    create_appointment_user_form = CreateAppointmentUserForm(request.form)
    if request.method == 'POST' and create_appointment_user_form.validate():
       appointmentuser_dict = {}
       db = shelve.open('appointmentuser.db', 'c')
       appoint = ["Dr Gilbert", "Dr Darius", "Dr Eden"]
       massage = ["Mr Hero", "Ms Mari", "Mr Kel"]
       today = date.today()
       newday = today + timedelta(days=1)
       newdaystr = newday.strftime("%d-%m-%Y")

       if create_appointment_user_form.type.data == "Appointment":
         if create_appointment_user_form.doctor.data not in appoint:
             session['wrong_dr'] = "Appointments should be by staff with Dr"
             return render_template('createappointmentUser.html', form=create_appointment_user_form)
       if create_appointment_user_form.type.data == "Massager":
         if create_appointment_user_form.doctor.data not in massage:
             session['wrong_mr'] = "Massager should start with Mr"
             return render_template('createappointmentUser.html', form=create_appointment_user_form)

       appointmentuser_dict = {}
       db = shelve.open('appointmentuser.db', 'r')
       appointmentuser_dict = db['Users']

       appointmentuser_list = []
       for key in appointmentuser_dict:
           appointmentuser = appointmentuser_dict.get(key)
           appointmentuser_list.append(appointmentuser)
           if 'login' in session:
               customername = session['login']
               if customername == appointmentuser.get_name():
                   if appointmentuser.get_date() == newdaystr:
                       session['no_way'] = "You cannot book an appointment twice a day"
                       return render_template('createappointmentUser.html', form=create_appointment_user_form)


           if appointmentuser.get_date() == newdaystr:
               if appointmentuser.get_time() == create_appointment_user_form.time.data:
                   if appointmentuser.get_venue() == create_appointment_user_form.venue.data:
                       session['no_time'] = "The timing selected is not available. Check for an available timing"
                       return render_template('createappointmentUser.html', form=create_appointment_user_form)


       try:
            appointmentuser_dict = db['Users']
       except:
            print("Error in retrieving Users from appointmentuser.db.")

       count_id = 0
       appointmentuser_list = []
       for key in appointmentuser_dict:
           appointmentuser = appointmentuser_dict.get(key)
           appointmentuser_list.append(appointmentuser)

       if len(appointmentuser_list) == 0:
          print("Hello")
          last_id = count_id + 1
          print(last_id)
       else:
          appointmentuser_dict = {}
          db = shelve.open('appointmentuser.db', 'r')
          appointmentuser_dict = db['Users']
          id_list = list(appointmentuser_dict.keys())
          last_id = max(id_list) + 1
          print(last_id)
          UserAppointment.UserAppointment.count_id = last_id

       if 'login' in session:
           customername = session['login']
       if 'customer_email' in session:
           customeremail = session['customer_email']
       if 'customer_phone' in session:
           customerphone = session['customer_phone']
       appointmentUser = UserAppointment.UserAppointment(create_appointment_user_form.type.data, create_appointment_user_form.doctor.data,
                         create_appointment_user_form.venue.data, create_appointment_user_form.time.data, create_appointment_user_form.date.data,customername, customeremail, customerphone)
       appointmentuser_dict[appointmentUser.get_user_id()] = appointmentUser
       db['Users'] = appointmentuser_dict

       db.close()


       return redirect(url_for('user_success'))
    return render_template('createappointmentUser.html', form=create_appointment_user_form, )


@app.route('/createappointmentCustomer', methods=['GET', 'POST'])
def create_appointment_customer():
  create_appointment_customer_form = CreateAppointmentCustomerForm(request.form)
  if request.method == 'POST' and create_appointment_customer_form.validate():
     appointmentcustomer_dict = {}
     db = shelve.open('appointmentcustomer.db', 'c')
     today = date.today()
     newday = today + timedelta(days=1)
     newdaystr = newday.strftime("%d-%m-%Y")
     valid = ["6", "8", "9"]
     appoint = ["Dr Gilbert", "Dr Darius", "Dr Eden"]
     massage = ["Mr Hero", "Ms Mari", "Mr Kel"]
     if create_appointment_customer_form.phonenum.data[0] not in valid:
          session['wrong_number'] = "Your phone number should contain 6,8 or 9"
          return render_template('createappointmentCustomer.html', form=create_appointment_customer_form)
     if str(create_appointment_customer_form.name.data).isnumeric() == True:
          print("ok")
          session['no_number'] = "Your name should not have numbers"
          return render_template('createappointmentCustomer.html', form=create_appointment_customer_form)
     if create_appointment_customer_form.type.data == "Appointment":
         if create_appointment_customer_form.doctor.data not in appoint:
             session['wrong_dr'] = "Appointments should be by staff with Dr"
             return render_template('createappointmentCustomer.html', form=create_appointment_customer_form)
     if create_appointment_customer_form.type.data == "Massager":
         if create_appointment_customer_form.doctor.data not in massage:
             session['wrong_mr'] = "Massager should start with Mr"
             return render_template('createappointmentCustomer.html', form=create_appointment_customer_form)

     try:
        appointmentcustomer_dict = db['Customers']
     except:
        print("Error in retrieving Customers from appointmentcustomer.db.")

     count_id = 0
     appointmentcustomer_list = []
     for key in appointmentcustomer_dict:
           appointmentcustomer = appointmentcustomer_dict.get(key)
           appointmentcustomer_list.append(appointmentcustomer)

     if len(appointmentcustomer_list) == 0:
         last_id = count_id + 1
         print(last_id)
     else:
        appointmentcustomer_dict = {}
        db = shelve.open('appointmentcustomer.db', 'r')
        appointmentcustomer_dict = db['Customers']
        id_list = list(appointmentcustomer_dict.keys())
        last_id = max(id_list) + 1
        print(last_id)
        CustomerAppointment.Customer.count_id = last_id

     appointmentcustomer = CustomerAppointment.Customer(create_appointment_customer_form.type.data,
create_appointment_customer_form.doctor.data,
                  create_appointment_customer_form.venue.data, create_appointment_customer_form.time.data,
                  create_appointment_customer_form.date.data, create_appointment_customer_form.email.data,
                  create_appointment_customer_form.phonenum.data,
                  create_appointment_customer_form.name.data, create_appointment_customer_form.status.data )
     appointmentcustomer_dict[appointmentcustomer.get_customer_id()] = appointmentcustomer
     db['Customers'] = appointmentcustomer_dict

     db.close()

     return redirect(url_for('customer_success'))
  return render_template('createappointmentCustomer.html', form=create_appointment_customer_form)

@app.route('/retrieveappointmentUsers')
def retrieve_appointment_users():
    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'r')
    appointmentuser_dict = db['Users']
    db.close()

    appointmentuser_list = []
    for key in appointmentuser_dict:
        appointmentuser = appointmentuser_dict.get(key)
        appointmentuser_list.append(appointmentuser)
        print(appointmentuser.get_user_id())
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        backday = today - timedelta(days=1)
        backdaystr = backday.strftime("%d-%m-%Y")
        if 'login' in session:
            customername = session['login']

    return render_template('retrieveappointmentUsers.html', count=len(appointmentuser_list), appointmentuser_list=appointmentuser_list, todaystr = todaystr, newdaystr = newdaystr, backdaystr = backdaystr, customername = customername)



@app.route('/retrieveappointmentCustomers')
def retrieve_appointment_customers():
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'r')
    appointmentcustomer_dict = db['Customers']
    db.close()

    appointmentcustomer_list = []
    for key in appointmentcustomer_dict:
        appointmentcustomer = appointmentcustomer_dict.get(key)
        appointmentcustomer_list.append(appointmentcustomer)
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        backday = today - timedelta(days=1)
        backdaystr = backday.strftime("%d-%m-%Y")
    return render_template('retrieveappointmentCustomers.html', count=len(appointmentcustomer_list), appointmentcustomer_list=appointmentcustomer_list, todaystr = todaystr, newdaystr = newdaystr, backdaystr = backdaystr)

@app.route('/createMedicalStaff', methods=['GET', 'POST'])
def create_medical():
  create_medical_form = CreateMedicalStaff(request.form)
  if request.method == 'POST' and create_medical_form.validate():
     medical_dict = {}
     db = shelve.open('medical.db', 'c')

     try:
        medical_dict = db['Medical']
     except:
        print("Error in retrieving medical staff from medical.db.")
     count_id = 0
     medical_list = []
     for key in medical_dict:
         medical = medical_dict.get(key)
         medical_list.append(medical)

     if len(medical_list) == 0:
          print("Hello")
          last_id = count_id + 1
          print(last_id)
     else:
        medical_list = {}
        db = shelve.open('medical.db', 'r')
        medical_dict = db['Medical']
        id_list = list(medical_dict.keys())
        last_id = max(id_list) + 1
        print(last_id)
        Medicalstaff.Medicalstaff.count_id = last_id

     medical = Medicalstaff.Medicalstaff(create_medical_form.name.data,create_medical_form.email.data,
                 create_medical_form.phonenum.data, create_medical_form.venue.data, create_medical_form.date.data, create_medical_form.note.data)
     medical_dict[medical.get_medical_id()] = medical
     print(medical.get_name())
     db['Medical'] = medical_dict

     db.close()

     return redirect(url_for('home'))
  return render_template('createMedicalStaff.html', form=create_medical_form)

@app.route('/retrieveMedicalStaff')
def retrieve_medical():
    medical_dict = {}
    db = shelve.open('medical.db', 'r')
    medical_dict = db['Medical']
    db.close()

    medical_list = []
    for key in medical_dict:
        medical = medical_dict.get(key)
        medical_list.append(medical)

    return render_template('retrieveMedicalStaff.html', count=len(medical_list), medical_list=medical_list)

@app.route('/updateMedicalStaff/<int:id>/', methods=['GET', 'POST'])
def update_medical(id):
    update_medical_form = CreateMedicalStaff(request.form)
    if request.method == 'POST' and update_medical_form.validate():
        medical_dict = {}
        db = shelve.open('medical.db', 'w')
        medical_dict = db['Medical']

        medical = medical_dict.get(id)
        medical.set_name(update_medical_form.name.data)
        medical.set_email(update_medical_form.email.data)
        medical.set_phonenum(update_medical_form.phonenum.data)
        medical.set_venue(update_medical_form.venue.data)
        medical.set_date(update_medical_form.date.data)
        medical.set_note(update_medical_form.note.data)

        db['Medical'] = medical_dict
        db.close()

        return redirect(url_for('retrieve_medical'))
    else:
        medical_dict = {}
        db = shelve.open('medical.db', 'r')
        medical_dict = db['Medical']
        db.close()

        medical = medical_dict.get(id)
        update_medical_form.name.data = medical.get_name()
        update_medical_form.email.data = medical.get_email()
        update_medical_form.phonenum.data = medical.get_phonenum()
        update_medical_form.venue.data = medical.get_venue()
        update_medical_form.date.data = medical.get_date()
        update_medical_form.note.data = medical.get_note()

        return render_template('updateMedicalStaff.html', form=update_medical_form )

def retrieve_medical_update():
    medical_dict = {}
    db = shelve.open('medical.db', 'r')
    medical_dict = db['Medical']
    db.close()

    medical_list = []
    for key in medical_dict:
        medical = medical_dict.get(key)
        medical_list.append(medical)

    return render_template('updateMedicalStaff.html', count=len(medical_list), medical_list=medical_list)


@app.route('/createappointmentMain', methods=['GET', 'POST'])
def create_main_appointment():
  create_main_form = CreateAppointmentMainForm(request.form)
  if request.method == 'POST' and create_main_form.validate():
     main_dict = {}
     db = shelve.open('main.db', 'c')
     today = date.today()
     newday = today + timedelta(days=1)
     newdaystr = newday.strftime("%d-%m-%Y")
     valid = ["6", "8", "9"]
     appoint = ["Dr Gilbert", "Dr Darius", "Dr Eden"]
     massage = ["Mr Hero", "Ms Mari", "Mr Kel"]
     if create_main_form.phonenum.data[0] not in valid:
          session['wrong_number'] = "Your phone number should contain 6,8 or 9"
          return render_template('createappointmentMain.html', form=create_main_form)
     if str(create_main_form.name.data).isnumeric() == True:
          print("ok")
          session['no_number'] = "Your name should not have numbers"
          return render_template('createappointmentCustomer.html', form=create_main_form)
     if create_main_form.type.data == "Appointment":
         if create_main_form.doctor.data not in appoint:
             session['wrong_dr'] = "Appointments should be by staff with Dr"
             return render_template('createappointmentMain.html', form=create_main_form)
     if create_main_form.type.data == "Massager":
         if create_main_form.doctor.data not in massage:
             session['wrong_mr'] = "Massager should start with Mr"
             return render_template('createappointmentMain.html', form=create_main_form)

     appointmentuser_dict = {}
     db = shelve.open('appointmentuser.db', 'r')
     appointmentuser_dict = db['Users']

     appointmentuser_list = []
     for key in appointmentuser_dict:
         appointmentuser = appointmentuser_dict.get(key)
         appointmentuser_list.append(appointmentuser)
         if appointmentuser.get_date() == newdaystr:
             if appointmentuser.get_time() == create_main_form.time.data:
                 if appointmentuser.get_venue() == create_main_form.venue.data:
                     session['no_time'] = "The timing selected is not available. Check for an available timing"
                     return render_template('createappointmentMain.html', form=create_main_form)
     try:
        main_dict = db['Main']
     except:
        print("Error in retrieving Main appointments from main.db.")

     count_id = 0
     main_list = []
     for key in main_dict:
         main = main_dict.get(key)
         main_list.append(main)

     if len(main_list) == 0:
        last_id = count_id + 1
        print(last_id)
     else:
        main_dict = {}
        db = shelve.open('main.db', 'r')
        main_dict = db['Main']
        id_list = list(main_dict.keys())
        last_id = max(id_list) + 1
        print(last_id)
        Main.Main.count_id = last_id

     main = Main.Main(create_main_form.name.data,
create_main_form.email.data,
                  create_main_form.phonenum.data, create_main_form.type.data,
                  create_main_form.doctor.data, create_main_form.venue.data,
                  create_main_form.time.data,
                  create_main_form.date.data )
     main_dict[main.get_main_id()] = main
     db['Main'] = main_dict

     db.close()

     session['main_created'] = main.get_name() + ' ' + main.get_email()

     return redirect(url_for('retrieve_the_appointments'))
  return render_template('createappointmentMain.html', form=create_main_form)

@app.route('/retrieveappointmentMain')
def retrieve_main():
    main_dict = {}
    db = shelve.open('main.db', 'r')
    main_dict = db['Main']
    db.close()

    main_list = []
    for key in main_dict:
        main = main_dict.get(key)
        main_list.append(main)
        print(main)
        today = date.today()
        todaystr = today.strftime("%d-%m-%Y")
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        backday = today - timedelta(days=1)
        backdaystr = backday.strftime("%d-%m-%Y")

    return render_template('retrieveappointmentMain.html', count=len(main_list), main_list=main_list, todaystr = todaystr, newdaystr = newdaystr, backdaystr = backdaystr)

@app.route('/updateappointmentUser/<int:id>/', methods=['GET', 'POST'])
def update_appointment_user(id):
    update_user_form = CreateAppointmentUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        today = date.today()
        newday = today + timedelta(days=1)
        newdaystr = newday.strftime("%d-%m-%Y")
        appoint = ["Dr Gilbert", "Dr Darius", "Dr Eden"]
        massage = ["Mr Hero", "Ms Mari", "Mr Kel"]
        appointmentuser_dict = {}
        db = shelve.open('appointmentuser.db', 'w')
        appointmentuser_dict = db['Users']

        appointmentuser_list = []
        for key in appointmentuser_dict:
           appointmentuser = appointmentuser_dict.get(key)
           appointmentuser_list.append(appointmentuser)

        user = appointmentuser_dict.get(id)
        user.set_type(update_user_form.type.data)
        user.set_doctor(update_user_form.doctor.data)
        user.set_venue(update_user_form.venue.data)
        user.set_time(update_user_form.time.data)
        user.set_date(update_user_form.date.data)

        if update_user_form.type.data == "Appointment":
         if update_user_form.doctor.data not in appoint:
             session['wrong_dr'] = "Appointments should be by staff with Dr"
             return render_template('createappointmentUser.html', form=update_user_form)
        if update_user_form.type.data == "Massager":
         if update_user_form.doctor.data not in massage:
             session['wrong_mr'] = "Massager should start with Mr"
             return render_template('createappointmentUser.html', form=update_user_form)
        if update_user_form.date.data == newdaystr:
               if update_user_form.venue.data == appointmentuser.get_venue():
                   if update_user_form.time.data == appointmentuser.get_time():
                       session['no_time'] = "The timing selected is not available. Check for an available timing"
                       return render_template('createappointmentUser.html', form=update_user_form)

        db['Users'] = appointmentuser_dict
        db.close()

        session['user_updated'] = user.get_type() + ' ' + user.get_date()

        return redirect(url_for('retrieve_appointment_users'))
    else:
        appointmentuser_dict = {}
        db = shelve.open('appointmentuser.db', 'r')
        appointmentuser_dict = db['Users']
        db.close()

        user = appointmentuser_dict.get(id)
        userid = user.get_user_id()
        usertype = user.get_type()
        update_user_form.type.data = user.get_type()
        update_user_form.doctor.data = user.get_doctor()
        update_user_form.venue.data = user.get_venue()
        update_user_form.time.data = user.get_time()
        update_user_form.date.data = user.get_date()


        return render_template('updateappointmentUser.html', form=update_user_form, userid=userid, usertype = usertype)

@app.route('/updateappointmentCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer_appointment(id):
    update_customer_form = CreateAppointmentCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        appointmentcustomer_dict = {}
        db = shelve.open('appointmentcustomer.db', 'w')
        appointmentcustomer_dict = db['Customers']

        customer = appointmentcustomer_dict.get(id)
        customer.set_type(update_customer_form.type.data)
        customer.set_doctor(update_customer_form.doctor.data)
        customer.set_venue(update_customer_form.venue.data)
        customer.set_date(update_customer_form.date.data)
        customer.set_time(update_customer_form.time.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_phonenum(update_customer_form.phonenum.data)
        customer.set_name(update_customer_form.name.data)
        customer.set_status(update_customer_form.status.data)

        db['Customers'] = appointmentcustomer_dict
        db.close()

        return redirect(url_for('retrieve_the_appointments'))
    else:
        appointmentcustomer_dict = {}
        db = shelve.open('appointmentcustomer.db', 'r')
        appointmentcustomer_dict = db['Customers']
        db.close()

        customer = appointmentcustomer_dict.get(id)
        update_customer_form.type.data = customer.get_type()
        update_customer_form.doctor.data = customer.get_doctor()
        update_customer_form.venue.data = customer.get_venue()
        update_customer_form.date.data = customer.get_date()
        update_customer_form.time.data = customer.get_time()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.phonenum.data = customer.get_phonenum()
        update_customer_form.name.data = customer.get_name()
        update_customer_form.status.data = customer.get_status()
        return render_template('updateappointmentCustomer.html', form=update_customer_form)

@app.route('/updateappointmentMain/<int:id>/', methods=['GET', 'POST'])
def update_main(id):
    update_main_form = CreateAppointmentMainForm(request.form)
    if request.method == 'POST' and update_main_form.validate():
        main_dict = {}
        db = shelve.open('main.db', 'w')
        main_dict = db['Main']

        main = main_dict.get(id)
        main.set_type(update_main_form.type.data)
        main.set_doctor(update_main_form.doctor.data)
        main.set_venue(update_main_form.venue.data)
        main.set_date(update_main_form.date.data)
        main.set_time(update_main_form.time.data)
        main.set_email(update_main_form.email.data)
        main.set_phonenum(update_main_form.phonenum.data)
        main.set_name(update_main_form.name.data)

        db['Main'] = main_dict
        db.close()

        session['main_updated'] = main.get_name() + ' ' + main.get_email()

        return redirect(url_for('retrieve_the_appointments'))
    else:
        main_dict = {}
        db = shelve.open('main.db', 'r')
        main_dict = db['Main']
        db.close()

        main = main_dict.get(id)
        update_main_form.type.data = main.get_type()
        update_main_form.doctor.data = main.get_doctor()
        update_main_form.venue.data = main.get_venue()
        update_main_form.date.data = main.get_date()
        update_main_form.time.data = main.get_time()
        update_main_form.email.data = main.get_email()
        update_main_form.phonenum.data = main.get_phonenum()
        update_main_form.name.data = main.get_name()
        return render_template('updateappointmentMain.html', form=update_main_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    appointmentuser_dict = {}
    db = shelve.open('appointmentuser.db', 'w')
    appointmentuser_dict = db['Users']

    appointmentuser_dict.pop(id)

    db['Users'] = appointmentuser_dict
    db.close()

    return redirect(url_for('retrieve_appointment_users'))

@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    appointmentcustomer_dict = {}
    db = shelve.open('appointmentcustomer.db', 'w')
    appointmentcustomer_dict = db['Customers']

    appointmentcustomer_dict.pop(id)

    db['Customers'] = appointmentcustomer_dict
    db.close()

    return redirect(url_for('retrieve_the_appointments'))

@app.route('/deleteMain/<int:id>', methods=['POST'])
def delete_main(id):
    main_dict = {}
    db = shelve.open('main.db', 'w')
    main_dict = db['Main']

    main_dict.pop(id)

    db['Main'] = main_dict
    db.close()

    return redirect(url_for('retrieve_the_appointments'))

@app.route('/deleteMedicalStaff/<int:id>', methods=['POST'])
def delete_medical(id):
    medical_dict = {}
    db = shelve.open('medical.db', 'w')
    medical_dict = db['Medical']

    medical_dict.pop(id)

    db['Medical'] = medical_dict
    db.close()

    return redirect(url_for('retrieve_medical'))

@app.route('/createRating', methods=['GET', 'POST'])
def create_rating():
    create_rating_form = CreateRating(request.form)
    if request.method == 'POST' and create_rating_form.validate():
       rating_dict = {}
       db = shelve.open('rating.db', 'c')

       try:
            rating_dict = db['Rating']
       except:
            print("Error in retrieving Users from appointmentuser.db.")

       count_id = 0
       rating_list = []
       for key in rating_dict:
           rating = rating_dict.get(key)
           rating_list.append(rating)

       if len(rating_list) == 0:
          print("Hello")
          last_id = count_id + 1
          print(last_id)
       else:
          rating_dict = {}
          db = shelve.open('rating.db', 'r')
          rating_dict = db['Rating']
          id_list = list(rating_dict.keys())
          last_id = max(id_list) + 1
          print(last_id)
          Rating.Rating.count_id = last_id

       rating = Rating.Rating(create_rating_form.doctor.data, create_rating_form.rating.data,
                         create_rating_form.comments.data)
       rating_dict[last_id] = rating
       db['Rating'] = rating_dict

       db.close()

       return redirect(url_for('thank_rating'))
    return render_template('createRating.html', form=create_rating_form)

@app.route('/retrieveRating')
def retrieve_rating():
    rating_dict = {}
    db = shelve.open('rating.db', 'r')
    rating_dict = db['Rating']
    db.close()


    rating_list = []
    total = 0
    for key in rating_dict:
        rating = rating_dict.get(key)
        rating_list.append(rating)
        hello = int(rating.get_rating())
        total += hello
    rate = total/len(rating_list)
    print(rate)



    return render_template('retrieveRating.html', count=len(rating_list), rating_list=rating_list, rate=rate)

@app.route('/deleteRating/<int:id>', methods=['POST'])
def delete_rating(id):
    rating_dict = {}
    db = shelve.open('rating.db', 'w')
    rating_dict = db['Rating']

    rating_dict.pop(id)

    db['Rating'] = rating_dict
    db.close()

    return redirect(url_for('retrieve_rating'))

if __name__ == '__main__':
    app.run()

