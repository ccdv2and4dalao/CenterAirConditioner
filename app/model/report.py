from abstract.model import Report, ReportModel
from app.database import sqlDatabase


class ReportModelImpl(ReportModel):
    def create(self):
        self.db = sqlDatabase
