from flask import Flask, request, render_template, jsonify
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


application = Flask(__name__)

app = application

@app.route('/')
def index():
    return "Welcome to the Student Performance Predictor. Go to /predictdata to make predictions."


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if request.is_json:
            data = request.json
        else:
            data = request.form

        custom_data = CustomData(
            gender=data.get('gender'),
            race_ethnicity=data.get('race_ethnicity'),
            parental_level_of_education=data.get('parental_level_of_education'),
            lunch=data.get('lunch'),
            test_preparation_course=data.get('test_preparation_course'),
            reading_score=float(data.get('reading_score')),
            writing_score=float(data.get('writing_score'))
        )
        pred_df = custom_data.get_data_as_data_frame()
        print(pred_df)
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        return jsonify({'result': round(float(results[0]), 2)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
