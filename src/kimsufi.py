'''
kimsufi.py: kimsufi's main file.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''


import argparse
import json
import logging
import time
import signal
from os import getpid
import http1

import utils
import notifications

### GLOBAL VARIABLES ###
running = True

### LOGGING CONF ###
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
)
logger = logging.getLogger('imapmanager')

def signal_handler(_signal, _frame):
    global running
    running = False
    logger.info('Ending signal handled, ending the script...')

def main():
    logger.info('--------------------')

    # Check python3 is used
    utils.check_python_version()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', '-c', dest='config_path')
    args = parser.parse_args()

    # Open conf and load parameters
    config = utils.open_and_load_config(args)

    level = logging.getLevelName(config.get(utils.SECTION_DEFAULT_NAME, utils.LOG_LEVEL_NAME))
    logger.setLevel(level)

    api_url = config.get(utils.SECTION_DEFAULT_NAME, utils.API_URL_NAME)
    id_servers = config.get(utils.SECTION_DEFAULT_NAME, utils.ID_SERVERS_NAME).split(',')
    polling_interval = config.get(utils.SECTION_DEFAULT_NAME, utils.POLLING_INTERVAL_NAME)
    zones_desired = set()
    for zone in set(config.items(utils.SECTION_ZONES_NAME)):
        zones_desired.add(zone[1])

    last_status = False
    logger.info('Calling kimsufi API on url=%s with PID=%d', api_url, getpid())
    while running:
        server_found = False
        try:
            response = http1.get(api_url)
            if response.status == 200:
                struct = json.loads(response.body)
                for item in struct:
                    zones = [z['datacenter'] for z in item['datacenters'] if z['availability'] not in ('unavailable', 'unknown')]
                    if set(zones).intersection(zones_desired) and item['hardware'] in id_servers:
                        server_found = True
                        if not last_status:
                            logger.info('Found available server, sending notifications...')
                            notifications.send_notifications(config, True)
                            last_status = True
                        else:
                            logger.debug('Notification already sent, passing...')
                        # Do not iterate on other items as we already found an available server
                        break
                if not server_found:
                    logger.debug('No server available')
                    if last_status:
                        logger.info('Server not available anymore')
                        notifications.send_notifications(config, False)
                        last_status = False
            else:
                logger.error('Calling API: status=%d msg=%s', response.status, response.message)
        except Exception as exc:
            logger.error('Calling API: err=%s', str(exc))
        finally:
            # If signal occurs during process, there is no need to sleep
            if running:
                time.sleep(float(polling_interval))

    logger.info('kimsufi script ended.')

if __name__ == '__main__':
    main()

