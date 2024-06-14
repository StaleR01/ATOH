from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from generate import fillingDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'clients': 'sqlite:///clients.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __bind_key__ = 'users'
    login = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Users {self.login}>'

class Clients(db.Model):
    __bind_key__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    patronymic = db.Column(db.String(32), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    inn = db.Column(db.String(12), nullable=False)
    responsible = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(32), default="Не в работе")

    def __repr__(self):
        return f'<Clients {self.id}>'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['user_name']
    password = request.form['password']

    user = Users.query.filter_by(login=username).first()
    if user and user.password == password:
        return redirect(url_for('clients_view', user_name=user.name))
    return 'Неверный логин или пароль'

@app.route('/clients/<user_name>')
def clients_view(user_name):
    user_clients = Clients.query.filter_by(responsible=user_name).all()
    return render_template('clients.html', clients=user_clients, user_name=user_name)

@app.route('/update_status', methods=['POST'])
def update_status():
    client_id = int(request.form['id'])
    new_status = request.form['status']
    user_name = request.form['user_name']

    client = Clients.query.get(client_id)
    if client:
        client.status = new_status
        db.session.commit()

    return redirect(url_for('clients_view', user_name=user_name))

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        fillingDB.fillDB(app, db, Users, Clients)
    app.run(debug=True)
