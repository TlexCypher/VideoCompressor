import subprocess


class ServiceResult(object):
    def __init__(self, result: subprocess.CompletedProcess | subprocess.CompletedProcess[bytes],
                 output_filepath: str) -> None:
        self.result = result
        self.output_filepath = output_filepath


class ServiceResult2(object):
    def __init__(self, return_code: int, output_filepath: str) -> None:
        self.return_code = return_code
        self.output_filepath = output_filepath
