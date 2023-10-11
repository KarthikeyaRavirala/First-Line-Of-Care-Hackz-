from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)
import openai
from googletrans import Translator

import elevenlabs


def translate_to_telugu_or_hindi(text, target_language):

    try:
        translator = Translator()
        translated_text = translator.translate(text,dest=target_language)
        return translated_text.text
    except Exception as e:
        return str(e)


# Load the data set
data = pd.read_csv('combined_childhood_illnesses_and_injuries.csv')

# Define a function to predict the output
# def predict_output(disease, age_group, severity):
#   # Filter the data set based on the input parameters
#   datares = (data['Disease']== disease)
#   print(datares)
#   datares = (datares['Age'] == age_group)
#   datares = ((data['Severity'] == severity)['Severity'] == severity)


#   # Get the output recommendations
#   output_recommendations = (data['Severity'] == severity)['Output Recommendations']
#   print('444444444444444444444')
#   print(output_recommendations)
#   print('444444444444444444444')


#   return output_recommendationss


def predict_output(disease, age_group, severity):
  # Check if the input parameters are valid
  if disease not in data['Disease'].unique():
    raise ValueError('Invalid disease')
  if age_group not in data['Age'].unique():
    raise ValueError('Invalid age group')
  if severity not in data['Severity'].unique():
    raise ValueError('Invalid severity')

  # Filter the data set based on the input parameters
  filtered_data = data[(data['Disease'] == disease) & (data['Age'] == age_group) & (data['Severity'] == severity)]

  # If there are no rows in the filtered data set, return an empty string
  if len(filtered_data) == 0:
    return ''

  # Get the output recommendations
  output_recommendations = filtered_data['Output Recommendations'].values[0]
  PossibleCauses = filtered_data['Possible Causes'].values[0]
  WaystoPrevent = filtered_data['Ways to Prevent'].values[0]
  WaystoTreat = filtered_data['Ways to Treat'].values[0]
  return output_recommendations , PossibleCauses , WaystoPrevent , WaystoTreat


# Define a route to render the main page
@app.route('/')
def index():
  

  return render_template('index.html')
@app.route('/pre')
def index1():
  # Get the list of diseases
  diseases = data['Disease'].unique()

  # Get the list of age groups
  age_groups = data['Age'].unique()

  # Get the list of severities
  severities = data['Severity'].unique()

  return render_template('predict1.html', diseases=diseases, age_groups=age_groups, severities=severities)
# Define a route to predict the output
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input parameters
    disease = request.form['disease']
    age_group = request.form['age_group']
    severity = request.form['severity']
    genri = request.form['genri']
    lang = ''
    

    # Predict the output
    output_recommendations  , PossibleCauses , WaystoPrevent , WaystoTreat = predict_output(disease, age_group, severity)

    if genri == 'yes':
        api_key = "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"
        openai.api_key = api_key
        prompt = f"based up on the following data give the parent a genrilised report explaining in detail in a lamen language disease : {disease}, Severity: {severity} , age_group:{age_group}, recommendations:{output_recommendations} , PossibleCauses:{PossibleCauses},WaystoPrevent:{WaystoPrevent},WaystoTreat{WaystoTreat}"
        response = response = openai.ChatCompletion.create( model="gpt-3.5-turbo",messages=[{"role": "system", "content": "You are a helpful assistant that generates reports."}, {"role": "user", "content": prompt}],temperature=0,max_tokens=256)
        response = response.choices[0].message["content"]
    else:response = ''
     
    #  response.choices[0].text
    if lang == 'Telugu':
        output_recommendations  , PossibleCauses , WaystoPrevent , WaystoTreat = predict_output(disease, age_group, severity)

        output_recommendations = translate_to_telugu_or_hindi(output_recommendations,'te')
        PossibleCauses = translate_to_telugu_or_hindi(PossibleCauses,'te')
        WaystoPrevent = translate_to_telugu_or_hindi(WaystoPrevent,'te')
        WaystoTreat = translate_to_telugu_or_hindi(WaystoTreat,'te')
        

        return render_template('telugu.html', output_recommendations=output_recommendations , PossibleCauses=PossibleCauses ,WaystoPrevent=WaystoPrevent,WaystoTreat=WaystoTreat,report=response)



#   return render_template('predict.html', output_recommendations=output_recommendations , PossibleCauses=PossibleCauses ,WaystoPrevent=WaystoPrevent,WaystoTreat=WaystoTreat )
    return render_template('report.html', output_recommendations=output_recommendations , PossibleCauses=PossibleCauses ,WaystoPrevent=WaystoPrevent,WaystoTreat=WaystoTreat,report=response)


# Start the Flask app
if __name__ == '__main__':
  app.run(debug=True)