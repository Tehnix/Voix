import unittest
import mox

from voix.client import Client
from voix.parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.parser = Parser(self.client)
        self.mock_parser = mox.Mox()

    def test_that_setting_hostname_is_successful(self):
        self.parser.parse('HOST: localhost')
        self.assertEquals(self.client.host, 'localhost')

    def test_that_setting_port_is_successful(self):
        self.parser.parse('PORT: 1337')
        self.assertEquals(self.client.port, '1337')

    def test_that_connecting_without_setting_hostname_raises_exception(self):
        self.assertRaises(Warning, self.client.connect, ['joe', 'Juice'])


if __name__ == '__main__':
    unittest.main()
