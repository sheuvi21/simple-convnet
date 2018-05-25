from flask import Flask
from flask import request, render_template, url_for, redirect
from image import preprocess_image
from model import predict
from rq import Queue
from worker import conn

LABELS = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' and 'image' in request.files:
        im = preprocess_image(request.files['image'].stream)
        q = Queue(connection=conn)
        job = q.enqueue(predict, im)
        return redirect(url_for('get_result', job_id=job.id))
    else:
        return render_template('main.html')


@app.route('/result/<job_id>/')
def get_result(job_id):
    q = Queue(connection=conn)
    job = q.fetch_job(job_id)
    predictions = job.result
    if predictions is None:
        return render_template('loading.html')
    else:
        predictions *= 100
        return render_template('result.html', labels=LABELS, predictions=predictions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
