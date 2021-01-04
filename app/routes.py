from app import app, db
from app.models import Car, Rent
from flask import render_template, request, url_for, redirect
from datetime import datetime


@app.route('/index')
@app.route('/')
def index():

    # получить все записи из таблицы Car
    cars = Car.query.all()
    car_list = []

    if len(cars) > 0:

        for car in cars:
            detail = {}
            detail['id'] = car.id
            detail['name_auto'] = car.name_auto
            detail['describe'] = car.describe
            detail['rent_price'] = car.rent_price
            detail['transmission'] = car.transmission
            detail['img_url'] = car.img_url
            detail['rents'] = car.rents
            detail['new'] = 'Свободен'

            if len(car.rents) == 0:
                detail['new'] = 'Новый'
            else:
                ss = car.rents[-1].completion
                if ss == None:
                    detail['new'] = 'Занят'

            car_list.append(detail)

    # задать шаблон
    index = 'main.html'

    # полученные наборы передать в контекст:
    context = {
        'index': index,
        'car_list': car_list,
    }

    return render_template(['layout.html'], **context)


@app.route('/rental_log')
def rental_log():

    # получить все записи из таблицы Car
    rental_list = Rent.query.order_by('car_id', 'created').all()

    # получить все записи из таблицы Rent
    index = 'rental_log.html'

    # итоговый список
    list_price = []

    for el in rental_list:
        id = el.car_id

        k = 0
        found = False

        while not found and (k < len(list_price)):
            if list_price[k]['id'] == id:  # в списке есть такой автомобиль
                list_price[k]['count_rent'] += 1

                if el.completion == None :# находится еще в аренде!
                    el.completion = datetime.now()

                list_price[k]['time_rent'] = list_price[k]['time_rent'] + int((el.completion - el.created).total_seconds() / 60)
                list_price[k]['rent'] = format((list_price[k]['time_rent'] * el.car.rent_price), '10,.2f')
                found = True

            k += 1


        if not found:
            price = {}
            # добавить в список новый автомобиль
            price['i'] = len(list_price) + 1
            price['id'] = id
            price['img'] = el.car.img_url
            price['name'] = el.car.name_auto
            price['describe'] = el.car.describe
            price['count_rent'] = 1
            if el.completion == None:
                el.completion = datetime.now()
            price['time_rent'] = int((el.completion - el.created).total_seconds() / 60)
            price['rent'] = format((price['time_rent'] * el.car.rent_price), '10,.2f')

            list_price.append(price)

    # полученные наборы передать в контекст:
    context = {
        'index': index,
        'list_price': list_price,
    }

    return render_template('layout.html', **context)




@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():

    context = None
    index = 'create_auto.html'

    if request.method == 'POST':
        #пришел запрос с методом POST (нажата кнопка ввода)
        #получаем название авто = значение поля input с атрибутом name="name_auto"
        name_auto = request.form['name_auto']

        describe = request.form['describe']

        rent_price = request.form['rent_price']

        # получаем трансмиссию
        if request.form['transmission'] == "1":
            transmission = True    #bool
        else:
            transmission = False

        #добавляем в БД
        db.session.add(Car(name_auto=name_auto, describe=describe, rent_price=rent_price, transmission=transmission, img_url=request.form['img_url']))

        #сохранить изменения в БД
        db.session.commit()


        #заполняем словарь контекста
        context = {
            'index': index,
            'method': 'POST',
            'name_auto': name_auto,
            'describe': describe,
            'rent_price': rent_price,
            'transmission': transmission,
        }

    elif request.method == 'GET':
        #пришел запрос с методом GET - открыта страница
        #просто передается в контекст имя метода
        context = {
            'index': index,
            'method': 'GET',
        }

    return render_template('layout.html', **context)




@app.route('/auto_detail/<int:car_id>', methods=['POST', 'GET'])
def auto_detail(car_id):

    car = Car.query.get(car_id)
    #список для истории аренды
    rental_list = car.rents

    #Значение в поле Доступность
    status_accessibility = "Свободен"
    #Название кнопки
    status_title = "Арендовать"
    #итоговый список
    list_price = []

    if (len(rental_list)) > 0:

        #выбрать последнюю запись из списка
        last_rental = rental_list[-1]

        if last_rental.completion == None:
            status_accessibility = "Занят"
            status_title = "Освободить"

        #подсчитать цену аренды по каждой строке
        i = 1
        for el in rental_list:
            print(el)
            delta = 0
            created = el.created.strftime("%d.%m.%Y %H:%M:%S")
            completion = ''
            if el.completion != None:
                delta = int((el.completion - el.created).total_seconds() / 60)
                completion = el.completion.strftime("%d.%m.%Y %H:%M:%S")

            list_price.append({
                'i': i,
                'created': created,
                'completion': completion,
                'rent': format((delta * car.rent_price), '10,.2f')
            })
            i += 1

    context = None

    if request.method == 'POST':

        new_name = request.form['new_name']
        new_describe = request.form['new_describe']
        new_rent_price = request.form['new_rent_price']
        new_transmission = request.form['new_transmission']
        new_img_url = request.form['new_img_url']

        if new_name: car.name_auto = new_name
        if new_describe: car.describe = new_describe
        if new_rent_price: car.rent_price = new_rent_price
        if new_img_url: car.img_url = new_img_url

        if new_transmission == "1":
            transmission = True  # bool
        else:
            transmission = False
        car.transmission = transmission

        db.session.commit()

    index = 'auto_detail.html'

    if car.transmission == True:
        transmission = 'Да'
        ch_value = ['checked', '']
    else:
        transmission = 'Нет'
        ch_value = ['', 'checked']


    context = {
        'index': index,
        'id': car.id,
        'name_auto': car.name_auto,
        'describe': car.describe,
        'rent_price': car.rent_price,
        'transmission': transmission,
        'ch_value': ch_value,
        'img_url': car.img_url,
        'list_price': list_price,
        'status_accessibility': status_accessibility,
        'status_title': status_title
    }

    return render_template('layout.html', **context)



@app.route('/create_rental/<int:car_id>', methods=['POST', 'GET'])
def create_rental(car_id):

    context = None
    index = 'auto_detail.html'

    if request.method == 'POST':
        rental_list = Rent.query.filter_by(car_id=car_id).order_by('created')
        status_accessibility = ''
        status_title=''
        flNew = False


        if (rental_list.count()) > 0:
            # выбрать последнюю запись из списка
            last_rental = rental_list[- 1]

            print(last_rental.created, last_rental.completion)
            # print(last_rental.car.describe)

            if last_rental.completion == None: #освободить - запись последнюю изменить
                status_accessibility = "Свободен"
                status_title = "Арендовать"
                last_rental.completion = datetime.now()
                db.session.commit()

            else: # добавить новую запись
                flNew = True

        else:  # добавить новую запись
            flNew = True


        if flNew:# добавить новую запись
            status_accessibility = "Занят"
            status_title = "Освободить"
            created = datetime.now()
            completion = None

            # добавляем в БД
            db.session.add(Rent(car_id=car_id, created=created, completion=completion))

            # сохранить изменения в БД
            db.session.commit()

        context = {
            'index': index,
            'status_accessibility': status_accessibility,
            'status_title': status_title
        }

    #перенаправляем на чтение страницы auto_detail
    return redirect(url_for('auto_detail', car_id = car_id))



@app.route('/del_auto/<int:car_id>', methods=['POST'])
def del_auto(car_id):
    car = Car.query.get(car_id)

    db.session.delete(car)
    db.session.commit()

    return redirect(url_for('index'))

