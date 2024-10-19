from typing import Annotated, Union, Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from fastapi_auth0 import Auth0User

class ProblemRequest(BaseModel):
    problem_id: int




@dataclass
class ProblemInfo(BaseModel):
    const_id: str
    title: str
    short_description: str
    max_tiers: int 
    tags: str
    location: str
    github_url: str
    public: bool
    #directory_name: str
    class Config:
        orm_mode = True



class ProblemListEntry(BaseModel):
    id: int
    const_id: str
    title: str
    short_description: str
    max_tiers: int 
    tags: str
    #directory_name: str
    class Config:
        orm_mode = True

class ProblemList(BaseModel):
    #problem_id_list: list 
    #directory_names: list
    userinfo : Optional[Auth0User]
    problems: list

class ProblemData(BaseModel):
    readme: str
    source: str
    compiler_options: str
    command_line_arguments: str


class AuthCallback(BaseModel):
    access_token: str
    scope: str
    expires_in: str
    token_type: str
    state: str

class Submission(BaseModel):
    command_line_arguments: str
    compiler_options: str
    language_id: int
    redirect_stderr_to_stdout: bool
    source_code: str
    stdin: str
    problem_id: str



@dataclass
class JobRunnerSubmission(BaseModel):
    # NOTE(TFK): This schema needs a refactor.
    # In particular, uncomment below line and remove duplicated fields.
    #user_submission: Submission
    token: str
    url: str
    location: str

    # Duplicated fields with Submission
    command_line_arguments: str
    compiler_options: str
    language_id: int
    redirect_stderr_to_stdout: bool
    source_code: str
    stdin: str
    problem_id: str
   
    class Config:
        orm_mode = True



class SubmissionResponse(BaseModel):
    status: bool
    stdout: Union[str, None]
    compile_output: str
    time: str
    memory: str
    token: str
    benchmark_results: str
    test_results: str
    previous_results: str

