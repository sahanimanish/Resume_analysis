from flask import Flask,request,redirect
from flask import render_template
from main import get_prediction

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict",methods = ['GET', 'POST'])
def get_result():
    data=request.form
    f = request.files['resume']
    f.save(f.filename)
    pred=get_prediction(f.filename,data)
    return render_template('rec.html',data=pred)
if __name__ == '__main__':
    app.run(debug=True)
