from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock data
status_options = ["Я свободен", "Занят", "Я сплю", "Играю"]
activities = ["Математика", "Испанский", "Укр. мова"]

@app.route('/')
def index():
    status = session.get('status', 'Неизвестно')
    return render_template('index.html', status=status)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'root' and password == '1223':
            session['logged_in'] = True
            session['status'] = 'Неизвестно'
            return render_template('admin.html', status_options=status_options, activities=activities)
        else:
            return "Неверный логин или пароль"
    else:
        if session.get('logged_in'):
            return render_template('admin.html', status_options=status_options, activities=activities)
        else:
            return render_template('admin.html', login_required=True)

@app.route('/update_status', methods=['POST'])
def update_status():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    status = request.form['status']
    activity = request.form.get('activity', '')
    time_range = request.form.get('time_range', '')
    sleep_until = request.form.get('sleep_until', '')
    custom_text = request.form.get('custom_text', '')
    
    if status == "Занят":
        status = f"<span class='red-text'>Занят</span> ({activity})"
        if time_range:
            status += f"<br>с {time_range}"
    elif status == "Я сплю":
        status = f"<span class='blue-text'>Сплю</span>"
        if sleep_until:
            status += f"<br>Не будить до {sleep_until}"
    elif status == "Я свободен":
        status = f"<span class='green-text'>Я свободен</span>"
    
    if custom_text:
        status = custom_text
    
    session['status'] = status
    return redirect(url_for('admin'))

@app.route('/get_status')
def get_status():
    status = session.get('status', 'Неизвестно')
    return jsonify(status=status)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)