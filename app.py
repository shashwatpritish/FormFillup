from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class Form(db.Model):
    name = db.Column(db.String(40),nullable=False,primary_key=False)
    email = db.Column(db.String(100),nullable=False,primary_key=True)
    feedback = db.Column(db.String(5000))

    def __repr__(self) -> str:
        return f"{self.name} - {self.email} - {self.feedback}"


with app.app_context():
    db.create_all()

@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']
        form = Form(name=name,email=email,feedback=feedback)
        db.session.add(form)
        db.session.commit()
    data = Form.query.all()
    return render_template('index.html', data=data)
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True,host="localhost", port=3000)