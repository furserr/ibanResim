from flask import Flask
from flask import request,redirect,render_template,url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import ImageFilter
from PIL import Image
import cv2

import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except Exception as e:
    pass

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/',methods=['POST',])
def submitImage():
    image = request.files['ocrImage']
    text = ''
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = c2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thresh)
    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
    f.write(text)
    f.close()
    return render_template('textFile.html',text=text,filename=f)


if __name__ == '__main__':
    app.run()
