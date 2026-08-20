from flask import Flask, render_template, request, redirect, url_for, flash, session
import nutrition
import food
import re

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.secret_key = "team1FP"

# Temporary "database"
users = {}


# --- ROUTES ---

@app.route('/')
def welcome():
    """Landing Page / Login Page"""
    return render_template("welcome.html")


@app.route('/signup')
def signup():
    """Page for users to create a new account"""
    return render_template("signup.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        session['user'] = username
        # CHECK: If profile doesn't exist, send to account setup, else go to main
        if 'user_profile' not in session:
            return redirect(url_for('account'))
        return redirect(url_for('main'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('welcome'))


@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    password = request.form.get('password')

    # Password validation logic
    if len(password) < 8 or not re.search(r'[!#$%()]', password):
        flash("Password must be at least 8 characters and include one of ! # $ % ( )")
        return redirect(url_for('signup'))

    if username in users:
        flash("Username already exists")
        return redirect(url_for('signup'))

    # Save user and log them in immediately
    users[username] = password
    session['user'] = username

    flash("Account created! Let's set up your profile.")
    # NEW FLOW: Force account setup immediately after signup
    return redirect(url_for('account'))


@app.route('/main')
def main():
    if 'user' not in session:
        return redirect(url_for('welcome'))

    user_profile = session.get('user_profile')
    nutrition_data = session.get('nutrition')

    if not user_profile or not nutrition_data:
        flash("Please complete your profile first.")
        return redirect(url_for('account'))

    return render_template(
        "main.html",
        user=user_profile,
        nutrition=nutrition_data,
        meals=session.get('meals', [])
    )


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/account', methods=['GET', 'POST'])
def account():
    # Load session data
    user = session.get('user_profile', {})
    nutrition_data = session.get('nutrition', {})

    if request.method == 'POST':
        try:
            # Collect form data
            name = request.form['name'].strip()
            sex = request.form['sex'].lower()
            age = int(request.form['age'])
            weight_lb = float(request.form['weight_lb'])
            height_ft = int(request.form['height_ft'])
            height_in = int(request.form['height_in'])
            activity_level = request.form['activity_level']
            goal = request.form['goal']

            # Calculate nutrition
            nutrition_data = nutrition.full_nutrition(
                weight_lb=weight_lb,
                height_ft=height_ft,
                height_in=height_in,
                age=age,
                sex=sex,
                activity_level=activity_level,
                goal=goal,
            )

            # Save to session
            session['user_profile'] = {
                'name': name,
                'sex': sex,
                'age': age,
                'weight_lb': weight_lb,
                'height_ft': height_ft,
                'height_in': height_in,
                'activity_level': activity_level,
                'goal': goal,
            }
            session['nutrition'] = nutrition_data

            flash("Profile saved!")
            return redirect(url_for('main'))

        except Exception as e:
            flash(str(e))

    return render_template(
        "account.html",
        user=user,
        nutrition=nutrition_data,
        activity_options=list(nutrition.ACTIVITY_MULTIPLIERS.keys()),
        goal_options=list(nutrition.GOALS.keys()),
    )


@app.route('/add_meal', methods=['GET', 'POST'])
def add_meal():
    if 'user' not in session:
        return redirect(url_for('welcome'))

    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('food_query', '').strip()
        if query:
            results = food.search_foods(query, limit=20)

    return render_template("add_meal.html", results=results, query=query)


@app.route('/add_meal/save', methods=['POST'])
def save_meal():
    if 'user' not in session:
        return redirect(url_for('welcome'))

    try:
        fdc_id = int(request.form['fdc_id'])
        servings = float(request.form.get('servings', 1))
    except (ValueError, KeyError):
        flash("Invalid food selection.")
        return redirect(url_for('add_meal'))

    f = food.get_food(fdc_id)
    if not f:
        flash("Food not found.")
        return redirect(url_for('add_meal'))

    meals = session.get('meals', [])
    meals.append({
        'name': f['description'],
        'calories': round((f['calories'] or 0) * servings, 1),
        'protein':  round((f['protein_g'] or 0) * servings, 1),
        'carbs':    round((f['carbs_g']   or 0) * servings, 1),
        'fat':      round((f['fat_g']     or 0) * servings, 1),
    })
    session['meals'] = meals
    flash(f"Added {f['description']}")
    return redirect(url_for('main'))


@app.route('/edit_meal/<int:index>', methods=['GET', 'POST'])
def edit_meal(index):
    meals = session.get('meals', [])

    if index < 0 or index >= len(meals):
        return redirect(url_for('meal_history'))

    meal = meals[index]

    if request.method == 'POST':
        meal['name'] = request.form.get('food_name')
        meal['calories'] = request.form.get('calories')
        meal['protein'] = request.form.get('protein')
        meal['carbs'] = request.form.get('carbs')
        meal['fat'] = request.form.get('fat')

        session['meals'] = meals
        return redirect(url_for('meal_history'))

    return render_template("edit_meal.html", meal=meal, index=index)


@app.route('/delete_meal/<int:index>', methods=['POST'])
def delete_meal(index):
    meals = session.get('meals', [])
    if 0 <= index < len(meals):
        meals.pop(index)
        session['meals'] = meals
    return redirect(url_for('meal_history'))


@app.route('/meals_history')
def meals_history():
    flash("Meal history is not implemented yet.")
    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if 'user' not in session:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        goals = {
            'goal_type': request.form.get('goal_type'),
            'calorie_goal': request.form.get('calorie_goal'),
            'protein_goal': request.form.get('protein_goal'),
            'carb_goal': request.form.get('carb_goal'),
            'fat_goal': request.form.get('fat_goal')
        }

        session['goals'] = goals
        flash("Goals updated!")
        return redirect(url_for('main'))

    return render_template("goals.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)