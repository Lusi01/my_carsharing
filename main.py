import os
from app import app


if os.environ.get('APP_LOCATION') == 'heroku':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(debug = True)

if __name__ == "__main__":
    print("server is running on localhost!!!")
    app.run(debug=True)