import json

import requests


class Question:
    def __init__(self, question_dict, _auth, _parent):
        self._parent = _parent
        self.body = question_dict['body']
        self.course = Course(question_dict['course'], _auth, _parent)
        self.created = question_dict['created']
        self.id = question_dict['id']
        self.is_instructor = question_dict['is_instructor']
        self.is_read = question_dict['is_read']
        self.last_activity = question_dict['last_activity']
        self.modified = question_dict['modified']
        self.num_follows = question_dict['num_follows']
        self.num_replies = question_dict['num_replies']
        self.num_reply_upvotes = question_dict['num_reply_upvotes']
        self.num_upvotes = question_dict['num_upvotes']
        self.related_lecture_id = question_dict['related_lecture_id']
        self.related_lecture_title = question_dict['related_lecture_title']
        self.related_lecture_url = question_dict['related_lecture_url']
        self.reply_raw = question_dict['replies']
        self.title = question_dict['title']
        self.user = User(question_dict['user'], _parent)
        self._auth = _auth

    @property
    def replies(self):
        for reply in self.reply_raw:
            yield Reply(reply, self._parent)

    def delete(self):
        self._parent.delete_question(self.course.id, self.id)

    def post_question_response(self, body):
        self._parent.post_question_response(self.course.id, self.id, body)

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.id == other.id
        else:
            return False


class Course:
    def __init__(self, course_dict, _auth, _parent):
        self._parent = _parent
        self._auth = _auth
        self.created = course_dict['created']
        self.description = course_dict['description']
        self.headline = course_dict['headline']
        self.id = course_dict['id']
        self.is_paid = course_dict['is_paid']
        self.is_published = course_dict['is_published']
        self.num_reviews = course_dict['num_reviews']
        self.published_time = course_dict['published_time']
        self.published_title = course_dict['published_title']
        self.rating = course_dict['rating']
        self.title = course_dict['title']
        self.url = course_dict['url']
        self.visible_instructors_raw = course_dict['visible_instructors']

    @property
    def visible_instructors(self):
        for instructor in self.visible_instructors_raw:
            yield User(instructor, self._parent)

    def get_questions(self):
        yield from self._parent.get_course_questions(self.id)

    def get_question_replies(self, question_id):
        yield from self._parent.get_course_replies(self.id, question_id)

    def delete_question(self, pk):
        self._parent.delete_question(self.id, pk)

    def post_question_response(self, question_id, body):
        self._parent.post_question_response(self.id, question_id, body)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.id == other.id
        else:
            return False


class Review:
    def __init__(self, review_dict, _auth, _parent):
        self._parent = _parent
        self.id = review_dict['id']
        self.content = review_dict['content']
        self.course = Course(review_dict['course'], _auth, _parent)
        self.created = review_dict['created']
        self.rating = review_dict['rating']
        try:
            self.response = Response(review_dict['response'], _parent)
        except TypeError:
            self.response = None
        self.user = User(review_dict['user'], _parent)
        self.user_modified = review_dict['user_modified']
        self._auth = _auth


class Response:
    def __init__(self, response_dict, _parent):
        self._parent = _parent
        self.content = response_dict['content']
        self.created = response_dict['created']
        self.modified = response_dict['modified']
        self.user = User(response_dict['user'], _parent)
        self.id = response_dict['id']


class Reply:
    def __init__(self, reply_dict, _parent):
        self._parent = _parent
        self.created = reply_dict['created']
        self.last_activity = reply_dict['last_activity']
        self.user = User(reply_dict['user'], _parent)
        self.is_top_answer = reply_dict['is_top_answer']
        self.body = reply_dict['body']
        self.is_upvoted = reply_dict['is_upvoted']
        self.num_upvotes = reply_dict['num_upvotes']
        self.id = reply_dict['id']


class Message:
    def __init__(self, message_dict, _parent):
        self._parent = _parent
        self.content = message_dict['content']
        self.created = message_dict['created']
        self.id = message_dict['id']
        self.is_outgoing = message_dict['is_outgoing']
        self.user = message_dict['user']

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False


class User:
    def __init__(self, user_dict, _parent):
        self._parent = _parent
        self.id = user_dict['id']
        self.locale = user_dict['locale']
        self.name = user_dict['name']
        self.title = user_dict['title']

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False


class Thread:
    def __init__(self, thread_dict, _parent):
        self._parent = _parent
        self.created = thread_dict['created']
        self.id = thread_dict['id']
        self.is_read = thread_dict['is_read']
        self.is_starred = thread_dict['is_starred']
        self.last_message = thread_dict['last_message']
        self.other_user = thread_dict['other_user']

    def post_message(self, body):
        self._parent.post_message(self.id, body)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False


class UdemyPublic:
    def __init__(self, client_id, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self._auth = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "bearer " + client_id
        }

    def get_all_courses(self, ordering=None, student=None):
        if not student:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/courses/"
                "?fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&student={}"
                "&ordering={}".format(student, ordering),
                headers=self._auth).json()
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/courses/"
                "?fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}".format(ordering),
                headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Course(result, self._auth, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def get_all_questions(self, status=None, course=None, ordering=None):
        if not course:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/questions/"
                "?status={}"
                "&fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}".format(status, ordering),
                headers=self._auth).json()
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/questions/"
                "?status={}"
                "&course={}"
                "&fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}".format(status, course, ordering),
                headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Question(result, self._auth, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def get_all_reviews(self, status=None, course=None, stars=None, ordering=None):
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
                "&ordering={}".format(status, stars, ordering),
                headers=self._auth).json()
        else:
            response = requests.get(
                "https://www.udemy.com/instructor-api/v1/taught-courses/reviews/"
                "?status={}"
                "&course={}"
                "&star={}"
                "&fields%5Bcourse_review%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                "&ordering={}".format(status, course, stars, ordering),
                headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Review(result, self._auth, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def get_course_questions(self, course_id, ordering=None):
        response = requests.get("https://www.udemy.com/instructor-api/v1/courses/{}/questions/"
                                "?fields%5Bquestion%5D=@all&fields%5Banswer%5D=@all&fields%5Bcourse%5D=@all&fields%5Buser%5D=@all"
                                "&ordering={}".format(course_id, ordering),
                                headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Question(result, self._auth, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def get_course_replies(self, course_id, question_id, ordering=None):
        response = requests.get("https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/replies/"
                                "?fields%5Banswer%5D=@all&fields%5Buser%5D=@all"
                                "&ordering={}".format(course_id, question_id, ordering),
                                headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Reply(result, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def delete_question(self, course_id, pk):
        requests.delete(
            'https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/'.format(course_id, pk),
            headers=self._auth)

    def get_message_threads(self, status=None, other_user=None):
        if other_user:
            response = requests.get("https://www.udemy.com/instructor-api/v1/message-threads/"
                                    "?fields%5Bmessage_thread%5D=@all&fields%5Bmessage%5D=@all&fields%5Buser%5D=@all"
                                    "&status={}"
                                    "&other_user={}".format(status, other_user),
                                    headers=self._auth).json()
        else:
            response = requests.get("https://www.udemy.com/instructor-api/v1/message-threads/"
                                    "?fields%5Bmessage_thread%5D=@all&fields%5Bmessage%5D=@all&fields%5Buser%5D=@all"
                                    "&status={}".format(status),
                                    headers=self._auth).json()
        while True:
            for result in response['results']:
                yield Thread(result, self)
            if not response['next']:
                break
            response = requests.get(response['next'], headers=self._auth).json()

    def post_question_response(self, course_id, question_id, body):
        response = requests.post('https://www.udemy.com/instructor-api/v1/courses/{}/questions/{}/replies'.format(course_id, question_id),
                                 headers=self._auth,
                                 data=json.dumps(body))

    def post_message(self, message_thread_id, body):
        response = requests.post('https://www.udemy.com/instructor-api/v1/message-threads/{}/messages/'.format(message_thread_id),
                                 headers=self._auth,
                                 data=json.dumps(body))
