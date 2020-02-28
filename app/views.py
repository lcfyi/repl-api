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
        if (
            data
            and "language" in data
            and "code" in data
            and verify_valid_language(data["language"])
        ):
            runner = CodeRunner(data["language"], data["code"])
            output = runner.run()
            return (output, 200)
        else:
            logging.info("Malformed request")
            return ("Malformed JSON data!", 400)
