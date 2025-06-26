from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "recipes.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    query = request.args.get('q', '')  # Get search query
    if query:
        recipes = Recipe.query.filter(
            (Recipe.title.ilike(f'%{query}%')) | 
            (Recipe.ingredients.ilike(f'%{query}%'))
        ).all()
    else:
        recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image_url = request.form.get('image_url')
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_url=image_url)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        recipe.image_url = request.form.get('image_url')
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', recipe=recipe)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
