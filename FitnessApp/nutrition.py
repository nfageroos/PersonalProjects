# Calculate BMI and Categories
def calc_bmi(weight_lb, height_in):
    if height_in <= 0:
        raise ValueError("Height must be greater than 0")
    bmi = (weight_lb / (height_in ** 2)) * 703
    return round(bmi, 2)

def convert_height(height_ft, height_in):
    return (height_ft * 12) + height_in

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi <25.0:
        return "Normal Weight"
    elif bmi <30.0:
        return "Overweight"
    else:
        return "Obese"


# Calculate BMR (Base Metabolic Rate)
def calc_bmr(weight_lb, height_in, age, sex):
    weight_kg = weight_lb * 0.453592
    height_cm = height_in * 2.54

    if sex.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    elif sex.lower() == "female":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        raise ValueError("Sex must be either 'male' or 'female'")
    return round(bmr, 2)


# Total Daily Exercise Expenditure (TDEE) and calculation.
ACTIVITY_MULTIPLIERS = {
    'Sedentary': 1.2,           # little to no exercise
    'Lightly active': 1.375,    # light exercise 1-3 days/week
    'Moderately active': 1.55,  # moderate exercise 3-5 days/week
    'Very active': 1.725,       # hard exercise 6-7 days/week
    'Extremely active': 1.9,    # very hard exercise / physical job
}

def calc_tdee(bmr, activity_level):
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level)
    if multiplier is None:
        raise ValueError("Invalid Activity Level. Choose from: " + str(list(ACTIVITY_MULTIPLIERS.keys())))
    return round(bmr * multiplier, 2)


# Calorie Goals
GOALS= {
    "Lose": -500,   # ~1 lb/week deficit
    "Maintain": 0,
    "Gain": +300    # lean bulk surplus
}

def calorie_goal(tdee, goal):
    adjustment = GOALS.get(goal)
    if adjustment is None:
        raise ValueError("Invalid Goal Level. Choose from: " + str(list(GOALS.keys())))
    return max(round(tdee + adjustment, 1), 1200) # Lowest 1200 kcal


# Macro Breakdown (Protein/Carbs/Fats (% of calories))
def calc_macros(calorie_target, goal):
    splits = {
        "lose": (0.40, 0.30, 0.30),
        "maintain": (0.30, 0.45, 0.25),
        "gain": (0.35, 0.45, 0.20)
    }

    protein, carbs, fats = splits.get(goal.lower(), (0.30, 0.45, 0.25))

    # Protein and Carbs = 4 kcal/g, Fats = 9 kcal/g
    return {
        "protein_g": round((calorie_target * protein) / 4, 1),
        "carb_g": round((calorie_target * carbs) / 4, 1),
        "fat_g": round((calorie_target * fats) / 9, 1),
    }

# Add up nutrition total from food.py
def calculate_meal_total(food_items):
    totals = {
        "calories": 0,
        "protein_g": 0,
        "fat_g": 0,
        "carb_g": 0
    }

    for food in food_items:
        totals["calories"] += food.get("calories") or 0
        totals["protein_g"] += food.get("protein_g") or 0
        totals["fat_g"] += food.get("fat_g") or 0
        totals["carb_g"] += food.get("carb_g") or 0

        for key in totals:
            totals[key] += round(food.get[key], 2)
        return totals


# Full profile wrapped up
def full_nutrition(weight_lb, height_ft, height_in, age, sex, activity_level, goal):
    height_inches = convert_height(height_ft, height_in)
    bmi = calc_bmi(weight_lb, height_inches)
    bmr = calc_bmr(weight_lb, height_inches, age, sex)
    tdee = calc_tdee(bmr, activity_level)
    cals = calorie_goal(tdee, goal)
    macros = calc_macros(cals, goal)

    return {
        "bmi": bmi,
        "bmi_category": bmi_category(bmi),
        "bmr": bmr,
        "tdee": tdee,
        "calorie_goal": cals,
        "protein_g": macros["protein_g"],
        "carb_g": macros["carb_g"],
        "fat_g": macros["fat_g"]

    }

# Testing
# if __name__ == "__main__":
#     sex = input("Sex: (Male/Female): ").lower()
#     age = int(input("Age (in years): "))
#     weight_lb = float(input("Weight (lb): "))
#     height_ft = int(input("Height (in feet): "))
#     height_in = int(input("Height (in inches): "))
#     print("Activity Levels: Sedentary, Lightly_Active, Moderately_Active, Very_Active, Extremely_Active")
#     activity_level = input("Activity level: ").lower()
#     goal = input("Goal to (Lose, Maintain, Gain) Weight: ").lower()
#
#     results = full_nutrition(weight_lb, height_ft, height_in, age, sex, activity_level, goal)
#
#     print()
#     print(f"  bmi:          {results['bmi']} ({results['bmi_category']})")
#     print(f"  bmr:          {results['bmr']} calories/day at rest")
#     print(f"  tdee:         {results['tdee']} calories/day maintenance")
#     print(f"  calorie goal: {results['calorie_goal']} calories/day")
#     print(f"  protein:      {results['protein_g']}g")
#     print(f"  carbs:        {results['carb_g']}g")
#     print(f"  fats:          {results['fat_g']}g")