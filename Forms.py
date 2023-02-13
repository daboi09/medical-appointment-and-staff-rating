from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField, PasswordField, TelField
from datetime import date , timedelta

today = date.today()
newday = today + timedelta(days=1)
newdaystr = newday.strftime("%d-%m-%Y")
todaystr = today.strftime("%d-%m-%Y")
backday = today - timedelta(days=1)
backdaystr = backday.strftime("%d-%m-%Y")

class CreateAppointmentUserForm(Form):
    type = SelectField('Type', [validators.DataRequired()], choices=[('', 'Select'), ('Appointment', 'Appointment'), ('Massager', 'Massager')], default='')
    doctor = SelectField('Doctors/Massagers', [validators.DataRequired()], choices=[('', 'Select'), ('Dr Gilbert', 'Dr Gilbert'), ('Dr Darius', 'Dr Darius'), ('Dr Eden', 'Dr Eden'), ('Mr Hero', 'Mr Hero'), ('Ms Mari', 'Ms Mari'), ('Mr Kel', 'Mr Kel')], default='')
    venue = SelectField('Venue', [validators.DataRequired()], choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Khatib', 'Khatib'), ('Yishun', 'Yishun')], default='')
    time = SelectField('Time', [validators.DataRequired()], choices=[('', 'Select'), ('9am', '9am'), ('9:30am', '9:30am'), ('10am', '10am'), ('10:30am', '10:30am'), ('11am', '11am'), ('11:30am', '11:30am'), ('12pm', '12pm')
                                                                           , ('12:30pm', '12:30pm'), ('1pm', '1pm'), ('1:30pm', '1:30pm'), ('2pm', '2pm'), ('2:30pm', '2:30pm'), ('3pm', '3pm'), ('3:30pm', '3:30pm')
                                                                           , ('4pm', '4pm'), ('4:30pm', '4:30pm')], default='')
    date = SelectField('Date', [validators.DataRequired()], choices=[(newdaystr,newdaystr)])

class CreateAppointmentCustomerForm(Form):
    type = SelectField('Type', [validators.DataRequired()], choices=[('', 'Select'), ('Appointment', 'Appointment'), ('Massager', 'Massager')], default='')
    doctor = SelectField('Prefered Doctors/Massagers', [validators.DataRequired()], choices=[('', 'Select'), ('Dr Gilbert', 'Dr Gilbert'), ('Dr Darius', 'Dr Darius'), ('Dr Eden', 'Dr Eden'), ('Mr Hero', 'Mr Hero'), ('Ms Mari', 'Ms Mari'), ('Mr Kel', 'Mr Kel')], default='')
    venue = SelectField('Prefered Venue', [validators.DataRequired()], choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Khatib', 'Khatib'), ('Yishun', 'Yishun')], default='')
    time = SelectField('Prefered Time', [validators.DataRequired()], choices=[('', 'Select'), ('9am', '9am'), ('9:30am', '9:30am'), ('10am', '10am'), ('10:30am', '10:30am'), ('11am', '11am'), ('11:30am', '11:30am'), ('12pm', '12pm')
                                                                           , ('12:30pm', '12:30pm'), ('1pm', '1pm'), ('1:30pm', '1:30pm'), ('2pm', '2pm'), ('2:30pm', '2:30pm'), ('3pm', '3pm'), ('3:30pm', '3:30pm')
                                                                           , ('4pm', '4pm'), ('4:30pm', '4:30pm')], default='')
    date = SelectField('Date', [validators.DataRequired()], choices=[(newdaystr,newdaystr)])
    name = TextAreaField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phonenum = StringField('Phone Number', [validators.DataRequired() ])
    status = SelectField('Status', [validators.DataRequired()], choices=[('Checked', 'Checked'), ('Unchecked', 'Unchecked')], default='Unchecked')

class CreateAppointmentMainForm(Form):
    type = SelectField('Type', [validators.DataRequired()], choices=[('', 'Select'), ('Appointment', 'Appointment'), ('Massager', 'Massager')], default='')
    doctor = SelectField('Doctors/Massagers', [validators.DataRequired()], choices=[('', 'Select'), ('Dr Gilbert', 'Dr Gilbert'), ('Dr Darius', 'Dr Darius'), ('Dr Eden', 'Dr Eden'), ('Mr Hero', 'Mr Hero'), ('Ms Mari', 'Ms Mari'), ('Mr Kel', 'Mr Kel')], default='')
    venue = SelectField('Venue', [validators.DataRequired()], choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Khatib', 'Khatib'), ('Yishun', 'Yishun')], default='')
    time = SelectField('Time', [validators.DataRequired()], choices=[('', 'Select'), ('9am', '9am'), ('9:30am', '9:30am'), ('10am', '10am'), ('10:30am', '10:30am'), ('11am', '11am'), ('11:30am', '11:30am'), ('12pm', '12pm')
                                                                           , ('12:30pm', '12:30pm'), ('1pm', '1pm'), ('1:30pm', '1:30pm'), ('2pm', '2pm'), ('2:30pm', '2:30pm'), ('3pm', '3pm'), ('3:30pm', '3:30pm')
                                                                           , ('4pm', '4pm'), ('4:30pm', '4:30pm')], default='')
    date = SelectField('Date', [validators.DataRequired()], choices=[(newdaystr,newdaystr)])
    name = TextAreaField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phonenum = StringField('Phone Number', [validators.DataRequired() ])

class CreateMedicalStaff(Form):
    venue = SelectField('Venue', [validators.DataRequired()], choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Khatib', 'Khatib'), ('Yishun', 'Yishun')], default='')
    name = TextAreaField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phonenum = StringField('Phone Number', [validators.DataRequired() ])
    date = DateField('Date joined', format='%Y-%m-%d')
    note = TextAreaField('Note', [validators.DataRequired()])

class CreateRating(Form):
    doctor = SelectField('Select Doctor', [validators.DataRequired()], choices=[('', 'Select'), ('Gilbert', 'Gilbert'), ('Darius', 'Darius'), ('Eden', 'Eden'), ('Hero', 'Hero'), ('Mari', 'Mari'), ('Kel', 'Kel')], default='')
    rating = SelectField('Select Rating', [validators.DataRequired()], choices=[('', 'Select'), (5, 5), (4, 4), (3, 3), (2,2), (1,1)], default='')
    comments = TextAreaField('Comments')

class LoginForm(Form):
    email = EmailField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.DataRequired()])

class CreateUserForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = RadioField('', choices=[('D', 'Doctor'), ('M', 'Massager'), ('R', 'Receptionist')], default='D')
    email = EmailField('', [validators.Email(), validators.DataRequired()])
    phone = TelField('', [validators.Length(min=8, max=8), validators.DataRequired()])
    birth = DateField('', format='%Y-%m-%d')
    date_joined = DateField('', format='%Y-%m-%d', default=date.today())
    address = TextAreaField('', [validators.length(max=200), validators.DataRequired()])
    remarks = TextAreaField('', [validators.Optional()])
    password = PasswordField('', [validators.DataRequired()])
