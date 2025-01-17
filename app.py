from bottle import Bottle, route, run, template, static_file, request, error, hook, get, post, server_names
import bottle
import dill as pickle
from beaker.middleware import SessionMiddleware
import json
import datetime
import control
from db_models import *

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


def show_error(error_title, error_text="", timeout=120):
    return template('tpl/error.tpl', error_title=error_title, error_text=error_text, timeout=timeout)


@error(500)
def handle_error500(error):
    return show_error("Es ist ein interner Fehler aufgetreten", error)


@route('/static/<type>/<filename>')
def serve_css(type, filename):
    return static_file(filename, root=type+'/')


@get('/')
def main_menu():
    request.session['product'] = None
    request.session['customer'] = None
    request.session['customer_verified'] = False
    return template('tpl/main.tpl', customers=Customer.select())


@get('/customer/<id>')
def sel_customer(id):

    customer = Customer.get_by_id(id)
    request.session['customer'] = customer
    if customer.pin:
        return template('tpl/keypad.tpl', customer=customer)
    else:
        request.session['user_verified'] = True
        return template('tpl/products.tpl', products=Product.select(), customer=customer)


@get("/keypad")
def show_keypad():
    return template('tpl/keypad')


@post('/keypad')
def process_keypad():
    pin = request.forms.get('pin')
    if pin == request.session['customer'].pin:
        request.session['customer_verified'] = True
        return template('tpl/products.tpl', products=Product.select(), customer=request.session['customer'])
    else:
        return show_error("Falsche Pin", "Du hast leider eine falsche Pin eingegeben.", 5)

@get('/product/<id>')
def show_product(id):
    product = Product.select(Product.get_id == id)
    request.session['product'] = product
    customer_name = request.session['customer'].name
    #product_name = request.session['product'].name
    return template('tpl/confirm.tpl', customer=customer_name)

@route('/confirm')
def confirm():
    #database.pay(request.session['customer'], request.session['product'])
    t = Transaction()
    t.c = request.session['customer']
    t.p = request.session['product']
    t.amount = request.session['product'].price
    t.quantity = 1
    t.save()
    return show_error("Kauf erfolgreich!", timeout=2)


@post('/product_barcode')
def submit_product_barcode():
    barcode = request.forms.get('barcode')
    product = Product.select(Product.ean == barcode)
    if product == None:
        return show_error("Barcode nicht gefunden", "Zu diesem Barcode wurde kein Produkt gefunden: " + barcode)
    request.session['product'] = product
    return template('tpl/confirm.tpl',  product=product, customer=request.session['customer'])

@post('/customer_barcode')
def submit_customer_barcode():
    barcode = request.forms.get('barcode')
    customer = Customer.select(Customer.rfid == barcode)
    if customer == None:
        return show_error("RFID/Barcode nicht gefunden", "Zu dieser RFID oder Barcode"
                                                         " wurde kein Mitglied gefunden: " + barcode)
    request.session['customer'] = customer
    return template('tpl/products.tpl', customer=customer)

@get('/create_customer')
def create_user():
    return template('tpl/create_user.tpl')


@get('/cash_payin')
def cash_payin():
    return template('tpl/cash_payin', customer = Customer.select(Customer.get_id == str(request.session['customer']['id'])))


@post('/cash_payin')
def register_payment():
    value  = float(request.forms.get('1xx.xx')) * 100.0
    value += float(request.forms.get('x1x.xx')) * 10.0
    value += float(request.forms.get('xx1.xx')) * 1.0
    if(value < 0 or value > 999):
        return show_error("Falsche Zahl eingegeben!", "Du kannst nur zwischen 0€ und 999€ einzahlen.")

    customer_id = request.session['customer']['id']
    print(value)
    database.register_transaction(customer_id, value)
    request.session['customer'] = Customer.select(Customer.get_id == str(customer_id))

    return show_error(str(value) + "€ eingezahlt, dein neuer Kontostand beträgt "
                      + str(request.session['customer'].get_credit()) + "€!")


@post('/new_user')
def new_user():
    user= Customer()
    user.name = request.forms.get('name')
    user.rfid = request.forms.get('rfid')
    user.pin = request.forms.get('pin')
    user.email = request.forms.get('email')
    user.save()
    return template('tpl/main.tpl', customers=database.get_customers())


run(app, host='127.0.0.1', port=8081)