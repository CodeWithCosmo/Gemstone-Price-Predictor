import sys
from flask import Flask,request,render_template
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline
from src.pipelines.training_pipeline import TrainPipeline
from src.logger import logging 
from src.exception import CustomException


application=Flask(__name__)

app=application

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/train")
def train():
    try:
        score = TrainPipeline().initiate_train_pipeline()

        return render_template("train.html",text = f"Accuracy of the model is {round(score,2)}")

    except Exception as e:
        raise CustomException(e,sys)

@app.route("/predict",methods=['GET','POST'])
def predict():
    if request.method=='GET':
        return render_template('form.html')
    else:
        try:
            data=CustomData(
                carat=float(request.form.get('carat')),
                depth = float(request.form.get('depth')),
                table = float(request.form.get('table')),
                cut = request.form.get('cut'),
                color= request.form.get('color'),
                clarity = request.form.get('clarity')
            )
            final_new_data=data.get_data_as_dataframe()
            predict_pipeline=PredictPipeline()
            pred=predict_pipeline.predict(final_new_data)

            result=round(pred[0],2)

            return render_template('form.html',prediction_text=f'The predicted price is {result}')
        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)
    

if __name__=="__main__":
    app.run(debug=True)