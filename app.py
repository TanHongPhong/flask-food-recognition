from flask import Flask, render_template, request, url_for
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Thư mục chứa ảnh upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load mô hình và menu
model = tf.keras.models.load_model(r'D:\DELL\GAME\THI_AI\fic_tuned.h5')
with open(r'D:\DELL\GAME\THI_AI\menu.json', 'r') as f:
    menu = json.load(f)
class_names = list(menu.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return render_template('index.html', error='Không có ảnh được chọn.')

    image = request.files['image']
    if image.filename == '':
        return render_template('index.html', error='Chưa chọn ảnh.')

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Tiền xử lý ảnh
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    # Dự đoán
    preds = model.predict(img_array)
    class_id = np.argmax(preds[0])
    label = class_names[class_id]
    price = menu.get(label, 0)

    # Trả về URL ảnh để hiển thị
    image_url = url_for('static', filename='uploads/' + filename)

    return render_template('index.html',
                           image_path=image_url,
                           label=label,
                           price=price)

if __name__ == '__main__':
    app.run(debug=True)
