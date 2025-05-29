from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    # Accepts a string, but does not use it, just returns 'hello'
    print(data)
    return jsonify({'message': str(data)+'hello'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 