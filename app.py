import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

model =  joblib.load('HFailure.pkl', 'r+')
modelHeart = joblib.load('HFailure_death.pkl', 'r+')

class PredictHeartFailue(Resource):
  def post(self):
    try:
        selected_gender = request.json['sex']
        gender_options = {
            'female': 0,
            'male': 0,
        }
        gender_options[selected_gender] = 1
    
        selected_chestpain = request.json['chest_pain_type']
        chestpain_options = {
            'ASV': 0,
            'ATA': 0,
            'NAP': 0, 
            'TA': 0
        }
        chestpain_options[selected_chestpain] = 1
        
        selected_restingECG = request.json['resting_ecg']
        restingECG_options = {
            "LVH":0,
            "normal":0,
            "ST":0
        }
        restingECG_options[selected_restingECG] = 1
    

        selected_ExerciseAngina = request.json['exercise_angina']
        ExerciseAngina_options = {
            'no': 0,
            'yes': 0,
        }
        ExerciseAngina_options[selected_ExerciseAngina] = 1



        selected_st_slope= request.json['st_slope']
        st_slope_options = {
            'down': 0,
            'flat': 0,
            'up': 0,
            
        }
        st_slope_options[selected_st_slope] = 1

        catgorised_list = list(gender_options.values())   + list(chestpain_options.values())  + list(restingECG_options.values()) +list(ExerciseAngina_options.values())  + list(st_slope_options.values())
        input_list = []
        for value in request.json.values():
            try:
                if isinstance(int(value), int):
                    input_list.append(int(value))
            except ValueError:
                pass
        
        int_features = input_list + catgorised_list
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        output = round(prediction[0], 2)
        
        if output == 0:
            output = "You have no heart failure"
        else:
            output =  "You have heart failure"
        return output
    except:
        return "error", 500

class PredictDeath(Resource):
  def post(self):
    try:
        input_list = list(request.json.values())
        
        final_features =[np.array(input_list)]
        
        prediction = modelHeart.predict(final_features)
        probability = modelHeart.predict_proba(final_features)
        proba = round(sorted(probability[0])[1], 2)
        output = round(prediction[0], 2)
        if output == 0:
            output = "There is a" + str(proba) + "the patient will die of Heart failure"
        else:
            output =  "There is a" + str(proba) + "the patient will die not of Heart failure"
        return output
    except Exception as e:
        print(e)
        return "error", 500


class PredictSubtype(Resource):
  def post(self):
    try:
        E_F= request.json['ejection_fraction']
        if E_F >= 70:
            return 'Hyperdynamic'
        elif E_F < 70 and E_F >= 55:
            return 'Normal'
        elif E_F < 55 and E_F >= 45:
            return 'Mildly Reduced'
        elif E_F < 45 and E_F >= 30:
            return 'Moderately Reduced'
        elif E_F < 30:
            return 'Severely Reduced'
    except:
        return "error", 500

   

api.add_resource(PredictHeartFailue, '/diagnosis/')
api.add_resource(PredictDeath, '/severity/')
api.add_resource(PredictSubtype, '/subtype/')



if __name__ == "__main__":
    app.run(debug=True)