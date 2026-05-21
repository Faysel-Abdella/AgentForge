def evaluate(response: str, rules: list):

    for rule in rules:

        if rule["type"] == "must_not_contain":

            for word in rule["value"]:

                if word.lower() in response.lower():
                    return False

        if rule["type"] == "must_contain":

            for word in rule["value"]:

                if word.lower() not in response.lower():
                    return False

    return True
