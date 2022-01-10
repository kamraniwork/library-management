# Library management API system

## list book
* ###### Request: `GET`  `http://localhost:8000/book/book/`
* ###### Param: `None`
* ###### Response: 
    ```json
      [
        {
            "url": string,
            "name": string,
            "slug": string,
            "category": list,
            "status": string
        }
      ]
    ```
    