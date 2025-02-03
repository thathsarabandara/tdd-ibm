"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_account_representation(self):
        account = Account()
        account.name = 'foo'
        self.assertEqual(account.__repr__(), '<Account foo>')

    def test_to_dict(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(result["name"],data.name)
        self.assertEqual(result["email"],data.email)
        self.assertEqual(result["phone_number"],data.phone_number)
        self.assertEqual(result["disabled"],data.disabled)
        self.assertEqual(result["date_joined"],data.date_joined)

    def test_from_dict(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account()
        account.from_dict(data)
        self.assertEqual(data["name"],account.name)
        self.assertEqual(data["email"],account.email)
        self.assertEqual(data["phone_number"],account.phone_number)
        self.assertEqual(data["disabled"],account.disabled)
        self.assertEqual(data["date_joined"],account.date_joined)

        def test_update_an_account(self):
            """ Test Account update using known data """
            data = ACCOUNT_DATA[self.rand] # get a random account
            account = Account(**data)
            account.create()
            self.assertIsNotNone(account.id)
            account.name = "Foo"
            account.update()
            found = Account.find(account.id)
            self.assertEqual(found.name, "Foo")

        def test_invalid_id_on_update(self):
            """ Test invalid ID update """
            data = ACCOUNT_DATA[self.rand] # get a random account
            account = Account(**data)
            account.id = None
            self.assertRaises(DataValidationError, account.update)

        def test_delete_an_account(self):
            """ Test Account update using known data """
            data = ACCOUNT_DATA[self.rand] # get a random account
            account = Account(**data)
            account.create()
            self.assertEqual(len(Account.all()), 1)
            account.delete()
            self.assertEqual(len(Account.all()), 0)
