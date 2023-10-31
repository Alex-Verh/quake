from flask import Flask, render_template, request
import config
import main_threads

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("live-state.html", sensors = main_threads.sensor_data)


@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/live-state")
def livestate():
    return render_template("live-state.html")

@app.route("/set_config", methods = ["POST"])
def set_config():
    name = request.args.get('name')
    value = request.args.get('value')
    print("Setting", name, "to", value)
    config.config[name] = value
    config.save()
    return "success"

if __name__ == "__main__":
    main_threads.main()
    app.run(debug=True)
