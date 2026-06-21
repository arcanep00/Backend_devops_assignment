from pydantic import BaseModel


class JobStatusResponse(
    BaseModel
):

    job_id: int

    status: str