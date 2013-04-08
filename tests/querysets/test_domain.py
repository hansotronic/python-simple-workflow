# -*- coding:utf-8 -*-

import unittest2

from mock import patch

from boto.exception import SWFResponseError

from swf.core import set_aws_credentials
from swf.exceptions import (ResponseError, DoesNotExistError,
                            InvalidCredentialsError)
from swf.models.domain import Domain
from swf.querysets.domain import DomainQuerySet

from ..mocks.domain import mock_describe_domain, mock_list_domains

set_aws_credentials('fakeaccesskey', 'fakesecretkey')


class TestDomainQuerySet(unittest2.TestCase):
    def setUp(self):
        self.domain = Domain("test-domain")
        self.qs = DomainQuerySet()

    def tearDown(self):
        pass

    def test_get_existent_domain(self):
        with patch.object(self.qs.connection, 'describe_domain', mock_describe_domain):
            domain = self.qs.get("test-domain")
            self.assertIsInstance(domain, Domain)

            self.assertTrue(hasattr(domain, 'name'))
            self.assertEqual(domain.name, 'test-domain')

            self.assertTrue(hasattr(domain, 'status'))
            self.assertEqual(domain.status, self.domain.status)

    def test_get_non_existent_domain(self):
        with patch.object(self.qs.connection, 'describe_domain') as mock:
            with self.assertRaises(DoesNotExistError):
                mock.side_effect = SWFResponseError(
                    400,
                    "mocking exception",
                    {'__type': 'UnknownResourceFault'}
                )
                self.qs.get('non_existent')

    def test_get_domain_with_invalid_credentials(self):
        with patch.object(self.qs.connection, 'describe_domain') as mock:
            with self.assertRaises(InvalidCredentialsError):
                mock.side_effect = SWFResponseError(
                    400,
                    "mocking exception",
                    {'__type': 'UnrecognizedClientException'}
                )
                self.qs.get('non_existent')

    def test_get_raising_domain(self):
        with patch.object(self.qs.connection, 'describe_domain') as mock:
            with self.assertRaises(ResponseError):
                mock.side_effect = SWFResponseError(
                    400,
                    "mocking exception",
                    {
                        '__type': 'WhateverError',
                        'message': 'WhateverMessage',
                    }
                )
                self.qs.get('whatever')

    def test_all_with_existent_domains(self):
        with patch.object(self.qs.connection, 'list_domains', mock_list_domains):
            domains = self.qs.all()
            self.assertEqual(len(domains), 1)
            self.assertIsInstance(domains[0], Domain)
