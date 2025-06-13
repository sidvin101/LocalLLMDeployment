from flask import Flask, request, render_template
from LocalLLMDeployment.api_wrapper import APIWrapper

# Initialize Flask app
app = Flask(__name__)
# Initialize API wrapper
api = APIWrapper()

#Main index route
@app.route("/", methods = ["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
        try:
            api_response = api.generate_chat(messages)
            response = api_response["choices"][0]["message"]["content"]
        except Exception as e:
            response = f"Error: {str(e)}"
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port = 8501)