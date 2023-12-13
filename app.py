import os
import pathlib
import requests
from flask import Flask, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import json
from datetime import datetime
from database_functions import save_sentiment_in_db, get_sentiments
from sentiment_functions import analyze_sentiment

app = Flask("Karel ML6 App")
app.secret_key = "<fill in your own secret>"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

google_client_id = "<fill in your own google client id>"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # redirect_uri="http://localhost:8080/callback"
    redirect_uri="https://ml6karel-uzv3utyvga-uc.a.run.app/callback"
)

ml6_sessions = {}

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if("email" not in ml6_sessions):
            return abort(401)
        email = ml6_sessions["email"]
        if(email.endswith("ml6.eu")):
            return function()
        else:
            return abort(401)
    wrapper.__name__ = function.__name__ 
    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    ml6_sessions["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not ml6_sessions["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id,
        clock_skew_in_seconds=1
    )
    ml6_sessions["email"] = id_info.get("email").lower()

    return redirect("/protected_area")


@app.route("/logout")
def logout():
    ml6_sessions.clear()
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_all_analyzes")
@login_is_required
def get_all_analyzes():
    limit = request.args.get('limit', default=10, type=int)
    docs = get_sentiments()
    analyzes = [doc.to_dict() for doc in docs]
    response_data = {
        "analyzes": analyzes[:limit]
    }
    return json.dumps(response_data, default=str)


@app.route("/analyze_sentiment")
@login_is_required
def handle_sentiment_request() -> str: 
    text = request.args.get('text', default="", type=str)
    if(text == ""):
        return "No text provided"
    sentiment, confidence = analyze_sentiment(text)
    response = {
        'sentiment': sentiment,
        'confidence': confidence
    }
    save_sentiment_in_db(datetime.now(), text, sentiment, confidence)
    return json.dumps(response)


@app.route("/protected_area")
@login_is_required
def protected_area():
    logout = f"Hello {ml6_sessions['email']}! <br/> <a href='/logout'><button>Logout</button></a>"
    get_all_analyzes = "Click <a href='./get_all_analyzes'>here</a> to see all the analyzes done before"
    
    analyze_post = '''
        <label for="analyzeText">Text:</label>
        <input type="text" id="textToAnalyze" name="textToAnalyze">
        <button onclick="analyzeSentiment()">Analyze</button>

        <script>
        function analyzeSentiment() {
            var textToAnalyze = document.getElementById('textToAnalyze').value;
            var url = './analyze_sentiment?text=' + textToAnalyze;
            window.location.href = url;
        }
        </script>
    '''
    page = logout  + "<br>" + get_all_analyzes + "<br>" + analyze_post
    return page


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)