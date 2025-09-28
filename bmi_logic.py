
def calculate_bmi(weight, height):
    """Calculates BMI given weight in kg and height in meters."""
    if height <= 0:
        return None
    return round(weight / (height ** 2), 2)

def classify_bmi(bmi):
    """Classifies BMI into standard categories."""
    if bmi is None:
        return "Invalid input"
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"
