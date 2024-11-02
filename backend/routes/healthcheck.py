from flask import Blueprint
from pydantic import BaseModel

from ..schemas import spec

bp = Blueprint("healthcheck", __name__, url_prefix="/api/v1")


def check_db():
    is_database_working = False
    output = ""

    try:
        # to check database we will execute raw query
        # TODO: replace with Chpher query
        is_database_working = True
    except Exception as e:
        output = str(e)

    return is_database_working, output


class Resp(BaseModel):
    apiVersion: str


@bp.route("/healthcheck", methods=["GET"])
# @validate(auth=False, resp=Response("HTTP_500", HTTP_200=Resp))
def healthcheck():
    """Verifies service health and returns the api version"""
    check_db()
    return {"apiVersion": spec.config.version}, 200
