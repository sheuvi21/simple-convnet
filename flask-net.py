from flask import Flask
from flask import request, render_template, url_for, jsonify, abort
from flask_wtf.csrf import CSRFProtect
from tools.image import preprocess_image
from tools.model import predict
from rq import Queue
from worker import conn
from settings import LABELS, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

csrf = CSRFProtect(app)

q = Queue(connection=conn)


@app.route('/')
def main():
    return render_template('main.html', labels=LABELS)


@app.route('/process/', methods=['POST'])
def do_predict():
    if 'image' in request.files:
        im = preprocess_image(request.files['image'].stream)
        job = q.enqueue(predict, im)
        return jsonify(ok=True, get_url=url_for('get_result', job_id=job.id))
    else:
        abort(406)  # Not Acceptable


@app.route('/result/<job_id>/')
def get_result(job_id):
    job = q.fetch_job(job_id)
    predictions = job.result
    if predictions is None:
        return jsonify(ok=False)
    else:
        predictions = zip(LABELS, predictions.tolist())
        predictions = [{
            'label': label,
            'prediction': prediction
        } for label, prediction in predictions]
        return jsonify(ok=True, result=predictions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
