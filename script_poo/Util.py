import base64

class Util:
    def log_info(info):
        print(f"INFO: {info}")
        print("--")
    

    def file_to_base64(file_name):
        with open(file_name, "rb") as file:
            file_content = file.read()
        return base64.b64encode(file_content)