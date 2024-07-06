from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # diperlukan untuk menggunakan session

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    items = [
        {"name": "Beras Emas", "price": 10000, "image": "2.png"},
        {"name": "Beras Kepal Super", "price": 15000, "image": "3.png"},
        {"name": "Beras Merah Premium", "price": 20000, "image": "4.png"}
    ]
    return render_template('index.html', items=items)

@app.route('/order/<item_name>', methods=['GET', 'POST'])
def order(item_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    items = {
        "Beras Emas": 10000,
        "Beras Kepal Super": 15000,
        "Beras Merah Premium": 20000
    }
    price = items.get(item_name, 0)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        quantity = int(request.form['quantity'])
        total_price = price * quantity
        error = None
        if not 10 <= len(phone) <= 12:
            error = "Nomor HP tidak sesuai"
        if error:
            return render_template('order.html', item_name=item_name, price=price, error=error)
        return render_template('thank_you.html', name=name, address=address, phone=phone, total_price=total_price)
    return render_template('order.html', item_name=item_name, price=price)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'saldin' and password == 'saldin123':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Username atau password salah"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
