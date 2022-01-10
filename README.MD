# Library management API system

## list book
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
    *   `name`: required | string
    *   `slug`: required | string
    *   `category`: not required | list
    *   `description`: not required | string
    *   `author`: required | string
    
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
