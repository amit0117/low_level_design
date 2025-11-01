from abc import ABC, abstractmethod
from app.models.user import User
from app.models.job import Job
from typing import List


class JobRecommendationStrategy(ABC):
    @abstractmethod
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        raise NotImplementedError("recommend_jobs method is not implemented")


class SkillBasedStrategy(JobRecommendationStrategy):
    """
    Recommends jobs based on user's skills matching job requirements
    Priority: Jobs that match more user skills come first
    """

    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        user_skills = user.get_profile().get_skills() if user.get_profile() else []

        # Score jobs based on skill matches
        scored_jobs = []
        for job in available_jobs:
            matching_skills = len(set(user_skills) & set(job.get_required_skills()))
            total_required = len(job.get_required_skills())

            if total_required == 0:
                score = 1.0  # No skills required = perfect match
            else:
                score = matching_skills / total_required

            scored_jobs.append((job, score))

        # Sort by score (descending) and return top matches
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, score in scored_jobs if score > 0][:10]


class LocationBasedStrategy(JobRecommendationStrategy):
    """
    Recommends jobs based on user's location preference or proximity
    Priority: Jobs in same location as user come first
    """

    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        user_location = user.get_profile().get_location() if user.get_profile() else ""

        if not user_location:
            return available_jobs[:10]  # Return first 10 if no location preference

        # Score jobs based on location match
        scored_jobs = []
        for job in available_jobs:
            if job.get_location().lower() == user_location.lower():
                score = 1.0  # Exact location match
            elif user_location.lower() in job.get_location().lower():
                score = 0.8  # Partial location match
            elif job.get_location().lower() in user_location.lower():
                score = 0.6  # Reverse partial match
            else:
                score = 0.2  # No location match but still show

            scored_jobs.append((job, score))

        # Sort by score (descending)
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, score in scored_jobs][:10]


class CompanyBasedStrategy(JobRecommendationStrategy):
    """
    Recommends jobs from companies where user's connections work
    Priority: Jobs from companies where friends work come first
    """

    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        friends = user.get_friends()
        friend_companies = set()

        # Collect companies where friends work (simplified - in real system would be from profiles)
        for friend in friends:
            # For now, we'll simulate this by checking if friend's profile has company info
            if friend.get_profile() and hasattr(friend.get_profile(), "get_current_company"):
                company = friend.get_profile().get_current_company()
                if company:
                    friend_companies.add(company.lower())

        # Score jobs based on company connections
        scored_jobs = []
        for job in available_jobs:
            company_name = job.get_company().get_name().lower()
            if company_name in friend_companies:
                score = 1.0  # Friend works here
            else:
                score = 0.5  # No direct connection

            scored_jobs.append((job, score))

        # Sort by score (descending) and return
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, score in scored_jobs][:10]


class SalaryBasedStrategy(JobRecommendationStrategy):
    """
    Recommends jobs based on salary expectations
    Priority: Jobs within user's expected salary range
    """

    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        # In a real system, user would have salary expectations in profile
        # For now, we'll filter jobs with salary info and sort by salary range
        jobs_with_salary = [job for job in available_jobs if job.get_salary_range()[0] is not None]

        # Sort by minimum salary (descending - higher paying first)
        jobs_with_salary.sort(key=lambda x: x.get_salary_range()[0] or 0, reverse=True)

        # Return top 10 highest paying jobs
        return jobs_with_salary[:10]


class RecentJobsStrategy(JobRecommendationStrategy):
    """
    Recommends most recently posted jobs
    Priority: Newest jobs first
    """

    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        # Sort by creation date (most recent first)
        sorted_jobs = sorted(available_jobs, key=lambda x: x.get_created_at(), reverse=True)
        return sorted_jobs[:10]
