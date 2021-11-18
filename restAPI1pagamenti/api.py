import flask
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>La risorsa non è presente.</p>", 404 #e.code ?

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Gestione pagamenti</h1>
<p> v0.0.1 Prototipo base per una restAPI di pagamenti</p>'''

#getAll http://127.0.0.1:5000/api/v1/resources/payments/all
@app.route('/api/v1/resources/payments/all', methods=['GET'])
def getAll():
    conn = sqlite3.connect('payments1.db')
    conn.row_factory = dict_factory #() ?
    cur = conn.cursor()
    all_payments = cur.execute('SELECT * FROM pays;').fetchall()
    
    return jsonify(all_payments)

#getFiltered
@app.route('/api/v1/resources/payments', methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    id = query_parameters.get('id')
    senderIBAN = query_parameters.get('senderIBAN')
    amount = query_parameters.get('amount')
    recipientIBAN = query_parameters.get('recipientIBAN')
    valid = query_parameters.get('valid')
    paymentDateTime = query_parameters.get('paymentDateTime')
    
    query = "SELECT * FROM pays WHERE"
    to_filter = []
    
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if senderIBAN:
        query += ' senderIBAN=? AND'
        to_filter.append(senderIBAN)
    if amount:
        query += ' amount=? AND'
        to_filter.append(amount)
    if recipientIBAN:
        query += ' recipientIBAN=? AND'
        to_filter.append(recipientIBAN)
    if valid:
        query += ' valid=? AND'
        to_filter.append(valid)
    if paymentDateTime:
        query += ' paymentDateTime=? AND'
        to_filter.append(paymentDateTime)
    if not(id or senderIBAN or amount or recipientIBAN or valid or paymentDateTime):
        return page_not_found(404)

    query = query[:-4] + ';'
    
    conn = sqlite3.connect('payments1.db')
    conn.row_factory = dict_factory #()
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

app.run()
    
    