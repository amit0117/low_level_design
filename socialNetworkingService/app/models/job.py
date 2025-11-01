from uuid import uuid4
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from app.models.enums import JobType, ApplicationStatus

if TYPE_CHECKING:
    from app.models.user import User


class Company:
    def __init__(self, name: str, location: str, description: Optional[str] = None):
        self.id = str(uuid4())
        self.name = name
        self.location = location
        self.description = description or ""
        self.jobs: List["Job"] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_location(self) -> str:
        return self.location

    def get_description(self) -> str:
        return self.description

    def add_job(self, job: "Job") -> None:
        self.jobs.append(job)

    def get_jobs(self) -> List["Job"]:
        return self.jobs.copy()


class Job:
    def __init__(
        self,
        title: str,
        company: Company,
        description: str,
        location: str,
        job_type: JobType,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        required_skills: Optional[List[str]] = None,
    ):
        self.id = str(uuid4())
        self.title = title
        self.company = company
        self.description = description
        self.location = location
        self.job_type = job_type
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.required_skills = required_skills or []
        self.created_at = datetime.now()
        self.applications: List["Application"] = []

    def get_id(self) -> str:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_company(self) -> Company:
        return self.company

    def get_description(self) -> str:
        return self.description

    def get_location(self) -> str:
        return self.location

    def get_job_type(self) -> JobType:
        return self.job_type

    def get_salary_range(self) -> tuple:
        return (self.salary_min, self.salary_max)

    def get_required_skills(self) -> List[str]:
        return self.required_skills.copy()

    def get_created_at(self) -> datetime:
        return self.created_at

    def add_application(self, application: "Application") -> None:
        self.applications.append(application)

    def get_applications(self) -> List["Application"]:
        return self.applications.copy()

    def matches_skills(self, user_skills: List[str]) -> bool:
        """Check if job requirements match user's skills"""
        if not self.required_skills:
            return True
        return any(skill in user_skills for skill in self.required_skills)


class Application:
    def __init__(self, job: Job, applicant: "User", cover_letter: Optional[str] = None):
        self.id = str(uuid4())
        self.job = job
        self.applicant = applicant
        self.cover_letter = cover_letter or ""
        self.status = ApplicationStatus.PENDING
        self.applied_at = datetime.now()
        self.updated_at = datetime.now()

    def get_id(self) -> str:
        return self.id

    def get_job(self) -> Job:
        return self.job

    def get_applicant(self) -> "User":
        return self.applicant

    def get_cover_letter(self) -> str:
        return self.cover_letter

    def get_status(self) -> ApplicationStatus:
        return self.status

    def get_applied_at(self) -> datetime:
        return self.applied_at

    def get_updated_at(self) -> datetime:
        return self.updated_at

    def update_status(self, status: ApplicationStatus) -> None:
        self.status = status
        self.updated_at = datetime.now()
