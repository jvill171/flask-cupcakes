"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY']="hidden-cupcakes"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    '''
    Lists all cupcakes and their data
    
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}, ...]}
    '''
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    '''
    Returns a specific cupcake's data, based on ID
    
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    '''
    cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''
    Creates new cupcake & returns data about the cupcake
    
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    '''
    data = request.json
    
    cupcake = Cupcake(
        flavor = data["flavor"],
        size = data["size"],
        rating = data["rating"],
        image = data["image"] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    
    resp_json = jsonify(cupcake=cupcake.serialize())
    return (resp_json, 201)






@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''
    Updates cupcake, but requires all 4 pieces of data to work
    
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    '''

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''
    Deletes cupcake, leaves message like

    Returns JSON like:
        {"message": "Deleted"}
    '''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")