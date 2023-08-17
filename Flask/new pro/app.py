from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import tensorflow as tf
from twilio.rest import Client

app = Flask(__name__)
model = tf.keras.models.load_model('Missing.h5')
name = ["Found Missing", "Normal"]

# Twilio credentials
account_sid = 'AC23079f1f58727c6b64054648096a1b05'
auth_token = 'a44b9e933a9a9d34ca3037e4ac919441 '
twilio_phone_number = '+12184299494'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    img = Image.open(image)
    img = img.resize((64, 64))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)
    pred_class = np.argmax(pred, axis=1)[0]
    result = name[pred_class]

    # Send SMS if the predicted class is "Found Missing"
    sms_status=""
    if pred_class == 0:
        send_sms("Found the person at Gudiwada")
        sms_status="SMS Sent"
        
    return render_template('result.html', result=result, sms_status=sms_status)

def send_sms(message_body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+91 7997938999",  # Replace with the recipient's phone number
        from_=twilio_phone_number,
        body=message_body
    )
    print(message.sid)
    print("SMS Sent")

if __name__ == '__main__':
    app.run(debug=False, port=2010)
