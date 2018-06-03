from flask import Flask
from flask import request, render_template, url_for, jsonify, abort
from flask_wtf.csrf import CSRFProtect
from tools.image import preprocess_image
from tools.model import predict, get_labels
from rq import Queue
from run_worker import conn
from settings import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

csrf = CSRFProtect(app)

q = Queue(connection=conn)


@app.route('/')
def main():
    labels = get_labels()
    return render_template('main.html', labels=labels)


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
        labels = get_labels()
        predictions = zip(labels, predictions.tolist())
        predictions = [{
            'label': label,
            'prediction': prediction
        } for label, prediction in predictions]
        return jsonify(ok=True, result=predictions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
