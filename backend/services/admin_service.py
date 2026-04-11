from fastapi import Depends
from pymongo.synchronous.collection import Collection



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

    def get_users(self, user:Collection):
        users= user.find({},{'_id':0,'user_k_id':1, 'name':1, 'role':1})
        return list(users)

