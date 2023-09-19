class FileData:
    data = {"title": "Title",
            "file_name": "test_file",
            "is_active": True,
            "file_type": "document",
            "file_size": "",
            "storage": ""
            }
    file = {'file': open('test_files/test_doc.txt', 'rb')}

    update_file = {"title": "Title_Updated",
                   "is_active": False, "storage": "local"}

    part_upd_file = {"is_active": True}


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
