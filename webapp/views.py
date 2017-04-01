from webapp import app
import json
import requests
from flask import render_template, jsonify, url_for, request, flash, redirect


@app.route('/', methods=['GET'])
def index():
    '''
    Display the list of available options.
    '''

    data = {
        'pageTitle': 'Home',
    }

    return render_template('index.html', data=data)

@app.route('/add/person', methods=['GET', 'POST'])
def add_person():
    '''
    Add a new person.
    '''

    data = {
        'pageTitle': 'Add new person',
        'url': url_for('add_person'),
    }

    if request.method == 'POST':
        data['person_name'] = request.form['person_name'].strip()
        if data['person_name'] == '':
            flash('Name could not be empty.', 'error')
        else:
            headers = {'Content-Type': 'application/json'}
            payload = {'name': data['person_name']}
            r = requests.post(app.config['API_URI'] + '/person', headers = headers, data = json.dumps(payload))
            if r.status_code != 201:
                return 'API Error', r.status_code
            flash('Person "' + data['person_name'] + '" added successfully', 'success')
            return redirect(url_for('person'))

    return render_template('add_person.html', data=data)

@app.route('/add/pet', methods=['GET', 'POST'])
def add_pet():
    '''
    Add a new pet.
    '''

    r = requests.get(app.config['API_URI'] + '/person')
    data = {
        'pageTitle': 'Add new pet',
        'url': url_for('add_pet'),
        'persons': r.json(),
    }

    if request.method == 'POST':
        data['pet_name'] = request.form['pet_name'].strip()
        data['owner_id'] = request.form['owner_id'].strip()
        if data['pet_name'] == '':
            flash('Name could not be empty.', 'error')
        elif data['owner_id'] == '':
            flash('Owner could not be empty.', 'error')
        else:
            headers = {'Content-Type': 'application/json'}
            payload = {'name': data['pet_name'], 'owner_id': data['owner_id']}
            r = requests.post(app.config['API_URI'] + '/pet', headers = headers, data = json.dumps(payload))
            if r.status_code != 201:
                return 'API Error', r.status_code
            flash('Pet "' + data['pet_name'] + '" added successfully', 'success')
            return redirect(url_for('pet'))

    return render_template('add_pet.html', data=data)

@app.route('/delete/person/<id>', methods=['POST'])
def del_person(id):
    '''
    Delete a person.
    '''

    if id == '':
        flash('ID could not be empty.', 'error')
    else:
        r = requests.get(app.config['API_URI'] + '/person/' + id)
        if r.status_code != 200:
            return 'API Error', r.status_code
        pets = r.json()['pets']
        for pet in pets:
            pet_id = str(pet['id'])
            r = requests.delete(app.config['API_URI'] + '/pet/' + pet_id)
            if r.status_code != 204:
                return 'API Error', r.status_code
        r = requests.delete(app.config['API_URI'] + '/person/' + id)
        if r.status_code != 204:
            return 'API Error', r.status_code
        flash('Person #' + id + ' and belonging pets deleted successfully', 'success')
    return redirect(url_for('person'))

@app.route('/delete/pet/<id>', methods=['POST'])
def del_pet(id):
    '''
    Delete a pet.
    '''

    if id == '':
        flash('ID could not be empty.', 'error')
    else:
        r = requests.delete(app.config['API_URI'] + '/pet/' + id)
        if r.status_code != 204:
            return 'API Error', r.status_code
        flash('Pet #' + id + ' deleted successfully', 'success')
    return redirect(url_for('pet'))

@app.route('/person', methods=['GET'])
def person():
    '''
    Display the list of available persons.
    '''

    r = requests.get(app.config['API_URI'] + '/person')
    if r.status_code != 200:
        return 'API Error', r.status_code

    data = {
        'pageTitle': 'List of persons',
        'persons': r.json()
    }

    return render_template('person.html', data=data)

@app.route('/person/<id>', methods=['GET'])
def person_detail(id):
    '''
    Display the details of a person.
    '''

    r = requests.get(app.config['API_URI'] + '/person/' + id)
    if r.status_code != 200:
        return 'API Error', r.status_code

    data = {
        'pageTitle': 'Details of person #' + id,
        'person_details': r.json()
    }

    return render_template('person_detail.html', data=data)

@app.route('/pet', methods=['GET'])
def pet():
    '''
    Display the list of available pets.
    '''

    r = requests.get(app.config['API_URI'] + '/pet')
    if r.status_code != 200:
        return 'API Error', r.status_code

    data = {
        'pageTitle': 'List of pets',
        'pets': r.json()
    }

    return render_template('pet.html', data=data)

@app.route('/pet/<id>', methods=['GET'])
def pet_detail(id):
    '''
    Display the details of a pet.
    '''

    data = {
        'pageTitle': 'Details of pet #' + id,
    }

    return render_template('pet.html', data=data)
