import company.package.config
import ConfigParser

import mock

import pytest

import unittest


from company.package.config import DEFAULT_CONFIG_FILE


class LoadTestCase(unittest.TestCase):
    """
    Tests for the company.package.config.load_configuration() function.
    """

    def setUp(self):
        # mock of logging.RootLogger
        self.patch_get_logger = mock.patch('company.package.config.logging.getLogger')
        self.mock_get_logger = self.patch_get_logger.start()

        self.mock_root_logger = self.mock_get_logger.return_value
        self.mock_root_logger.debug.return_value = None
        self.mock_root_logger.error.return_value = None
        self.mock_root_logger.info.return_value = None

        self.addCleanup(self.patch_get_logger.stop)

    @mock.patch('company.package.config.os.path')
    @mock.patch('company.package.config.ConfigParser.read')
    def test_load_configuration(self, mock_read, mock_path):
        """
        Test company.package.config.load_configuration() when configuration file exists.
        """
        mock_path.exists.return_value = True
        mock_path.isfile.return_value = True
        mock_read.return_value = None

        company.package.config.load_configuration()

        mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)
        mock_read.assert_called_with(DEFAULT_CONFIG_FILE)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.info.assert_called_once_with(
            '%s configuration file was loaded.' % DEFAULT_CONFIG_FILE)

    @mock.patch('company.package.config.os.path')
    @mock.patch('company.package.config.ConfigParser.read')
    def test_load_configuration_nofile(self, mock_read, mock_path):
        """
        Test company.package.config.load_configuration() when the configuration file doesn't exist.
        """
        mock_path.exists.return_value = True
        mock_path.isfile.return_value = False
        mock_read.return_value = None

        with pytest.raises(ValueError):
            company.package.config.load_configuration()

        mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)

        self.assertFalse(mock_read.readConfig.called)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.error.assert_called_once_with(
            '%s configuration file does not exist!' % DEFAULT_CONFIG_FILE)

    @mock.patch('company.package.config.os.path')
    @mock.patch('company.package.config.ConfigParser.read')
    def test_load_configuration_errors(self, mock_read, mock_path):
        """
        Test company.package.config.load_configuration() when NoSectionErrors are raised.
        """
        mock_path.exists.return_value = True
        mock_path.isfile.return_value = True
        mock_read.side_effect = ConfigParser.NoSectionError("No section: 'formatters'")

        company.package.config.load_configuration()

        mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)

        self.assertFalse(mock_read.readConfig.called)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.error.assert_called_once_with(
            'Failed to load configuration from %s!' % DEFAULT_CONFIG_FILE)
        self.mock_root_logger.debug.assert_called_once_with(
            str(ConfigParser.NoSectionError("No section: 'formatters'")), exc_info=True)


class GetTestCase(unittest.TestCase):
    """
    Tests for the company.package.config.get() function.
    """
