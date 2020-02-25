
class Question:
    def __init__(self, question_dict, _parent):
        self._parent = _parent
        self._raw = question_dict
        self.content = question_dict['body']
        self.course = Course(question_dict['course'], _parent)
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

    @property
    def replies(self):
        for reply in self.reply_raw:
            yield Reply(reply, self._parent)

    def delete(self):
        self._parent.delete_question(self.course.id, self.id)

    def post_question_response(self, body):
        self._parent.post_question_response(self.course.id, self.id, body)

    def update_question(self, read):
        self._parent.update_question(self.course.id, self.id, read)

    def update_question_reply(self, response_id, is_top_answer=None, body=None):
        self._parent.update_question_reply(self.course.id, self.id, response_id, is_top_answer, body)

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.id == other.id
        else:
            return False


class Course:
    def __init__(self, course_dict, _parent):
        self._parent = _parent
        self._raw = course_dict
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

    def get_reviews(self, status='', stars=None, ordering=''):
        if stars is None:
            stars = []
        yield from self._parent.get_all_reviews(course=self.id, status=status, stars=stars, ordering=ordering)

    def get_questions(self, ordering=''):
        yield from self._parent.get_course_questions(self.id, ordering=ordering)

    def get_question_replies(self, question_id, ordering=''):
        yield from self._parent.get_question_replies(self.id, question_id, ordering=ordering)

    def delete_question(self, pk):
        self._parent.delete_question(self.id, pk)

    def post_question_response(self, question_id, body):
        self._parent.post_question_response(self.id, question_id, body)

    def update_question(self, question_id, body):
        self._parent.update_question(self.id, question_id, body)

    def update_question_reply(self, question_id, response_id, is_top_answer=None, body=None):
        self._parent.update_question_reply(self.id, question_id, response_id, is_top_answer, body)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.id == other.id
        else:
            return False


class Review:
    def __init__(self, review_dict, _parent):
        self._parent = _parent
        self._raw = review_dict
        self.id = review_dict['id']
        self.content = review_dict['content']
        self.course = Course(review_dict['course'], _parent)
        self.created = review_dict['created']
        self.stars = review_dict['rating']
        try:
            self.response = Response(review_dict['response'], _parent)
        except TypeError:
            self.response = None
        self.user = User(review_dict['user'], _parent)
        self.user_modified = review_dict['user_modified']

    def __eq__(self, other):
        if isinstance(other, Review):
            return self.id == other.id
        else:
            return False


class Response:
    def __init__(self, response_dict, _parent):
        self._parent = _parent
        self._raw = response_dict
        self.content = response_dict['content']
        self.created = response_dict['created']
        self.modified = response_dict['modified']
        self.user = User(response_dict['user'], _parent)
        self.id = response_dict['id']

    def __eq__(self, other):
        if isinstance(other, Response):
            return self.id == other.id
        else:
            return False


class Reply:
    def __init__(self, reply_dict, _parent):
        self._parent = _parent
        self._raw = reply_dict
        self.created = reply_dict['created']
        self.last_activity = reply_dict['last_activity']
        self.user = User(reply_dict['user'], _parent)
        if reply_dict['is_top_answer']:
            self.is_top_answer = reply_dict['is_top_answer']
        else:
            self.is_top_answer = False
        self.content = reply_dict['body']
        self.is_upvoted = reply_dict['is_upvoted']
        self.num_upvotes = reply_dict['num_upvotes']
        self.id = reply_dict['id']

    def __eq__(self, other):
        if isinstance(other, Reply):
            return self.id == other.id
        else:
            return False


class Message:
    def __init__(self, message_dict, _parent):
        self._parent = _parent
        self._raw = message_dict
        self.content = message_dict['content']
        self.created = message_dict['created']
        self.id = message_dict['id']
        self.is_outgoing = message_dict['is_outgoing']
        self.user = User(message_dict['user'], _parent)

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.id == other.id
        else:
            return False


class User:
    def __init__(self, user_dict, _parent):
        self._parent = _parent
        self._raw = user_dict
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
        self._raw = thread_dict
        self.created = thread_dict['created']
        self.id = thread_dict['id']
        self.is_read = thread_dict['is_read']
        self.is_starred = thread_dict['is_starred']
        self.last_message = Message(thread_dict['last_message'], _parent)
        self.other_user = User(thread_dict['other_user'], _parent)

    def post_message(self, body):
        self._parent.post_message(self.id, body)

    def update_thread_detail(self, is_read=None, is_starred=None, is_deleted=None, is_muted=None):
        self._parent.update_thread_detail(self.id, is_read, is_starred, is_deleted, is_muted)

    def get_messages(self):
        yield from self._parent.get_messages(self.id)

    def __eq__(self, other):
        if isinstance(other, Thread):
            return self.id == other.id
        else:
            return False