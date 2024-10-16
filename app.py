from flask import Flask, request, render_template, jsonify
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to the Student Performance Predictor. Go to /predictdata to make predictions."


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )
        pred_df = data.get_data_as_data_frame()
        print(pred_df)
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        return jsonify({'result': round(float(results[0]), 2)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
