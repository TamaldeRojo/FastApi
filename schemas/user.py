def userModel(i) -> dict:
    return {
        "email":i["email"],
        "password":i["password"]
    }

def usersModel(i=10) -> list:
    return [userModel(item) for item in i]