from flask import Flask,render_template,request,redirect,url_for
import main as an
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/analysis',methods=['POST','GET'])
def analysis():
    tempCV = request.files['cv']
    tempCV.save('tempCV.pdf')
    
    
    # lines =[line.decode('utf-8') for line in uploadedCV]
    # print(lines)
    return 'hello world'
    # cvsText = an.cleaner(an.pdfReader(cvs))
    # jobText = an.cleaner(an.pdfReader(job))

if __name__ == '__main__':
    app.run(debug=True)