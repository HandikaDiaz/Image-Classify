import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.secret_key = 'SECRETKEY'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    model = load_model('model.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model not found: {e!r}")
    exit(1)

CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
            'dog', 'frog', 'horse', 'ship', 'truck']

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path, target_size=(32, 32)):
    """Preprocess image untuk model CNN"""
    try:
        # Baca gambar
        img = Image.open(img_path)
        
        # Konversi ke RGB jika perlu
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize gambar
        img = img.resize(target_size)
        
        # Konversi ke array dan normalisasi
        img_array = np.array(img) / 255.0
        
        # Tambahkan batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    print("Predict route called with method:", request.method)
    print("Form data:", request.form)
    print("Files:", request.files)
    
    if 'file' not in request.files:
        flash('No file selected')
        print("No file in request.files")
        return redirect(url_for('index'))
    
    file = request.files['file']
    print("File object:", file)
    print("File filename:", file.filename)
    
    if file.filename == '':
        flash('No file selected')
        print("Empty filename")
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file to: {filepath}")
            file.save(filepath)
            
            if not os.path.exists(filepath):
                flash('Error saving file')
                return redirect(url_for('index'))
                
            print("File saved successfully")
            print("Using real model for prediction")
            processed_image = preprocess_image(filepath)
            
            if processed_image is not None:
                predictions = model.predict(processed_image)
                predicted_class = np.argmax(predictions[0])
                confidence = np.max(predictions[0])
                
                # Dapatkan nama kelas
                if predicted_class < len(CLASS_NAMES):
                    class_name = CLASS_NAMES[predicted_class]
                else:
                    class_name = f"Class {predicted_class}"
                print(f"Prediction: {class_name} with confidence {confidence:.2f}")
            else:
                flash('Error processing image')
                return redirect(url_for('index'))
            
            return render_template('result.html', 
                                filename=filename,
                                prediction=class_name,
                                confidence=f"{confidence:.2%}")
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    app = app