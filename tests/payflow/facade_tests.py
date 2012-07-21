from decimal import Decimal as D

from django.test import TestCase
from oscar.apps.payment.utils import Bankcard
import mock

from paypal.payflow import facade
from paypal.payflow import models

"""
See page 49 of the PDF for information on PayPal's testing set-up
"""

class TestAuthorize(TestCase):

    def setUp(self):
        self.card = Bankcard(
            card_number='4111111111111111',
            name='John Doe',
            expiry_date='12/13',
        )

    def authorize(self):
        return facade.authorize('1234', self.card, D('10.00'))

    def test_returns_nothing_when_txn_is_approved(self):
        with mock.patch('paypal.payflow.gateway.authorize') as mock_f:
            mock_f.return_value = models.PayflowTransaction(
                result='0'
            )
            self.assertIsNone(self.authorize())

    def test_raises_exception_when_not_approved(self):
        with mock.patch('paypal.payflow.gateway.authorize') as mock_f:
            mock_f.return_value = models.PayflowTransaction(
                result='1'
            )
            with self.assertRaises(facade.NotApproved):
                self.authorize()

    def test_not_approved_exception_contains_useful_message(self):
        with mock.patch('paypal.payflow.gateway.authorize') as mock_f:
            mock_f.return_value = models.PayflowTransaction(
                result='23',
                respmsg='Invalid account number',
            )
            try:
                self.authorize()
            except facade.NotApproved, e:
                self.assertEqual("Invalid account number", e.message)