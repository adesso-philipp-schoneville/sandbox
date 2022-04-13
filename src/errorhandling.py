from flask import Response, jsonify, Flask
from werkzeug.exceptions import HTTPException, BadRequest

from src.common import logger

class RequestWrongEventType(BadRequest):
    """If eventType not OBJECT_FINALIZE."""
    pass

class BQError(Exception):
    """Raised when BQ insertion fails."""
    pass

class RequestKeyError(KeyError):
    """KeyError in request."""
    pass

def register_error_handlers(app: Flask) -> None:
    """Register all errorhandlers to the app."""
    
    @app.errorhandler(Exception)
    def handle_exceptions(e: Exception) -> Response:
        """Handle all exceptions that are not excplicitly handled and log traceback."""
        msg = f"Unexpected Error - {e.__class__.__name__} : {e}"
        logger.exception(e)
        
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        
        response = {"code": code,
                    "name": e.__class__.__name__,
                    "description": msg}
        return jsonify(response), code

    @app.errorhandler(404)
    def handle_not_found(e: Exception) -> Response:
        """Logging and return json of 404 errors."""
        logger.error(str(e))
        return jsonify(code=404, name="Not Found", description=str(e)), 404


    @app.errorhandler(BQError)
    @app.errorhandler(FileNotFoundError)
    @app.errorhandler(BadRequest)
    @app.errorhandler(RequestKeyError)
    def handle_exceptions(e: Exception) -> Response:
        """Logging and return json of all errors as a result of a bad request."""
        if isinstance(e, RequestWrongEventType):
            logger.warning(str(e))
        else:
            logger.error(str(e))
        response = {"code": 400,
                    "name": e.__class__.__name__,
                    "description": str(e)}
        return jsonify(response), 400