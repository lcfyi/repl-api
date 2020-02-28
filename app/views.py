from flask import views, request
from app.dind.runner import CodeRunner
from app.dind.utils import verify_valid_language
import logging


class RunnerAPI(views.MethodView):
    def get(self):
        return ("Heartbeat", 200)

    def post(self):
        data = request.get_json(silent=True)
        logging.info(data)
        if not data:
            return ("Malformed JSON data!", 400)
        if "language" not in data or not data["language"]:
            return ("Missing language field!", 400)
        if "code" not in data or not data["code"]:
            return ("Missing code field!", 400)
        if not verify_valid_language(data["language"]):
            return ("Invalid language!", 400)
        
        runner = CodeRunner(data["language"], data["code"])
        output = runner.run()
        return (output, 200)

