import requests
import json


print(

    requests.post(

        "http://127.0.0.1:8000", 
        json = {

            "from_email":"cyriac.kodath@gmail.com",
            "content":"""
                Dear Jason
                I hope this message finds you well. I am Chinmayee from ABC Company;
                I am looking to purchase some company T shirts for my team of 10 people and we want 
                Please let me know the price and timeline you can work with;
                Looking forward
                Chinmayee

            """

        }
    ).json()

)

