from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_mysqldb import MySQL
import pymysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, EmailField

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# config mySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYAQL_DB'] = 'flaskregister'
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
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    confirmpassword = PasswordField('', validators=[length(min=3), EqualTo(password)],
                                    render_kw={'placeholder': 'Password'})
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
        dbpassword = form.password.data
        dbconfirmpassword = form.confirmpassword.data
        dbmobile = form.mobile.data

        # create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(dbname, dbemail, dbusername, dbpassword, dbconfirmpassword, dbmobile) VALUES(%s, %s, %s, %s, %s, %s)",
                    (name, email, username, password, confirmpassword, mobile))

        # commit cursor
        mysql.connection.commit()

        # close cursor
        cur.close()

        flash(f'{name}, you are now registred! ', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.run(debug=True)
