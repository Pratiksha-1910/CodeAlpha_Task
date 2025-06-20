from flask import Flask, request, render_template
import pymysal
app = Flask(__name__)
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="data_system"
    )
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_data():
    name = request.form['name']
    email = request.form['email']

    conn = connect_db()
    cursor = conn.cursor()

    # Check if duplicate exists
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    result = cursor.fetchone()

    if result:
        return "❌ Duplicate entry found. Data not added."
    
    # Insert only if unique
    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(insert_query, (name, email))
    conn.commit()

    return "✅ Data successfully added!"

if __name__ == '__main__':
    app.run(debug=True)
    