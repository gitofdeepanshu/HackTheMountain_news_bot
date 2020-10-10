from flask import Flask, request, abort, jsonify

from sem_matching import predict

app = Flask(__name__)
# app.config["Debug"] = True

@app.route("/find_news", methods=['GET', 'POST'])
def find_news():
    print(request.data)
    if request.method == 'POST':
        if not request.json or not 'data' in request.json:
            abort(400)
        return jsonify({'url': predict(request.json['data'])})
    else:
        return 'send POST with json, {"data": YOUR DATA HERE}'

# import threading
# threading.Thread(target=app.run, kwargs={'host':'0.0.0.0','port':80}).start()
