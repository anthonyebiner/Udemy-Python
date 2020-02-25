import unittest
import udemy


class MyTestCase(unittest.TestCase):
    def course_test(self, course):
        self.assertIsInstance(course, udemy.Course)
        self.assertIsInstance(course.created, str)
        self.assertIsInstance(course.description, str)
        self.assertIsInstance(course.headline, str)
        self.assertIsInstance(course.id, str)
        self.assertIsInstance(course.is_paid, bool)
        self.assertIsInstance(course.is_published, bool)
        if course.is_published:
            self.assertIsInstance(course.published_title, str)
        self.assertIsInstance(course.num_reviews, int)
        self.assertNotIsInstance(course.rating, str)
        self.assertIsInstance(course.title, str)
        self.assertIsInstance(course.url, str)
        self.assertIsNotNone(course.visible_instructors_raw)

    def review_test(self, review):
        self.assertIsInstance(review.id, str)
        self.assertIsInstance(review.content, str)
        self.assertIsInstance(review.course, udemy.Course)
        self.assertIsInstance(review.created, str)
        self.assertNotIsInstance(review.rating, str)
        self.assertIsInstance(review.user, udemy.User)
        self.assertIsInstance(review.user_modified, str)

    def question_test(self, question):
        self.assertIsInstance(question.content, str)
        self.assertIsInstance(question.course, udemy.Course)
        self.assertIsInstance(question.created, str)
        self.assertIsInstance(question.id, str)
        self.assertIsInstance(question.is_instructor, bool)
        self.assertIsInstance(question.is_read, bool)
        self.assertIsInstance(question.last_activity, str)
        self.assertIsInstance(question.modified, str)
        self.assertIsInstance(question.num_follows, int)
        self.assertIsInstance(question.num_replies, int)
        self.assertIsInstance(question.num_reply_upvotes, int)
        self.assertIsInstance(question.num_upvotes, int)
        self.assertIsInstance(question.related_lecture_id, str)
        self.assertIsInstance(question.related_lecture_title, str)
        self.assertIsInstance(question.related_lecture_url, str)
        self.assertIsNotNone(question.reply_raw)
        self.assertIsInstance(question.title, str)
        self.assertIsInstance(question.user, udemy.User)

    def reply_test(self, reply):
        self.assertIsInstance(reply.created, str)
        self.assertIsInstance(reply.last_activity, str)
        self.assertIsInstance(reply.user, udemy.User)
        self.assertIs(reply.is_top_answer, False)
        self.assertIsInstance(reply.content, str)
        self.assertIsInstance(reply.is_upvoted, bool)
        self.assertIsInstance(reply.num_upvotes, int)
        self.assertIsInstance(reply.id, str)

    def thread_test(self, thread):
        self.assertIsInstance(thread.created, str)
        self.assertIsInstance(thread.id, str)
        self.assertIsInstance(thread.is_read, bool)
        self.assertIsInstance(thread.is_starred, bool)
        self.assertIsInstance(thread.last_message, udemy.Message)
        self.assertIsInstance(thread.other_user, udemy.User)

    def message_test(self, message):
        self.assertIsInstance(message.content, str)
        self.assertIsInstance(message.created, str)
        self.assertIsInstance(message.id, str)
        self.assertIsInstance(message.is_outgoing, bool)
        self.assertIsInstance(message.user, udemy.User)

    def test_courses(self):
        api = udemy.Udemy(auths.udemy_api)
        courses = api.get_all_courses()
        self.assertIsNotNone(courses)
        num = 0
        for course in courses:
            if num > 50:
                break
            self.course_test(course)
            self.assertIsNotNone(course.get_reviews())
            num += 1

    def test_all_reviews(self):
        api = udemy.Udemy(auths.udemy_api)
        reviews = api.get_all_reviews()
        self.assertIsNotNone(reviews)
        num = 0
        for review in reviews:
            if num > 50:
                break
            self.review_test(review)
            num += 1

    def test_course_reviews(self):
        pass

    def test_questions(self):
        api = udemy.Udemy(auths.udemy_api)
        questions = api.get_all_questions(status='unanswered', ordering='oldest')
        self.assertIsNotNone(questions)
        num = 0
        for question in questions:
            if num > 20:
                break
            self.question_test(question)
            for reply in question.replies:
                self.reply_test(reply)
            num += 1

    def test_course_questions(self):
        api = udemy.Udemy(auths.udemy_api)
        courses = api.get_all_courses(ordering='popularity')
        self.assertIsNotNone(courses)
        num = 0
        for course in courses:
            if num > 10:
                break
            num2 = 0
            for question in course.get_questions():
                if num2 > 20:
                    break
                self.question_test(question)
                num2 += 1
            num += 1

    def test_messages(self):
        api = udemy.Udemy(auths.udemy_api)
        threads = api.get_message_threads()
        self.assertIsNotNone(threads)
        for thread in threads:
            self.thread_test(thread)
            for message in thread.get_messages():
                self.message_test(message)
            self.assertIsNotNone(thread.get_messages())


if __name__ == '__main__':
    unittest.main()
