from flask import Flask, request, render_template, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "n/a"  # Needed for session management

CHATBOT_URL = "https://advancedchatbot.onrender.com/chat"

@app.route("/", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            session["chat_history"].append(("You", user_message))
            try:
                response = requests.post(CHATBOT_URL, json={"message": user_message})
                if response.status_code == 200:
                    bot_reply = response.text
                else:
                    bot_reply = f"Error {response.status_code}: {response.text}"
            except Exception as e:
                bot_reply = f"An error occurred: {e}"

            session["chat_history"].append(("Chatbot", bot_reply))
            session.modified = True

        return redirect(url_for("chat"))

    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(debug=True)
