from app import app_factory

if __name__ == '__main__':
    app = app_factory()
    if app:
        app.run()