from flask import (Flask)
from flask_cors import CORS
from .controller.nutrition import nutrition_page
from .controller.logReg import logReg_page
from .controller.message import message_page
from .controller.foodSearch import foodSearch_page
from .controller.news import news_page
from .controller.profile import profile_page
from .controller.fitness import fitness_page
from .controller.friends import friends_page
from .controller.caloriesHistory import caloriesHistory_page


app = Flask("__main__")
app.register_blueprint(nutrition_page)
app.register_blueprint(logReg_page)
app.register_blueprint(message_page)
app.register_blueprint(foodSearch_page)
app.register_blueprint(news_page)
app.register_blueprint(profile_page)
app.register_blueprint(news_page)
app.register_blueprint(fitness_page)
app.register_blueprint(friends_page)
app.register_blueprint(caloriesHistory_page)



CORS(app)