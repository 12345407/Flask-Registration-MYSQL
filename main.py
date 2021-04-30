from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_mysqldb import MySQL
import pymysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# config mySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskregister'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={
                           'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={
        'placeholder': 'password'})

    confirmpassword = PasswordField(
        'password', validators=[DataRequired(), EqualTo('password')], render_kw={
            'placeholder': 'confirmpassword'})

    mobile = StringField('', [validators.length(min=10, max=15)], render_kw={
                         'placeholder': 'Mobile'})


class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        dbname = form.name.data
        dbemail = form.email.data
        dbusername = form.username.data
        dbpassword = form.password.data
        dbconfirmpassword = form.confirmpassword.data
        dbmobile = form.mobile.data

        # create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(dbname, dbemail, dbusername, dbpassword, dbconfirmpassword, dbmobile) VALUES(%s, %s, %s, %s, %s, %s)",
                    (dbname, dbemail, dbusername, dbpassword, dbconfirmpassword, dbmobile))

        # commit cursor
        mysql.connection.commit()

        # close cursor
        cur.close()

        flash(' you are now registred! ', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        dbusername = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute(
            "SELECT * FROM users WHERE dbusername=%s", [dbusername])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['dbpassword']
            uid = data['id']
            name = data['dbname']

            # Compare password
            if (password_candidate == password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name

                return redirect(url_for('home'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:

            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route("/out")
def logout():
    if 'uid' in session:
        # create cursor
        cur = mysql.connection.cursor()

        uid = session['uid']
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('home'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
