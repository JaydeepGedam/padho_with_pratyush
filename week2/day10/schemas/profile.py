from pydantic import BaseModel, Field
from typing import Optional

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_year: Optional[str] = None
    achievements: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str
    designation: str
    duration: Optional[str] = None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class Profile(BaseModel):
    name: str
    professional_summary: str
    skills: list[str]
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
