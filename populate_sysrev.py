import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sysrevt.settings')

import django
django.setup()

#As for now I just added the three test users as specified in the email
#I will then put mock data accordingly to the format we will find during development
from sysrev.models import Researcher


def populate():

    add_researcher(
        username='jill',
        password='jill',
        email='jillTEST@research.gla.ac.uk',
        forename='Jill',
        surname='McTracy',
        institution='GLA'
    )

    add_researcher(
        username='jim',
        password='jim',
        email='jimTEST@research.gcu.ac.uk',
        forename='Jim',
        surname='Robertson',
        institution='GCU'
    )

    add_researcher(
        username='joe',
        password='joe',
        email='joeTEST@research.ox.ac.uk',
        forename='Joe',
        surname='Tudor',
        institution='OXF'
    )

    # Print out what we have added to the user.
    for r in Researcher.objects.all():
            print "- {0} - {1}".format(str(r))

def add_researcher(username, password, email, forename,surname,institution):
    r = Researcher.objects.get_or_create(
        username=username,
        password=password,
        email=email,
        forename=forename,
        surname=surname,
        institution=institution)[0]
    r.url=url
    r.views=views
    r.save()
    return r


# Start execution here!
if __name__ == '__main__':
    print "Adding the default users(researchers)"
    populate()