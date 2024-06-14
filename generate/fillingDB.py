import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

def fillDB(app, db, Users, Clients):
    with app.app_context():
        if db.session.query(Users) != None:
            db.session.query(Users).delete()
        if db.session.query(Clients) != None:
            db.session.query(Clients).delete()
            db.session.commit()

    users_data = [
        {'login': 'user1', 'password': 'password1', 'name': 'Иван Иванов Иванович'},
        {'login': 'user2', 'password': 'password2', 'name': 'Петр Петров Петрович'},
        {'login': 'user3', 'password': 'password3', 'name': 'Мария Смирнова Генадьевна'}
    ]

    with app.app_context():
        for user in users_data:
            new_user = Users(login=user['login'], password=user['password'], name=user['name'])
            db.session.add(new_user)
            db.session.commit()

        numbers_clients = random.randint(1, 100)

        start_date = datetime(1970, 1, 1)
        end_date = datetime(2024, 1, 1)

        resp_clients = requests.get(f"https://randomus.ru/name?type=0&sex=10&count={numbers_clients}")

        if resp_clients.status_code == 200:
            soup_clients = BeautifulSoup(resp_clients.content, "html.parser")
            clients_data = soup_clients.find_all('div', {'class': 'result_items'})

            with app.app_context():
                all_users = Users.query.all()

                for client in clients_data:
                    fio = client.get_text(strip=True).split()
                    if len(fio) == 3:
                        surname, name, patronymic = fio
                        random_dob = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                        new_client = Clients(
                            surname=surname,
                            name=name,
                            patronymic=patronymic,
                            dob=random_dob.strftime('%Y-%m-%d'),
                            inn=''.join(random.choices('0123456789', k=12)),
                            responsible=random.choice(all_users).name
                        )
                        db.session.add(new_client)
                db.session.commit()
        else:
            print("Ошибка при выполнении запросов.")