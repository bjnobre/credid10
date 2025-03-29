from flask import Flask

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    # Set your flag here:
    app.config['SHOW_TABLE'] = True  # Change to False to show only the parcela value
    app.config['JUROS'] = 15.0         # Interest rate (15% per month, for example)

    from .routes import main
    app.register_blueprint(main)
    return app
