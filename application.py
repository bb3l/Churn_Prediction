from flask import Flask, escape, request, render_template
import pandas as pd
import joblib

application = Flask(__name__)





@application.route('/')
@application.route('/about')
def about():

    return render_template("about.html")

@application.route('/CustomerChurnPredictor')
def CustomerChurnPredictor():

    return render_template("CustomerChurnPredictor.html")

def preprocessDataAndPredict(CreditScore, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary):
    # keep all inputs in array
    data = [CreditScore, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary ]

    # Create Data Frame
    data = pd.DataFrame({'CreditScore': [CreditScore], 'Gender': [Gender],
     'Age': [Age], 'Tenure': [Tenure], 'Balance': [Balance],
     'NumOfProducts': [NumOfProducts], 'HasCrCard': [HasCrCard], 'IsActiveMember': [IsActiveMember], 
     'EstimatedSalary': [EstimatedSalary]})

    # open file
    file = open("finalmodel.pkl", "rb")

    # load trained model
    trained_model = joblib.load(file)

    # predict
    prediction = trained_model.predict(data)

    return round(prediction[0], 0)

@application.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        # get form data
        CreditScore = request.form.get('CreditScore')
        Gender = request.form.get('Gender')
        Age = request.form.get('Age')
        Tenure = request.form.get('Tenure')
        Balance = request.form.get('Balance')
        NumOfProducts = request.form.get('NumOfProducts')
        HasCrCard = request.form.get('HasCrCard')
        IsActiveMember = request.form.get('IsActiveMember')
        EstimatedSalary = request.form.get('EstimatedSalary')

        # call preprocessDataAndPredict and pass inputs
        try:
            prediction = preprocessDataAndPredict(CreditScore, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
            
            if prediction==0:
                predict_result= "not churn"
            else:
                predict_result= "churn"
            # pass prediction to template
            return render_template('predict.html', prediction=predict_result)

        except ValueError:
            return "Please Enter valid values"

        pass
    pass

# Run Flask app
if __name__ == '__main__':
     application.run()