import subprocess


class ServiceResult(object):
    def __init__(self, result: subprocess.CompletedProcess | subprocess.CompletedProcess[bytes],
                 output_filepath: str, mime_type: str) -> None:
        self.result = result
        self.output_filepath = output_filepath
        self.mime_type = mime_type


class ServiceResult2(object):
    def __init__(self, return_code: int, file_content: bytes, mime_type: str) -> None:
        self.return_code = return_code
        self.file_content = file_content
        self.mime_type = mime_type
