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

    def get_status(self):
        if request.method == 'POST':
            status = self._lptender_model.getCurrentState()
            resp = make_response('{"response": "ok", "status": "' + status + '"}')
            resp.headers['Content-Type'] = "application/json"
            return resp


if __name__ == '__main__':
    app = Flask(__name__)

    lptender_impl = LPTenderImplMock.LpTenderMock()
    lptender_model = LPTenderModel.LpTenderStateMachine(lptender_impl)

    LPTenderWebView.register(app, init_argument=lptender_model)
    app.run()