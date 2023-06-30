import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib

app = Flask(__name__)
model =  joblib.load('HFailure.pkl', 'r+')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    selected_gender = request.form.get('Sex')
    gender_options = {
        'Female': '0',
        'Male': '0',
    }
    gender_options[selected_gender] = '1'
   
    selected_chestpain = request.form.get('chest_pain')
    chestpain_options = {
        'ASV': '0',
        'ATA': '0',
        'NAP': '0', 
        'TA': '0'
    }
    chestpain_options[selected_chestpain] = '1'
    
    selected_restingECG = request.form.get('resting_ecg')
    restingECG_options = {
        "LVH":"0",
        "Normal":"0",
        "ST":"0"
    }
    restingECG_options[selected_restingECG] = '1'
   

    selected_ExerciseAngina = request.form.get('exercise_angina')
    ExerciseAngina_options = {
        'No': '0',
        'Yes': '0',
    }
    ExerciseAngina_options[selected_ExerciseAngina] = '1'



    selected_st_slope= request.form.get('st_slope')
    st_slope_options = {
        'Down': '0',
        'Flat': '0',
        'Up': '0',
        
    }
    st_slope_options[selected_st_slope] = '1'
    
    
    catgorised_list = list(gender_options.values())   + list(chestpain_options.values())  + list(restingECG_options.values()) +list(ExerciseAngina_options.values())  + list(st_slope_options.values())
    print(catgorised_list)
    input_list = []
    for value in request.form.values():
        try:
            if isinstance(int(value), int):
                catgorised_list.append(int(value))
        except ValueError:
            pass

    int_features = input_list + catgorised_list
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    print(output)
    if output == 0:
        output = "This patient does not have heart diseases"
    else:
        output =  "This patient has heart diseases"
    return render_template('index.html', prediction_text=output)

@app.route('/results',methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)