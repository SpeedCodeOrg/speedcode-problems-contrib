from typing import Annotated, Union, Optional, List
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from fastapi_auth0 import Auth0User

from models.problem_response_models import PRM_InputManifest


class ProblemRequest(BaseModel):
    problem_id: int

class PresignedURL(BaseModel):
    response : str 

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
    problem_set_id: Optional[int]
    input_manifest : Optional[str] = None
    
    #directory_name: str
    class Config:
        orm_mode = True

#@dataclass
#class Fastcoder_Result(BaseModel):
#    id : int #= Column(Integer, primary_key=True, index=True)
#    const_id : str #= Column(String, index=True)
#    parent_const_id : str #= Column(String)
#    title : str #= Column(String)
#    status : str#= Column(String)
#    prompt : str#= Column(String)
#    method : str#= Column(String)
#    display_data : str#= Column(String)
#    #time_created = Column(DateTime(timezone=True), server_default=func.now())
#    #time_updated = Column(DateTime(timezone=True), onupdate=func.now())
#    class Config:
#        orm_mode = True
    



class UserAPIKeysResponse(BaseModel):
    user_const_id : str #Column(String, index=True)
    api_key : str#Column(String, index=True)
    title : Optional[str] = None
    short_description : Optional[str] = None
    readme : Optional[str] = None
    source : Optional[str] = None
    default_custom_input : Optional[str] = None
    input_manifest : Optional[str] = None


class ProblemListEntry(BaseModel):
    #id: int
    const_id: str
    title: str
    short_description: str
    max_tiers: int 
    tags: str
    user_progress : Optional[int] = None
    #directory_name: str
    class Config:
        orm_mode = True

class ProblemSetListEntry(BaseModel):
    #id: int
    const_id: str
    title: str
    class Config:
        orm_mode = True



class LeaderboardEntries(BaseModel):
    user_id: str
    points: int

class Leaderboard(BaseModel):
    leaderboard_entries : List[LeaderboardEntries]
    your_user_id : Optional[str]
    your_points : Optional[int]
    your_rank : Optional[int]

class ProblemList(BaseModel):
    #problem_id_list: list 
    #directory_names: list
    userinfo : Optional[Auth0User]
    problems: list
    problem_set_title : Optional[str]


class SubmissionListEntry(BaseModel):
    user_const_id : str
    problem_const_id : str
    problem_title : str
    runtime : float
    status : str

class ProblemSetList(BaseModel):
    problem_sets : list

class ProblemSetSubmissions(BaseModel):
    submissions : list


class AuthCallback(BaseModel):
    access_token: str
    scope: str
    expires_in: str
    token_type: str
    state: str

class ContributePrompt(BaseModel):
    prompt: str

class Submission(BaseModel):
    command_line_arguments: str
    compiler_options: str
    language_id: int
    redirect_stderr_to_stdout: bool
    source_code: str
    stdin: str
    problem_id: str
    run_parallel: bool
    run_custom: bool
    input_targets : Optional[List[str]] = None

class EditProblemSetRequest(BaseModel):
    problem_set_const_id : Optional[str]
    problem_set_name : str
    problem_set_problems : List[str]

class EditProblemSetResponse(BaseModel):
    problem_set_const_id : str
    success: bool    

@dataclass
class JobRunnerSubmission(BaseModel):
    # NOTE(TFK): This schema needs a refactor.
    # In particular, uncomment below line and remove duplicated fields.
    #user_submission: Submission
    token: str
    url: str
    location: str
    run_parallel: bool
    run_custom: bool
    # Duplicated fields with Submission
    command_line_arguments: str = ""
    compiler_options: str = ""
    language_id: int
    redirect_stderr_to_stdout: bool
    source_code: str
    stdin: str = ""
    problem_id: str

    input_targets: Optional[List[str]] = None
   
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

class FastCoderDemoAction(BaseModel):
    data : str
    method : str
    reference_id: str


class FastCoder_Result(BaseModel):
    const_id : str
    parent_const_id : Optional[str] = None
    title : Optional[str] = None
    status : Optional[str] = None
    prompt: str
    method: str
    display_data : Optional[str] = None

class FastCoder_Result_List(BaseModel):
    results : List[FastCoder_Result]

# note this is a temporary class just for giving code snippets and other junk.
class FastCoder_RawResponse(BaseModel):
    data : str


