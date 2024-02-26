from flask.views import MethodView
from flask import render_template


class AboutEndpoint(MethodView):
    def get(self):
        return render_template('about.html')

