from flask import Flask, render_template

app = Flask(__name__)



@app.route("/")
def main():
    return render_template("live-state.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/live-state")
def livestate():
    return render_template("live-state.html")

if __name__ == "__main__":
    app.run(debug=True)