from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "service": "AI-TestLab API",
        "endpoint": "/api/jobs/flow_def/list",
        "method": "POST"
    })


@app.route("/api/jobs/flow_def/list", methods=["POST"])
def get_flow_list():
    data = request.get_json(silent=True) or {}

    page_num = data.get("page_num", 1)
    page_size = data.get("page_size", 10)

    if (
        type(page_num) is not int
        or type(page_size) is not int
        or page_num < 1
        or page_size < 1
        or page_size > 100
    ):
        return jsonify({
            "code": 0,
            "message": "Invalid pagination parameters"
        }), 400

    flows = [
        {"id": 1, "name": "Flow A"},
        {"id": 2, "name": "Flow B"},
        {"id": 3, "name": "Flow C"}
    ]

    start = (page_num - 1) * page_size
    result = flows[start:start + page_size]

    return jsonify({
        "code": 1,
        "data": {
            "list": result,
            "total": len(flows)
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True)