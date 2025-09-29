from dotenv import load_dotenv

wsgi_app = "api.app:create_app()"


def on_starting(_server):
    load_dotenv(".env")
