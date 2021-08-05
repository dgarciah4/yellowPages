from flask import Flask, render_template, request
import sqlite3
import random
import os
from flask_sqlalchemy import SQLAlchemy
## flask env == yellowEnv
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Company(db.Model):
    __tablename__ ="company"

    name = db.Column(db.Text, primary_key=True)
    addr = db.Column(db.Text)
    email = db.Column(db.Text)
    pNum = db.Column(db.Integer)

    def __init__(self,name,addr,email,pNum):
        self.name = name
        self.addr = addr
        self.email = email
        self.pNum = pNum

@app.route('/')
def home ():
    return render_template('home.html')

@app.route('/records', methods = ['POST', 'GET'])
def records ():
    all_records = Company.query.all()
    return render_template ('records.html',all_records = all_records)

    return render_template('records.html')

@app.route('/forms', methods = ['POST', 'GET'])
def forms ():
    if request.method == 'POST':
        data = request.form
        name = data["name"]
        addr = data["addr"]
        email = data["email"]
        pNum = data["pNum"]

        new_data = Company(name, addr, email, pNum)
        db.session.add(new_data)
        db.session.commit()
        all_records = Company.query.all()
        return render_template('records.html',all_records=all_records)

    return render_template('forms.html')

@app.route('/view_all', methods = ['POST', 'GET'])
def view_all ():
    all_records = Company.query.all()
    return render_template ('records.html',all_records = all_records)

@app.route('/delete_record', methods = ['POST'])
def delete_record():
    if request.method == "POST":
        select_record = request.form.get("company.name")
        Company.query.filter(Company.name==select_record).delete()
        db.session.commit()
    return render_template('records.html', all_records=Company.query.all())

@app.route('/update_name', methods = ['POST'])
def update_name():
    if request.method == "POST":
        select_record = request.form.get("company.name") # get record to update

        name    = request.form.get("new_name")  # getting new name from form
        oldname = select_record    # selecting the old name
        company = Company.query.filter_by(name=oldname).first() #selecting Column
        company.name = name

        db.session.commit()
    return render_template('records.html', all_records=Company.query.all())

@app.route('/update_email', methods = ['POST'])
def update_email():
    if request.method == "POST":
        select_record = request.form.get("company.email") # get record to update

        email    = request.form.get("new_email")  # getting new email from form
        oldemail = select_record    # selecting the old email
        company = Company.query.filter_by(email=oldemail).first() #selecting Column
        company.email = email

        db.session.commit()
    return render_template('records.html', all_records=Company.query.all())

@app.route('/update_addr', methods = ['POST'])
def update_addr():
    if request.method == "POST":
        select_addr = request.form.get("company.addr") # get record to update

        addr    = request.form.get("new_addr")  # getting new address from form
        oldaddr = select_addr    # selecting the old address
        company = Company.query.filter_by(addr=oldaddr).first() #selecting Column
        company.addr = addr

        db.session.commit()
    return render_template('records.html', all_records=Company.query.all())

@app.route('/update_num', methods = ['POST'])
def update_num():
    if request.method == "POST":
        select_pNum = request.form.get("company.pNum") # get record to update

        pNum    = request.form.get("new_pNum")  # getting new number from form
        oldnum = select_pNum    # selecting the old number
        company = Company.query.filter_by(pNum=oldnum).first() #selecting Column
        company.pNum = pNum

        db.session.commit()
    return render_template('records.html', all_records=Company.query.all())




@app.errorhandler(404)
def page_not_found (e):
    return render_template ('404.html'),404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
