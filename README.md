# **PYTHON-UDEMY**
_A better python wrapper for the Udemy Instructor API_

## Install
Install  
`$ pip install python-udemy`

Use  
`>>> from udemy import Api`

## Authenticate
In order to use this module, you must supply an instructor API token. 
This can be created by logging into Udemy and creating an instructor API client. 
Once you have generated the token, the API can be set up with:

`>>> udemy_api = Api(<TOKEN>)`

## Use
Here's a few examples of ways you can use this wrapper.
### Courses
Here's a simple script to get all the unanswered questions from each course.

    for course in udemy_api.get_all_courses():
        print("Getting questions for", course.title)
        for question in course.get_questions(status="unanswered"):
            print("Unanswered question from", question.user.title)
            print(question.title)
            print(question.content)
        
### Reviews
Or to get all your bad reviews.

    for review in udemy_api.get_all_reviews(stars=[1, 2, 3], page_size=100):
        print("\nBad review from", review.user.name, ":(")
        print(review.stars, "stars")
        print(review.content)
    

### Everything Else
These are just a couple examples of what you can accomplish with this wrapper. Anything
you can see on the API is possible, and I will try my best to update this if any changes
are made. If you have any issues or errors, please log a issue on the GitHub repo. Want 
to add a feature? Submit a pull request!


## Philosophy
The design philosophy behind this API wrapper was to abstract away as much of the 
annoying raw json processing as possible. Unlike every other Udemy API wrappers, each
model is represented as an object with easily accessible attributes holding the data you
want. This wrapper also handles pagination for you, wrapping it up in a generator you can
easily iterate through. However, another one of my goals was to not remove any functionality 
of the original API. Every option shown in the docs is still available, including setting
manual pages, page sizes, ordering, and filtering. Most of the names in the API are
unchanged, however a few were changed to more sensible alternatives, such as the Answer
'body' to 'content' in order to stay consistent with the other models. 

## TODO
* Write docs
* Add C O M M E N T S
* Make additional helper functions
* Add Affiliate API
* Add private API?
* Figure out the meaning of Life
