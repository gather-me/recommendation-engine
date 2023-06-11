from flask import Flask, request
from service.group_recommendation import make_group_recommendation
from service.single_recommendation import make_recommendation
from service.collaborative_filtering import crossValidate
app = Flask(__name__)

@app.route("/events/<event_type>/predict/rate/<int:user_id>")
def single_recommendation(event_type, user_id):
    return make_recommendation(event_type, user_id)


@app.route("/events/<event_type>/predict/rate")
def group_recommendation(event_type):
    users = request.args.getlist('users')
    user_ids = [int(user_id) for user_id in users]
    return make_group_recommendation(event_type, user_ids)