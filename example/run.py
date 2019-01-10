import string
from random import choice, randint, seed

import names

from app.app import app
from app.db import db, Person, Item


def random_string(n):
    return u"".join(choice(string.ascii_letters + string.digits) for _ in range(n))


def unique_name(existing, name_func):
    while True:
        name = name_func()
        if name not in existing:
            existing.add(name)
            return name


SEED = 53
N_PERSONS = 23
N_ITEMS = 113
TITLE_LEN = 10

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed(SEED)
        person_names = set()
        persons = [Person(name=unique_name(person_names, names.get_full_name)) for _ in range(N_PERSONS)]
        for x in persons:
            db.session.add(x)
        db.session.flush()


        def random_person_id():
            return persons[randint(0, N_PERSONS - 1)].id


        title_names = set()
        items = [Item(title=unique_name(title_names, lambda: random_string(TITLE_LEN)), owner_id=random_person_id(),
                      holder_id=random_person_id()) for _ in range(N_ITEMS)]
        for x in items:
            db.session.add(x)
        db.session.commit()

    app.run(debug=True)
