from flask import Flask,render_template
import main

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/analysis',methods=['POST','GET'])
def analysis():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)