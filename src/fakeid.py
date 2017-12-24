import json
import random
import math
import datetime
import string
import uuid
import sys
import inspect
import os


def get_default_lists():

    routes = json.loads(open( os.path.join(os.path.dirname(__file__),  '../datasets/routes.json'), 'r').read())
    
    defaults = {}

    for k, v in routes["defaults"].items():
        
        defaults[k] = []
        
        for wordlist in v:
            defaults[k].extend(open( os.path.join(os.path.dirname(__file__), "../datasets/" + routes["lists"][k][wordlist]), "r").readlines())

    return defaults


def pretty_print(value, code, newline=True):
    
    s = "\x1b[{}m{}\x1b[0m".format(value, code)

    if newline:
        s += '\n'

    sys.stdout.write(s)

class FakeID:

    def __init__(self, lists=get_default_lists()):
        
        # Normalize by stripping newlines
        # Also remove any lines that start with `#`, as well as empty strings
        # Remove duplicates too

        for k, v1 in lists.items():
            
            to_delete = []

            for i, v2 in enumerate(v1):

                lists[k][i] = v2.replace('\n', '')

                if v2.startswith('#') or v2 == '':
                    to_delete.append(i)

            to_delete = sorted(to_delete, reverse=True)

            for i in to_delete:

                lists[k].pop(i)

            lists[k] = list(set(lists[k]))


        self.lists = lists
        random.seed()

        
        self.information = {}
        
        # These need to be called before other methods because other methods rely on them and inspect.getmembers is a dict (unsorted)
        called_before = [
            "_first_name",
            "_middle_name",
            "_last_name"
            
        ]

        excluded = [
                
            "__init__",
            "print"
        ]


        for b in called_before:

            self.information[b[1:]] = getattr(self, b)()
            
        for k, v in inspect.getmembers(self, predicate=inspect.ismethod):
            
            
            if k in called_before or k in excluded:
                continue
            
            self.information[k[1:]] = v()


        self.information["age"] = self.information["age_and_birthday"][0]
        self.information["birthday"] = self.information["age_and_birthday"][1]

        self.information.pop("age_and_birthday")

        self.information["mother's_maiden_name"] = self._last_name()
    

    def print(self, pretty=True):
        
        order = [
            "full_name",
            "address",
            "[[]]",
            "mother's_maiden_name",
            "SSN",
            "[[PHONE:]]",
            "phone_number",
            "country_code",
            "[[BIRTHDAY:]]",
            "birthday",
            "age",
            "[[ONLINE:]]",
            "email_address",
            "username",
            "password",
            "website",
            "user_agent",
            "[[FINANCE:]]",
            "credit_card",
            "expiry_date",
            "CVC2",
            "[[EMPLOYMENT:]]",
            "company",
            "occupation",
            "[[PHYSICAL CHARACTERISTICS:]]",
            "height",
            "weight",
            "blood_type",
            "[[TRACKING NUMBERS:]]",
            "UPS_tracking_number",
            "Western_Union_MTCN",
            "MoneyGram_MTCN",
            "[[OTHER:]]",
            "GUID"

        ]

        for k in order:
            
            if k.startswith("[[") and k.endswith("]]"):

                print()

                if pretty:
                    pretty_print("2;30;47", k[2:-2])

                else:
                    print(k[2:-2])

                print()
                continue

            else:

                key = ' '.join(x[0].upper() + x[1:] for x in k.split('_'))
                value = self.information[k]
                

                if pretty:

                    pretty_print('1;31;43', key, False)
                    sys.stdout.write(": ")
                    pretty_print('1;37;44', value, True)

                else:
                    print("{}: {}".format(key, value))
        
        
    def _first_name(self):
        
        return random.choice(self.lists["firstnames"]).capitalize()
    
    def _middle_name(self):

        return "{}.".format(random.choice(string.ascii_uppercase))

    def _last_name(self):
        
        return random.choice(self.lists["lastnames"]).capitalize()

    
    def _full_name(self):
        return "{} {} {}".format(self.information["first_name"], self.information["middle_name"], self.information["last_name"])
    
    def _address(self):
        return random.choice(self.lists["addresses"])
    
    def _SSN(self):
        return "{}-{}-{}".format \
        (
        ''.join(random.choice(string.digits) for i in range(3)),
        ''.join(random.choice(string.digits) for i in range(2)),
        ''.join(random.choice(string.digits) for i in range(4))
        )

    def _phone_number(self):
        
        return "{}-{}-{}".format \
        ( 
        ''.join(random.choice(string.digits) for i in range(3)),
        ''.join(random.choice(string.digits) for i in range(3)),
        ''.join(random.choice(string.digits) for i in range(4)),
        )

    def _age(self):
        return str(random.randint(21, 75))
    
    def _company(self):
        return random.choice(self.lists["businesses"])

    def _occupation(self):
        return random.choice(self.lists["occupations"])


    def _country_code(self):
        return '1';

    def _age_and_birthday(self):
        
       # No 29th day in February because that adds an unnecessary layer of complexity (need to make year dividible by 4)
        days_in_month = [
            31, 28, 31, 30,
            31, 30, 31, 31,
            30, 31, 30, 31
        ]
        month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        now = datetime.datetime.now()
        age = random.randint(21, 75)
        yearborn = now.year - age
        monthborn = random.randint(0, 11)
        dayborn = random.randint(1, days_in_month[monthborn])
        dayborn_ord = str(dayborn)

        if dayborn_ord[-1] == '1':
            dayborn_ord += "st"
        elif dayborn_ord[-1] == '2':
            dayborn_ord += "nd"
        elif dayborn_ord[-1] == '3':
            dayborn_ord += "rd"
        else:
            dayborn_ord += "th"

        if monthborn + 1 >= now.month and dayborn > now.day:

            age -= 1
        
        return age, "{} {}, {}".format(month_names[monthborn], dayborn_ord, yearborn)
    
    def _email_address(self):
        
        domain = random.choice(self.lists["emailproviders"])

        username = (self.information["first_name"] + "." + self.information["last_name"]).lower()

        return "{}@{}".format(username, domain)

    def _username(self):

        def random_word():
            return random.choice(self.lists["words"]).replace('\'', '').lower().capitalize()

        return random_word() + random_word()
    
    def _password(self):

        return ''.join(random.choice(string.digits + string.ascii_letters + string.punctuation) for i in range(random.randint(8, 16)))
    
    def _website(self):

        def random_word():
            return random.choice(self.lists["words"]).replace('\'', '').lower()

        return "http://" + random_word() + random_word() + "." + random.choice(self.lists["TLDs"])
        
    def _user_agent(self):

        return random.choice(self.lists["useragents"])

    def _GUID(self):
        return str(uuid.uuid4())


    def _blood_type(self):

        blood_types = [
            "O+", "O-",
            "A+", "A-",
            "B+", "B-",
            "AB+", "AB-"
        ]

        return random.choice(blood_types)

    def _UPS_tracking_number(self):
 
        return "1Z" + ''.join( random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

    def _Western_Union_MTCN(self):

        return ''.join(random.choice(string.digits) for _ in range(10))
    
    def _MoneyGram_MTCN(self):
        return ''.join(random.choice(string.digits) for _ in range(8))

    def _weight(self):

        weight_pounds = random.uniform(110.0, 190.0)
        
        return "{} pounds ({} KG)".format(round(weight_pounds, 1), round(weight_pounds / 2.20462262, 2))

    def _height(self):

        height_inches = random.randint(5 * 12, 6 * 12)

        height_ft_inches = "{}' {}\"".format(math.floor(height_inches / 12), height_inches % 12)

        return "{} ({} cm)".format(height_ft_inches, height_inches * 2.54)

    def _credit_card(self):
        return "{} {} {} {}".format \
        ( 
        ''.join(random.choice(string.digits) for i in range(4)),
        ''.join(random.choice(string.digits) for i in range(4)),
        ''.join(random.choice(string.digits) for i in range(4)),
        ''.join(random.choice(string.digits) for i in range(4)),
        )
    def _expiry_date(self):
        
        month = random.randint(1, 12)

        month_str = str(month)

        if month < 10:
            month_str = '0' + month_str 

        return "{}/{}".format(month_str, datetime.datetime.now().year + random.randint(1, 15))

    def _CVC2(self):
        return ''.join(random.choice(string.digits) for i in range(3))

if __name__ == "__main__":
    

    test = FakeID()

    test.print()
