import joblib
from flask import Flask
from flask import redirect, url_for
from flask import render_template
from flask import request
import pandas as pd


# Load the trained model.
# The deployment_dict maps user inputs from the variables
# 'customer_type', 'class_of_travel', and 'type_of_travel'
# to their corresponding numeric representations used during model training.
# age_group_dict maps user ages
# to specific labels (used during model training) that correspond to predefined age ranges.

model_file = 'flask_airline_best_model_26.08.2023.bin'

try:
    with open(model_file, 'rb') as f_in:
        deployment_dict, age_group_dict, model = joblib.load(f_in)
except FileNotFoundError:
    print(f"Model file '{model_file}' not found. Make sure the file is in the correct location.")

# Defining the Flask application.
app = Flask('airline_passenger_satisfaction')

@app.route('/')
def main_page():
    # Get error message, if present
    error_message = request.args.get('error')
    print(error_message)
    return render_template('/main_page.html', error_message=error_message)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        passenger_dict = request.form.to_dict()
        
        # Validate input values
        if not validate_input(passenger_dict):
            error_message = "Invalid input. Please provide valid values."
            return redirect(url_for('main_page', error=error_message))

        # Preprocesses the input dictionary into a model-ready DataFrame.
        preprocessed_passenger_df = preprocess_data(passenger_dict)
      
        try:
            result = model.predict(preprocessed_passenger_df)
            return render_template('/predict_page.html', prediction = result)
   
        except ValueError:
            return "Please Enter valid values"

# Validate user inputs       

def validate_input(dictionary):
    # Check if required keys are in the dictionary
    keys_to_check = {'customer_type', 'type_of_travel', 'class_of_travel', 'age'}
    if not keys_to_check.issubset(dictionary.keys()):
        return False
    
    try:
        # Check if values under the required keys are one of the relevant variants
        customer_type_bool = dictionary['customer_type'] in ['Loyal customer', 'Disloyal customer']
        travel_type_bool = dictionary['type_of_travel'] in ['Business travel', 'Personal travel']
        travel_class_bool = dictionary['class_of_travel'] in ['Business', 'Eco', 'Eco plus']
        if not (customer_type_bool and travel_type_bool and travel_class_bool):
            return False

        # Check age
        age = dictionary['age']
        if not age.isdigit() or int(age) not in range(0, 100):
            return False
        
        # Check other numeric values
        for key, value in dictionary.items():
            if key not in keys_to_check:
                if not value.isdigit() or int(value) not in range(0, 6):
                    return False
    except AttributeError:
        return False

    return True

# Preprocesses the input dictionary by mapping categorical variables,
# creating two new variables, from existing ones: 
# xor_customer_travel and age_group,
# reordering columns, and
# turning string input into float.
# Input: dictionary containing passenger information.
# Returns: preprocessed DataFrame ready for model prediction.

def preprocess_data(dictionary):
    # Map categorical variables to their numeric representations.
    for key in dictionary:
        if dictionary[key] in deployment_dict:
            dictionary[key] = deployment_dict[dictionary[key]]
    
    # Create xor_customer_travel variable and add it to dictionary
    xor_customer_travel = dictionary['customer_type'] ^ dictionary['type_of_travel']
    dictionary['xor_customer_travel'] = xor_customer_travel
    
    # Turn passenger's age into age_group and add it to dictionary
    age_group = age_to_age_group(int(dictionary['age']))
    dictionary['age_groups'] = age_group
    
    # Reorder columns.
    ordered_passenger_dict = reorder_dict(dictionary)
    
    # Transform dictionary into DataFrame.
    passenger_df = pd.json_normalize(ordered_passenger_dict)
    
    # Convert string input to float.
    passenger_df = passenger_df.astype(float)
    
    return passenger_df

# Turn passenger's age to age_group,
# as the model was trained with 'Age_groups' feature
# and without 'Age' feature.
# Input: passenger's age.
# Returns: specific number for the age_group.

def age_to_age_group(passenger_age):
    for age in age_group_dict.items():
        min_age = age[0][0]
        max_age = age[0][1]
        if min_age < passenger_age < max_age:
            return age[1]
        

# Order the input dictionary according to the required column order for the LightGBM model,
# as the last one is sensitive to the order of columns.
# Input: dictionary containing passenger information.
# Returns: the same dictionary with reordered columns.

def reorder_dict(dictionary):
    column_order = ['type_of_travel', 'inflight_wifi_service', 'gate_location',
                    'online_boarding', 'seat_comfort', 'inflight_entertainment',
                    'onboard_service', 'baggage_handling', 'checkin_service', 'inflight_service',
                    'cleanliness', 'class_of_travel', 'age_groups', 'xor_customer_travel']
    reordered_dict = {
        key: dictionary.get(key, '0') for key in column_order
    }
    
    return reordered_dict

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
