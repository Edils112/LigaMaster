from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://edils:1021669825Sm@sergio-prueba.database.windows.net/FUTBOL-DB?driver=ODBC+Driver+17+for+SQL+Server'
)

db = SQLAlchemy(app)

class Equipo(db.Model):
    __tablename__ = 'Equipos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    entrenador = db.Column(db.String(100))
    estadio = db.Column(db.String(100))
    titulos = db.Column(db.Integer)

@app.route('/')
def index():
    equipos = Equipo.query.all()
    return render_template('index.html', equipos=equipos)

@app.route('/crear', methods=['GET', 'POST'])
def crear():

    if request.method == 'POST':

        nuevo = Equipo(
            nombre=request.form['nombre'],
            ciudad=request.form['ciudad'],
            entrenador=request.form['entrenador'],
            estadio=request.form['estadio'],
            titulos=request.form['titulos']
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect('/')

    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    equipo = Equipo.query.get(id)

    if request.method == 'POST':

        equipo.nombre = request.form['nombre']
        equipo.ciudad = request.form['ciudad']
        equipo.entrenador = request.form['entrenador']
        equipo.estadio = request.form['estadio']
        equipo.titulos = request.form['titulos']

        db.session.commit()

        return redirect('/')

    return render_template('editar.html', equipo=equipo)

@app.route('/eliminar/<int:id>')
def eliminar(id):

    equipo = Equipo.query.get(id)

    db.session.delete(equipo)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)