

class AdminService:
    def __init__(self):
        pass
    def check_extension(self, file_name: str) -> bool:
        """
        확장자 검사
        :param file_name:
        :return:
        """
        if file_name.split(".")[-1] == "txt":
            return True
        else:
            return False
