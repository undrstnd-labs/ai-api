import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class InferenceType(Enum):
    GR_LPU = "gr-lpu"
    CR_INF = "cr-inf"
    SM_RDU = "sm-rdu"
    AZ_INF = "az-inf"


class InferenceBaseUrl(Enum):
    GR_LPU = os.environ.get("GR_LPU_ENDPOINT")
    CR_INF = os.environ.get("CR_INF_ENDPOINT")
    SM_RDU = os.environ.get("SM_RDU_ENDPOINT")
    AZ_INF = os.environ.get("AZ_INF_ENDPOINT")
