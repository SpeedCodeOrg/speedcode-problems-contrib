# Models for messages related to the cloud manager.

from typing import Annotated, Union, Literal, List, Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

##
## Messages from webserver to Cloud Manager
##

# Message indicating that a job has been submitted.
class CM_JobSubmission(BaseModel):
    user_id: str

##
## Messages from a job runner instance to the Cloud Manager
##

# Message indicating that a cloud instance is shutting down.
class CM_Shutdown(BaseModel):
    instance_id: str
    # Indicates whether shutdown is voluntary or due to a detected interruption.
    interrupted: bool

# Message indicating that an instance is entering hibernation.
class CM_Hibernate(BaseModel):
    instance_id: str

# Message indicating that a particular job has started.
class CM_JobStart(BaseModel):
    instance_id: str
    job_id: str

# Message indicating that a particular job has completed.
class CM_JobEnd(BaseModel):
    instance_id: str
    job_id: str

# Notification that the machine is idle.
class CM_Idle(BaseModel):
    instance_id: str

class CM_Message(BaseModel):
    message : Union[CM_JobSubmission, CM_Shutdown, CM_Hibernate, CM_JobStart, \
                    CM_JobEnd, CM_Idle]
