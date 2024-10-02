import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class InferenceType(Enum):
    GR_LPU = "gr-lpu"
    CR_INF = "cr-inf"
    SM_RDU = "sm-rdu"


class InferenceBaseUrl(Enum):
    GR_LPU = os.getenv("GR_LPU_ENDPOINT")
    CR_INF = os.getenv("CR_INF_ENDPOINT")
    SM_RDU = os.getenv("SM_RDU_ENDPOINT")
