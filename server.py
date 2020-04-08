from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from functions import sortable, filterable, wraps

app = Flask(__name__)

# Konfiguriere die Datenbank
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'

db = SQLAlchemy(app)

# Aufgabenklasse
class Quests(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quest_text = db.Column(db.String(250))
    quest_art = db.Column(db.String(20))
    quest_state = db.Column(db.String(25))
    created_at = db.Column(db.DateTime, default = datetime.now)

# Wendet alle filter auf die query an
def render(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = func()
        print("===render===")
        query = ctx.get('query')
        filter_by = ctx.get('filter_by')
        sort_dir = ctx.get('sort_direction')
        if filter_by:
            query = query.filter(Quests.quest_art == filter_by)
        if sort_dir == 'asc':
            query = query.order_by(Quests.quest_state,Quests.quest_text)
        elif sort_dir == 'desc':
            query = query.order_by(desc(Quests.quest_state),desc(Quests.quest_text))
        return render_template('todo.html',quests=list(query), sort_dir= sort_dir)
    return wrapper


# Nur zum testen: löscht Datenbank, erstellt sie neu und befüllt sie mit 2 beispielwerten
# !!In einem Produktivsystem diesen Block entfernen!!
@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()
    db.session.add(Quests(quest_text='Das Programm entwickeln' ,quest_art='weekquests'))
    db.session.add(Quests(quest_text='Nach Fehlern suchen', quest_state="checked", quest_art='monthquests'))
    db.session.commit()

#Login wird erst später eingerichtet, solange verlinke direkt auf /todo
@app.route('/')
def index():
    return redirect(url_for('todo'))

#Liste alle Aufgaben auf
@app.route('/todo')
@render
@filterable
@sortable
def todo():
    return Quests.query

# ändere quest_status, leite danach zu todo weiter
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method=='POST':
        q_id = request.form['qid']
        Quest = Quests.query.filter(Quests.id==q_id).first()
        if Quest.quest_state == None:
            Quest.quest_state = "checked"
        else:
            Quest.quest_state = None
        db.session.commit()
    return redirect(url_for('todo'))


# lösche empfangenen Datensatz, leite danach zu todo weiter
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method=='POST':
        q_id = request.form['qid']
        Quest = Quests.query.filter(Quests.id==q_id).first()
        db.session.delete(Quest)
        db.session.commit()
    return redirect(url_for('todo'))


# füge empfangene Daten in die Datenbank ein, leite danach zu todo weiter
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        quest_text = request.form['quest_text']
        quest_art = request.form['quest_art']
        if quest_text != '':
            Quest = Quests(quest_text= quest_text, quest_art=quest_art)
            db.session.add(Quest)
            db.session.commit()
    return redirect(url_for('todo'))

#starte Server
if __name__ == '__main__':
    print('Server startet...')
    app.run(port=9999, debug=True, host='0.0.0.0')

