import enum
from typing import Optional

from enum import Enum


class CompressService(Enum):
    Compress = 1
    Change_Resolution = 2
    Change_Aspect_Ratio = 3
    Convert_Into_Audio = 4
    Create_Gif = 5

    @staticmethod
    def get_service(selected_service: str) -> Optional[enum.Enum]:
        for service in CompressService:
            if int(service.value) == int(selected_service):
                return service
        return None
