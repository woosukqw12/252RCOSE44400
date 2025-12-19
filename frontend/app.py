from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# URL of the backend container inside Docker network
# Docker 네트워크 내에서 'backend'라는 서비스 이름으로 통신합니다.
BACKEND_URL = "http://backend:5001"


@app.route("/", methods=["GET"])
def index():
    """
    TODO:
    - Send a GET request to BACKEND_URL + "/api/message"
    - Extract the message from the JSON response
    - Render index.html and pass the message as "current_message"
    """
    try:
        response = requests.get(f"{BACKEND_URL}/api/message")

        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "")

            if "(updated at " in message:
                msg_and_time = message.split("(updated at ")
                message_content = msg_and_time[0].strip()
                timestamp = msg_and_time[1].replace(")", "")
            else:
                message_content = message
                timestamp = "N/A"
        else:
            message = "Error: Backend returned error status."

    except requests.exceptions.RequestException:
        message = "Error: Could not connect to backend."

    return render_template("index.html", current_message=message_content, timestamp=timestamp)

@app.route("/update", methods=["POST"])
def update():
    """
    TODO:
    - Get the value from the form field named "new_message"
    - Send a POST request to BACKEND_URL + "/api/message"
      with JSON body { "message": new_message }
    - Redirect back to "/"
    """
    new_message = request.form.get("new_message")

    try:
        requests.post(f"{BACKEND_URL}/api/message", json={"message": new_message})
    except requests.exceptions.RequestException:
        pass

    return redirect("/")


if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5000)