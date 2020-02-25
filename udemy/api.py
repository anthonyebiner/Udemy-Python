import json
import requests
from udemy.errors import UdemyResponseError
from udemy.models import (
    Question,
    Course,
    Review,
    Reply,
    Message,
    Thread,
)


class Api:
    def __init__(self, client_id, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self._auth = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "bearer " + client_id
        }

    def get_all_courses(self, ordering='', student='', page=1, page_size=25):
        if student:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/courses/"
                "?fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&student={}"
                "&ordering={}"
                "&page={}"
                "&page_size{}".format(student, ordering, page, page_size),
                headers=self._auth)
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/courses/"
                "?fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}"
                "&page={}"
                "&page_size={}".format(ordering, page, page_size),
                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get courses', response))
            for result in response.json()['results']:
                yield Course(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_all_questions(self, status='', course='', ordering='', page=1, page_size=25):
        if not course:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/questions/"
                "?status={}"
                "&fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}"
                "&page={}"
                "&page_size={}".format(status, ordering, page, page_size),
                headers=self._auth)
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/questions/"
                "?status={}"
                "&course={}"
                "&fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}"
                "&page={}"
                "&page_size={}".format(status, course, ordering, page, page_size),
                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get questions', response))
            for result in response.json()['results']:
                yield Question(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_all_reviews(self, status='', course='', stars=None, ordering='', page=1, page_size=25):
        if stars is None:
            stars = []
        if stars and isinstance(stars, list):
            string = ""
            for star in stars:
                string += str(star) + ','
            stars = string[:-1]
        elif not stars:
            stars = "1,2,3,4,5"
        if not course:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/reviews/"
                "?status={}"
                "&star={}"
                "&fields%5Bcourse_review%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}"
                "&page={}"
                "&page_size={}".format(status, stars, ordering, page, page_size),
                headers=self._auth)
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/reviews/"
                "?status={}"
                "&course={}"
                "&star={}"
                "&fields%5Bcourse_review%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}"
                "&page={}"
                "&page_size={}".format(status, course, stars, ordering, page, page_size),
                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get reviews', response))
            for result in response.json()['results']:
                yield Review(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_course_questions(self, course_id, ordering='', page=1, page_size=25):
        response = requests.get("https://www.udemy.com/instructor-api/v1/courses/{}/questions/"
                                "?fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                                "&ordering={}"
                                "&page={}"
                                "&page_size={}".format(course_id, ordering, page, page_size),
                                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get questions', response))
            for result in response.json()['results']:
                yield Question(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_question_replies(self, course_id, question_id, ordering='', page=1, page_size=25):
        response = requests.get("https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/replies/"
                                "?fields%5Banswer%5D=@all&fields%5Buser%5D=@all"
                                "&ordering={}"
                                "&page={}"
                                "&page_size={}".format(course_id, question_id, ordering, page, page_size),
                                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get replies', response))
            for result in response.json()['results']:
                yield Reply(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_message_threads(self, status='', other_user='', page=1, page_size=25):
        if other_user:
            response = requests.get("https://www.udemy.com/instructor-api/v1/message-threads/"
                                    "?fields%5Bmessage_thread%5D=@all&fields%5Bmessage%5D=@all&fields%5Buser%5D=@all"
                                    "&status={}"
                                    "&other_user={}"
                                    "&page={}"
                                    "&page_size={}".format(status, other_user, page, page_size),
                                    headers=self._auth)
        else:
            response = requests.get("https://www.udemy.com/instructor-api/v1/message-threads/"
                                    "?fields%5Bmessage_thread%5D=@all&fields%5Bmessage%5D=@all&fields%5Buser%5D=@all"
                                    "&status={}"
                                    "&page={}"
                                    "&page_size={}".format(status, page, page_size),
                                    headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get threads', response))
            for result in response.json()['results']:
                yield Thread(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def get_messages(self, message_thread_id, page=1, page_size=25):
        response = requests.get("https://www.udemy.com/instructor-api/v1/message-threads/{}/messages/"
                                "?fields%5Bmessage%5D=@all&fields%5Buser%5D=@all"
                                "&page={}"
                                "&page_size={}".format(message_thread_id, page, page_size),
                                headers=self._auth)
        while True:
            if response.status_code != 200:
                raise UdemyResponseError(UdemyResponseError.generateError('Could not get messages', response))
            for result in response.json()['results']:
                yield Message(result, self)
            if not response.json()['next']:
                break
            response = requests.get(response.json()['next'], headers=self._auth)

    def delete_question(self, course_id, pk):
        response = requests.delete(
            "https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/"
            "?fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all".format(
                course_id, pk),
            headers=self._auth)
        if response.status_code != 200:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not delete question', response))
        return Question(response.json(), self)

    def post_question_reply(self, course_id, question_id, body):
        data = {"body": body}
        response = requests.post(
            'https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/replies'.format(course_id, question_id),
            headers=self._auth,
            data=json.dumps(data))
        if response.status_code != 201:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not post reply', response))
        return Reply(response.json(), self)

    def post_message(self, message_thread_id, body):
        data = {"body": body}
        response = requests.post("https://www.udemy.com/instructor-api/v1/message-threads/{}/messages/"
                                 "?fields%5Bmessage%5D=@all&fields%5Buser%5D=@all".format(message_thread_id),
                                 headers=self._auth,
                                 data=json.dumps(data))
        if response.status_code != 201:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not post message', response))
        return Message(response.json(), self)

    def update_question(self, course_id, question_id, read):
        data = {'is_read': read}
        response = requests.put(
            "https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/"
            "?fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all".format(
                course_id, question_id),
            headers=self._auth,
            data=json.dumps(data))
        if response.status_code != 200:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not update question', response))
        return Question(response.json(), self)

    def update_question_reply(self, course_id, question_id, response_id, is_top_answer=None, body=None):
        data = {}
        if is_top_answer is not None:
            data['is_top_answer'] = is_top_answer
        if body is not None:
            data['body'] = body
        response = requests.put(
            "https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/replies/{}/"
            "?fields%5Banswer%5D=@all&fields%5Buser%5D=@all".format(course_id, question_id, response_id),
            headers=self._auth,
            data=json.dumps(data))
        if response.status_code != 200:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not update reply', response))
        return Reply(response.json(), self)

    def update_thread_detail(self, thread_id, is_read=None, is_starred=None, is_deleted=None, is_muted=None):
        data = {}
        if is_read is not None:
            data['is_read'] = is_read
        if is_starred is not None:
            data['is_starred'] = is_starred
        if is_deleted is not None:
            data['is_deleted'] = is_deleted
        if is_muted is not None:
            data['is_muted'] = is_muted
        response = requests.put(
            "https://www.udemy.com/instructor-api/v1/message-threads/{}/"
            "?fields%5Bmessage_thread%5D=@all&fields%5Bmessage%5D=@all&fields%5Buser%5D=@all".format(thread_id),
            headers=self._auth,
            data=json.dumps(data))
        if response.status_code != 200:
            raise UdemyResponseError(UdemyResponseError.generateError('Could not update thread', response))
        return Thread(response.json(), self)
