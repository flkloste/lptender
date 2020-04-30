from flask import Flask, render_template, request, make_response
from flask_classful import FlaskView
import LPTenderImplMock
import LPTenderModel

class LPTenderWebView(FlaskView):
    route_base = '/'
    default_methods = ['GET', 'POST']

    def __init__(self, lptender_model):
        self._lptender_model = lptender_model

    def index(self):
        return render_template('index.html');

    def play(self):
        if request.method == 'POST':
            self._lptender_model.play()
            resp = make_response('{"response": "ok"}')
            resp.headers['Content-Type'] = "application/json"
            return resp

    def stop(self):
        if request.method == 'POST':
            self._lptender_model.stop()
            resp = make_response('{"response": "ok"}')
            resp.headers['Content-Type'] = "application/json"
            return resp

    def flip(self):
        if request.method == 'POST':
            self._lptender_model.flip()
            resp = make_response('{"response": "ok"}')
            resp.headers['Content-Type'] = "application/json"
            return resp

    def get_status(self):
        if request.method == 'POST':
            status = self._lptender_model.getCurrentState()
            resp = make_response('{"response": "ok", "status": "' + status + '", "autoflip": "' + str(self._lptender_model.autoFlip) + '" }')
            resp.headers['Content-Type'] = "application/json"
            return resp

    def set_autoflip(self):
        if request.method == 'POST':
            autoflip_value = request.form['autoflip']
            self._lptender_model.autoFlip = (autoflip_value == 'true')
            resp = make_response('{"response": "ok"}')
            resp.headers['Content-Type'] = "application/json"
            return resp

    def emergency_shutdown(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def init(self):
        if request.method == 'POST':
            self._lptender_model.init()
            resp = make_response('{"response": "ok"}')
            resp.headers['Content-Type'] = "application/json"
            return resp

if __name__ == '__main__':
    app = Flask(__name__)

    lptender_impl = LPTenderImplMock.LpTenderMock()
    lptender_model = LPTenderModel.LpTenderStateMachine(lptender_impl)

    LPTenderWebView.register(app, init_argument=lptender_model)
    app.run(host='0.0.0.0')