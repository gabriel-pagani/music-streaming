from utils.conection import server_request


class UserController:
    def __init__(self):
        pass

    def insert_user(self) -> dict:
        return server_request(query='insert into usuarios values ...')

    def select_users(self) -> dict:
        return server_request(query='select * from usuarios')

    def update_user(self) -> dict:
        return server_request(query='updete set usuarios ...')

    def delete_user(self) -> dict:
        return server_request(query='delete from usuarios where ...')
