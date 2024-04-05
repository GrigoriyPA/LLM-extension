import typing as tp
from copy import copy

from configs.entities import ENTITY_TYPE
from configs.main_config import ExtensionFeature
from datasets.database_utils import Table
from models.base_model import BaseModel

T = ENTITY_TYPE
U = copy(ENTITY_TYPE)


class Experiment(tp.Generic[T, U]):
    def __init__(self, model: BaseModel, task_type: ExtensionFeature, src: Table[T], dst: Table[U]):
        self.model = model
        self.task_type = task_type
        self.src = src
        self.dst = dst


