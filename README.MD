# Library management API system

1. [Book](#Book)
    *   [list](#list-book)
    *   [detail](#detail-book)
    *   [create](#detail-book)
    *   [update](#update-book)
    *   [delete](#delete-book)
1. [Issue](#Issue)
    *   [list](#list-issue)
    *   [detail](#detail-issue)
    *   [create](#create-issue)
    *   [update](#update-issue)
    *   [delete](#delete-issue)
    *   [list issue custom user](#list-issue-custom-user)
    *   [Request for renew issue book](#request-for-renew-issue-book)
    *   [Accept request for renew issue book](#accept-request-for-renew-issue-book)
    *   [Reject request for renew issue book](#reject-request-for-renew-issue-book)
    *   [Return issue book](#return-issue-book)
## Book
### list book
* ###### Description: 
    return all book for superuser but if user is not superuser return books that `status=p`
    
* ###### Request: `GET`  `http://localhost:8000/book/book/`
* ###### Param: `None`
* ###### Response:
    ```json
      [
        {
            "url": "http://localhost:8000/book/book/two-scoops-of-django/",
            "name": "two scoops of django 3.x",
            "slug": "two-scoops-of-django",
            "category": [
                {
                    "title": "اموزشی",
                    "slug": "learning"
                },
                {
                    "title": "برنامه نویسی",
                    "slug": "programming"
                },
                {
                    "title": "جنگو",
                    "slug": "django"
                }
            ],
            "status": "p"
        }
      ]   
    ```
## detail book
* ###### Description: 
    return detail all book for superuser but if user is not superuser return detail books that `status=p`
    
* ###### Request: `GET`  `http://localhost:8000/book/book/{slug}/`
* ###### Param:  `None`
* ###### Response:
    ```json
      {
        "name": "two scoops of django 3.x",
        "slug": "two-scoops-of-django",
        "category": [
            {
                "title": "اموزشی",
                "slug": "learning"
            },
            {
                "title": "برنامه نویسی",
                "slug": "programming"
            },
            {
                "title": "جنگو",
                "slug": "django"
            }
        ],
        "description": "About the E-Book\r\n540+ pages, 519 while in Alpha\r\n\r\nOnce again, we're releasing a book chock-full of material that will help you with your Django projects!\r\n\r\nIn Two Scoops of Django we introduce you to various tips, tricks, patterns, code snippets, and techniques that we’ve picked up over the years. This book is an update and expansion of previous editions:\r\n\r\nUpdated for Django 3.x (which will be maintained by the Django core team until at least April 2024!)\r\nUpdated to match changes in the Django ecosystem, with corrections and clarifications added thanks to the feedback of our readers and technical reviewers.\r\nUpdated for Python 3.8 and/or 3.9\r\nRevised material on nearly every topic within the book.\r\nNew material on GraphQL, Django REST Framework, security, forms, models, and more.\r\nTwo Scoops of Django 3.x: Best Practices for the Django Web Framework is available in PDF now, possibly Kindle, ePub, and print formats later.",
        "author": "ali",
        "jpublish": "27 آذر 1400 , ساعت 23 : 21 ",
        "status": "p"
      }
    ```
## create book
* ###### Description: 
    jsut superuser can create new book
    
* ###### Request: `post`  `http://localhost:8000/book/book/`
* ###### Param:
    *   `name`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `slug`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `category`: not required | ![](https://img.shields.io/static/v1?label=&message=list&color=red)
    *   `description`: not required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `author`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    
* ###### example:
    ```json
      {
        "name": "two scoops of django 3.x",
        "slug": "two-scoops-of-django",
        "category": [
               "learning",
                "programming",        
                "django"
        ],
        "description": "About the E-Book\r\n540+ pages, 519 while in Alpha\r\n\r\nOnce again, we're releasing a book chock-full of material that will help you with your Django projects!\r\n\r\nIn Two Scoops of Django we introduce you to various tips, tricks, patterns, code snippets, and techniques that we’ve picked up over the years. This book is an update and expansion of previous editions:\r\n\r\nUpdated for Django 3.x (which will be maintained by the Django core team until at least April 2024!)\r\nUpdated to match changes in the Django ecosystem, with corrections and clarifications added thanks to the feedback of our readers and technical reviewers.\r\nUpdated for Python 3.8 and/or 3.9\r\nRevised material on nearly every topic within the book.\r\nNew material on GraphQL, Django REST Framework, security, forms, models, and more.\r\nTwo Scoops of Django 3.x: Best Practices for the Django Web Framework is available in PDF now, possibly Kindle, ePub, and print formats later.",
        "author": "ali"
      }
    ```
## update book
* ###### Description: 
    jsut superuser can update book
    
* ###### Request: `put`  `http://localhost:8000/book/book/{slug}`
* ###### Param:
    *   `name`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `category`: not required | ![](https://img.shields.io/static/v1?label=&message=list&color=red)
    *   `description`: not required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `author`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    
* ###### example:
    ```json
      {
        "name": "two scoops of django 3.x",
        "category": [
               "learning",
                "programming",        
                "django"
        ],
        "description": "About the E-Book\r\n540+ pages, 519 while in Alpha\r\n\r\nOnce again, we're releasing a book chock-full of material that will help you with your Django projects!\r\n\r\nIn Two Scoops of Django we introduce you to various tips, tricks, patterns, code snippets, and techniques that we’ve picked up over the years. This book is an update and expansion of previous editions:\r\n\r\nUpdated for Django 3.x (which will be maintained by the Django core team until at least April 2024!)\r\nUpdated to match changes in the Django ecosystem, with corrections and clarifications added thanks to the feedback of our readers and technical reviewers.\r\nUpdated for Python 3.8 and/or 3.9\r\nRevised material on nearly every topic within the book.\r\nNew material on GraphQL, Django REST Framework, security, forms, models, and more.\r\nTwo Scoops of Django 3.x: Best Practices for the Django Web Framework is available in PDF now, possibly Kindle, ePub, and print formats later.",
        "author": "ali"
      }
    ```
## delete book
* ###### Description: 
    jsut superuser can delete book
    
* ###### Request: `delete`  `http://localhost:8000/book/book/{slug}`
* ###### Param: `None`

## Issue
### list issue
* ###### Description: 
    return all issue book for superuser. issue books that `status=d,p,q,d`
    
* ###### Request: `GET`  `http://localhost:8000/book/issue/`
* ###### Param: `None`
* ###### Response:
    ```json
      [
        {
          "url": "http://localhost:8000/book/issue/2/",
          "book": {
                "url": "http://localhost:8000/book/book/two-scoops-of-django/",
                "name": "two scoops of django 3.x",
                "slug": "two-scoops-of-django"
          },
          "user": 1,
          "renewCount": 1,
          "is_not_time": false
        }
      ]   
    ```
## detail issue
* ###### Description: 
    return detail issue book for superuser that `status=p,q,o,d`
    
* ###### Request: `GET`  `http://localhost:8000/book/issue/{pk}/`
* ###### Param:  `None`
* ###### Response:
    ```json
      {
        "book": {
            "name": "two scoops of django 3.x",
            "slug": "two-scoops-of-django",
            "category": [
                {
                    "title": "اموزشی",
                    "slug": "learning"
                },
                {
                    "title": "برنامه نویسی",
                    "slug": "programming"
                },
                {
                    "title": "جنگو",
                    "slug": "django"
                }
            ],
            "description": "About the E-Book\r\n540+ pages, 519 while in Alpha\r\n\r\nOnce again, we're releasing a book chock-full of material that will help you with your Django projects!\r\n\r\nIn Two Scoops of Django we introduce you to various tips, tricks, patterns, code snippets, and techniques that we’ve picked up over the years. This book is an update and expansion of previous editions:\r\n\r\nUpdated for Django 3.x (which will be maintained by the Django core team until at least April 2024!)\r\nUpdated to match changes in the Django ecosystem, with corrections and clarifications added thanks to the feedback of our readers and technical reviewers.\r\nUpdated for Python 3.8 and/or 3.9\r\nRevised material on nearly every topic within the book.\r\nNew material on GraphQL, Django REST Framework, security, forms, models, and more.\r\nTwo Scoops of Django 3.x: Best Practices for the Django Web Framework is available in PDF now, possibly Kindle, ePub, and print formats later.",
            "author": "ali",
            "jpublish": "27 آذر 1400 , ساعت 23 : 21 ",
            "status": "d"
        },
        "user": 1,
        "jpublish": "20 دی 1400 , ساعت 31 : 17 ",
        "renewCount": 1,
        "status": "p",
        "is_not_time": false
      }
    ```
## create issue
* ###### Description: 
    jsut superuser can create new book
    
* ###### Request: `post`  `http://localhost:8000/book/issue/`
* ###### Param:
    *   `user`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `book`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `renewCount`: not required | ![](https://img.shields.io/static/v1?label=&message=int&color=red)
    *   `status`: not required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    
* ###### example:
    ```json
      {
        "user": "mehran",
        "book": "two-scoops-of-django"
      }
    ```
## update issue
* ###### Description: 
    jsut superuser can update issue book
    
* ###### Request: `put`  `http://localhost:8000/book/issue/{pk}`
* ###### Param:
    *   `user`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `book`: required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    *   `renewCount`: not required | ![](https://img.shields.io/static/v1?label=&message=int&color=red)
    *   `status`: not required | ![](https://img.shields.io/static/v1?label=&message=string&color=red)
    
* ###### example:
    ```json
      {
        "user": "mehran",
        "book": "two-scoops-of-django",
        "renewCount": 1,
        "status": "d"
      }
    ```
## delete issue
* ###### Description: 
    jsut superuser can delete issue
    
* ###### Request: `delete`  `http://localhost:8000/book/issue/{pk}`
* ###### Param: `None`

### list issue custom user
* ###### Description: 
    return all issue book for authenticated user. issue books that `status=d,p,q,d`
    
* ###### Request: `GET`  `http://localhost:8000/book/issue/user_issue_list_book/`
* ###### Param: `None`
* ###### Response:
    ```json
      [
        {
          "url": "http://localhost:8000/book/issue/2/",
          "book": {
                "url": "http://localhost:8000/book/book/two-scoops-of-django/",
                "name": "two scoops of django 3.x",
                "slug": "two-scoops-of-django"
          },
          "user": 1,
          "renewCount": 1,
          "is_not_time": false
        }
      ]   
    ```
### Request for renew issue book
* ###### Description: 
    user can renew book and if accept by superuser `RenewCount +=1`
    
    superuser can go to `http://localhost:8000/book/issue/{pk}/user_issue_accept_renew` accept request or `http://localhost:8000/book/issue/{pk}/user_issue_reject_renew` reject it
* ###### Request: `GET`  `http://localhost:8000/book/issue/{pk}/user_issue_renew_request/`
* ###### Param: `None`
* ###### Response:
    ```json
      {
        "status": "please waite for accept request..."
      }   
    ```
### Accept request for renew issue book
* ###### Description: 
    user can renew book and if accept by superuser `RenewCount +=1`
    
* ###### Request: `GET`  `http://localhost:8000/book/issue/{pk}/user_issue_accept_renew`
* ###### Param: `None`
* ###### Response:
    ```json
      {
        "status": "you accept issue user "
      }   
    ```
### Reject request for renew issue book
* ###### Description: 
    user can renew book and if accept by superuser `RenewCount +=1` else `status=d`
    
* ###### Request: `GET`  `http://localhost:8000/book/issue/{pk}/user_issue_reject_renew`
* ###### Param: `None`
* ###### Response:
    ```json
      {
        "status": "you reject issue user "
      }   
    ```
### Return issue book 
* ###### Description: 
    return issue book by user and `status=k`
    
* ###### Request: `POST`  `http://localhost:8000/book/issue/{pk}/user_issue_return`
* ###### Param: `None`
* ###### Response:
    ```json
      {
        "status": "book return to library "
      }   
    ```
