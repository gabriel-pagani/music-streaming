from utils.conection import server_request


class UserController:
    def __init__(self):
        pass

    def insert_user(self) -> dict:
        self.response = server_request(query='insert into usuarios values ...')
        return self.response

    def select_users(self) -> dict:
        self.response = server_request(query='select * from usuarios')
        return self.response

    def update_user(self) -> dict:
        self.response = server_request(query='updete set usuarios ...')
        return self.response

    def delete_user(self) -> dict:
        self.response = server_request(query='delete from usuarios where ...')
        return self.response
