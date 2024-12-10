from app.app import app

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
    app.run(PYTHONHASHSEED=app.config["PYTHONHASHSEED"]
~                                                         
