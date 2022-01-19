'''
utils.py: kimsufi's utilities.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import configparser
import logging
import os.path
import sys

DEFAULT_CONFIG_PATH = '../config/kimsufi.conf'
SECTION_DEFAULT_NAME = 'GENERAL'
API_URL_NAME = 'API_URL'
SECTION_ZONES_NAME = 'ZONES'
ID_SERVERS_NAME = 'ID_SERVERS'
POLLING_INTERVAL_NAME = 'POLLING_INTERVAL'
LOG_LEVEL_NAME = 'LOG_LEVEL'
SECTION_HTTP_REQUEST_NAME = 'HTTP_REQUEST'
HTTP_REQUEST_FOUND_NAME = 'REQUEST_FOUND'
HTTP_REQUEST_NOT_FOUND_NAME = 'REQUEST_NOT_FOUND'
SECTION_EMAIL_NAME = 'EMAIL'
EMAIL_SMTP_SERVER_NAME = 'SMTP_SERVER'
EMAIL_SMTP_PORT_NAME = 'SMTP_PORT'
EMAIL_SMTP_FROM_NAME = 'SMTP_FROM'
EMAIL_SMTP_PASSWORD_NAME = 'SMTP_PASSWORD'
EMAIL_SMTP_TO_NAME = 'SMTP_TO'
SECTION_TELEGRAM_NAME = 'TELEGRAM'
TELEGRAM_TOKEN_NAME = 'TOKEN'
TELEGRAM_CHATID_NAME = 'CHATID'
SECTION_DISCORD_NAME = 'DISCORD'
DISCORD_WEBHOOK_TOKEN = 'WEBHOOK_TOKEN'
logger = logging.getLogger('kimsufi')

def open_and_load_config(args):
    if args.config_path:
        config_path = args.config_path
    else:
        config_path = DEFAULT_CONFIG_PATH
    config = configparser.ConfigParser()

    if os.path.isfile(config_path):
        try:
            config.read(config_path)
        except configparser.ParsingError as exc:
            logger.critical('Parsing error=%s', str(exc))
            sys.exit(1)
    else:
        logger.critical('config_path=%s not found', config_path)
        sys.exit(1)

    check_config(config)

    return config

def check_config(config):
    # Check at least a section of notification exists
    if (not is_config_section(config, SECTION_HTTP_REQUEST_NAME)
            and not is_config_section(config, SECTION_EMAIL_NAME)
            and not is_config_section(config, SECTION_TELEGRAM_NAME)
            and not is_config_section(config, SECTION_DISCORD_NAME)):
        logger.warning('No section of notification found in the config file, just logs will be done.')

    # Check the mandatories keys and sections
    check_config_section(config, SECTION_ZONES_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, API_URL_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, ID_SERVERS_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, POLLING_INTERVAL_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, LOG_LEVEL_NAME)

    # Check notifications sections
    if is_config_section(config, SECTION_HTTP_REQUEST_NAME):
        check_config_key(config, SECTION_HTTP_REQUEST_NAME, HTTP_REQUEST_FOUND_NAME)
        check_config_key(config, SECTION_HTTP_REQUEST_NAME, HTTP_REQUEST_NOT_FOUND_NAME)
    if is_config_section(config, SECTION_EMAIL_NAME):
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_SERVER_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_PORT_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_FROM_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_PASSWORD_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_TO_NAME)
    if is_config_section(config, SECTION_TELEGRAM_NAME):
        check_config_key(config, SECTION_TELEGRAM_NAME, TELEGRAM_TOKEN_NAME)
        check_config_key(config, SECTION_TELEGRAM_NAME, TELEGRAM_CHATID_NAME)
    if is_config_section(config, SECTION_DISCORD_NAME):
        check_config_key(config, SECTION_DISCORD_NAME, DISCORD_WEBHOOK_TOKEN)

def is_config_section(config, section):
    if config.has_section(section):
        return True
    return False

def is_config_key(config, section, key):
    if config.has_option(section, key):
        return True
    return False

def check_config_section(config, section):
    if not is_config_section(config, section):
        logger.critical('No section=%s in config file', section)
        sys.exit(1)

def check_config_key(config, section, key):
    if not is_config_key(config, section, key):
        logger.critical('No key=%s in section=%s in config file', key, section)
        sys.exit(1)

def check_python_version():
    if sys.version_info <= (3, 9):
        logger.critical('The script needs at least python 3.9')
        sys.exit(1)

