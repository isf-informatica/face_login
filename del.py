from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('del.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    data = request.get_json()
    photo_data = data['photo']
    
    # Process the photo_data (e.g., save it to a file, perform image analysis, etc.)
    # For simplicity, let's just print the length of the received data as an example
    print("Received photo with {} bytes.".format(len(photo_data)))

    return "Photo received successfully."

if __name__ == '__main__':
    app.run(debug=True)
