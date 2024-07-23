from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('erp.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/customers')
def customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/customers/new', methods=('GET', 'POST'))
def new_customer():
    if request.method == 'POST':
        acct_ref = request.form['acct_ref']
        name = request.form['name']
        email = request.form['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO customers (acct_ref, name, email) VALUES (?, ?, ?)',
                     (acct_ref, name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('customers'))

    return render_template('new_customer.html')

@app.route('/invoices')
def invoices():
    conn = get_db_connection()
    invoices = conn.execute('SELECT * FROM invoices').fetchall()
    conn.close()
    return render_template('invoices.html', invoices=invoices)

@app.route('/invoices/new', methods=('GET', 'POST'))
def new_invoice():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        ref = request.form['ref']
        details = request.form['details']
        amount = request.form['amount']

        conn = get_db_connection()
        conn.execute('INSERT INTO invoices (customer_id, ref, details, amount) VALUES (?, ?, ?, ?)',
                     (customer_id, ref, details, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('invoices'))

    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('new_invoice.html', customers=customers)

@app.route('/payments')
def payments():
    conn = get_db_connection()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    return render_template('payments.html', payments=payments)

@app.route('/payments/new', methods=('GET', 'POST'))
def new_payment():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        ref = request.form['ref']
        amount = request.form['amount']

        conn = get_db_connection()
        conn.execute('INSERT INTO payments (customer_id, ref, amount) VALUES (?, ?, ?)',
                     (customer_id, ref, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('payments'))

    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('new_payment.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)
