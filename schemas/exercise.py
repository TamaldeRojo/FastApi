def exerciseModel(i) -> dict:
    return {
        "email":i["email"],
        "typeOf":i["typeOf"],
        "count":i["count"]
    }

def exercisesModel(i=10) -> list:
    return [exerciseModel(item) for item in i]