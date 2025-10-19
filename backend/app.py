import os

from database import PostgresHandler
from flask import Flask, jsonify
from flask.cli import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:3000",
    ],
)


def create_db_connection():
    return PostgresHandler(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        port=5432,
    )


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/api/ping")
def ping_db():
    db = create_db_connection()
    try:
        db.execute("SELECT 1")
        return jsonify({"status": "ok", "message": "db connection successful"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


@app.route("/api/majors")
def get_majors():
    db = create_db_connection()
    try:
        majors = db.fetchall("select name, uid from majors")
        if majors is None:
            return jsonify({"status": "ok", "message": "failed to get majors"})
        return jsonify({"status": "ok", "data": majors}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


@app.route("/api/major/<int:major_uid>")
def get_major(major_uid):
    db = create_db_connection()
    try:
        major_data = db.fetchone("select * from majors where uid = %s", (major_uid,))
        if major_data is None:
            return jsonify({"status": "error", "message": "major not found"}), 404
        return jsonify({"status": "ok", "data": major_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


@app.route("/api/admission/<int:major_uid>")
def get_admission_statistics(major_uid):
    db = create_db_connection()
    try:
        admission_statistics = db.fetchall(
            "select * from admission_statistics where uid = %s", (major_uid,)
        )
        if admission_statistics is None:
            return (
                jsonify(
                    {"status": "error", "message": "admission statistics not found"}
                ),
                404,
            )
        return jsonify({"status": "ok", "data": admission_statistics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


@app.route("/api/average-cutoffs")
def get_average_cutoff():
    db = create_db_connection()
    try:
        average_admission_statistics = db.fetchall(
            """
            select year, avg(min_grade) as min_grade, avg(max_grade) as max_grade, sum(initial_reject) as initial_reject, sum(final_admit) as final_admit
            from admission_statistics
            group by year
            """
        )
        if average_admission_statistics is None:
            return (
                jsonify({"status": "error", "message": "average cutoff not available"}),
                404,
            )
        return jsonify({"status": "ok", "data": average_admission_statistics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


@app.route("/api/max-admissions")
def get_max_cutoff():
    db = create_db_connection()
    try:
        max_admission_statistics = db.fetchall(
            """
            select distinct on (year) year, uid, min_grade, max_grade
            from admission_statistics
            where min_grade is not null
            order by year, min_grade desc;
            """
        )
        if max_admission_statistics is None:
            return (
                jsonify({"status": "error", "message": "max admissions not available"}),
                404,
            )
        return jsonify({"status": "ok", "data": max_admission_statistics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
