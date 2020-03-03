from typing import Dict
from abc import abstractmethod, abstractproperty

import mimetypes

from marshmallow import Schema


class ResponseObjectInterface:
    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_schema() -> Schema:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def content_type() -> str:
        raise NotImplementedError
