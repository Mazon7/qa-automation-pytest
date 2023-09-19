import random
import string

# Get random name
letters = string.ascii_letters
random_name = 'RandomSubject_' + \
    "".join(random.choice(letters) for i in range(10))


class AdminSubjectData:
    free_data = {
        "title": random_name,
        "descriptions": "Test Subject with Free Tariff for Autotests",
        "descriptions_link": "https://example.com/",
        "is_active": True,
        "access_type": "free",
        "language": "all",
        "is_shadow": False,
        "trial_period_days": None,
        "tariffs": [],
    }

    trial_data = {
        "title": random_name,
        "descriptions": "Test Subject with Trial Tariff for Autotests",
        "descriptions_link": "https://example.com/",
        "is_active": True,
        "access_type": "trial",
        "language": "all",
        "is_shadow": False,
        "trial_period_days": 30,
        "tariffs": [{
            "currency": "rub",
            "discount": 0,
            "interval": "month",
            "is_active": True,
            "is_recurring_pay": False,
            "period": 1,
            "price": 1
        }],
    }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
