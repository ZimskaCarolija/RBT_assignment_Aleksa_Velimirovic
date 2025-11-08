from flask import jsonify
from typing import Any, Optional

class ApiResponse:
    @staticmethod
    def success(data: Any, status_code: int = 200):
        return jsonify({
            "success": True,
            "data": data,
            "error": None,
            "status_code": status_code
        }), status_code

    @staticmethod
    def error(message: str, status_code: int = 500):
        return jsonify({
            "success": False,
            "data": None,
            "error": message,
            "status_code": status_code
        }), status_code