from flask import Flask

from api.home import HomeEndpoint
from api.about import AboutEndpoint
from api.signout import SignOutEndpoint
from api.signup import SignUpEndpoint
from api.signin import SignInEndpoint
from api.userpage import UserpageEndpoint
from api.showcase import ShowcaseEndpoint
from api.stylize import StylizeEndpoint
from api.styling_result import StylingResultEndpoint

import os


template_abs_path_directory = os.path.abspath('src/templates')
static_abs_path_directory = os.path.abspath('static')

app = Flask(
    __name__, 
    template_folder=template_abs_path_directory,
    static_folder=static_abs_path_directory
)

app.add_url_rule('/', view_func=HomeEndpoint.as_view('home'))
app.add_url_rule('/about', view_func=AboutEndpoint.as_view('about'))
app.add_url_rule('/signin', view_func=SignInEndpoint.as_view('signin'))
app.add_url_rule('/signup', view_func=SignUpEndpoint.as_view('signup'))
app.add_url_rule('/signout', view_func=SignOutEndpoint.as_view('signout'))
app.add_url_rule('/userpage', view_func=UserpageEndpoint.as_view('userpage'))
app.add_url_rule('/stylize', view_func=StylizeEndpoint.as_view('stylize'))
app.add_url_rule('/styling-result', view_func=StylingResultEndpoint.as_view('styling-result'))
app.add_url_rule('/showcase/<int:id>', view_func=ShowcaseEndpoint.as_view('showcase'))
