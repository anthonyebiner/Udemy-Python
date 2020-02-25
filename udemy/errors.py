class UdemyResponseError(Exception):
    @staticmethod
    def generateError(msg, response):
        error = '\n' + msg + '\n'
        error += str(response) + '\n'
        error += str(response.text) + '\n'
        error += str(response.url)
        return error


class UdemyArgumentsError(Exception):
    pass
