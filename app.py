from flask import Flask,render_template,request
from werkzeug.utils import redirect 
import model as m
import numpy as np
import joblib
app=Flask(__name__)
xgmodel=joblib.load('xgboostmodel.sav')
def predict_op(s):
    s=m.remove_punctuation_and_stopwords(s)
    wordvec_arrays = np.zeros((1,200)) 
    wordvec_arrays[0,:] = m.word_vector(s, 200)
    return xgmodel.predict(wordvec_arrays)[0]
@app.route("/")
@app.route("/",methods=["POST"])
def hello():
    return render_template("index1.html")
@app.route("/sub1",methods=["POST"])
def submit():
    if request.method=="POST":
        name=request.form["tweetbywords"]
        flag=predict_op(name)
        val=None
        if flag:
            sending="This message contains sensitive content which some users may find offensive"
            val=True
        else:
            sending="This message has no abusive words"
    return render_template("sub1.html",sending=sending,name=name,val=val)
@app.route("/sub2",methods=["POST"])
def submit2():
    if request.method=="POST":
        val=None
        name=request.form["tweetbyURL"]
        sending="This  tweet contains sensitive content which some users may find offensive"
    return render_template("sub2.html",sending=sending)
@app.route("/red")
def returnindex():
    redirect('index1.html')
if __name__=="__main__":
    app.run(debug=True)

