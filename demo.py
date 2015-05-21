#!/usr/bin/env python
import os
import sys

# CAUTION! This line is only used for a development environment, when pywps is not installed
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.pardir))

from server import Server
from processes.sleep import Sleep
from processes.ultimate_question import UltimateQuestion
from processes.centroids import Centroids
from processes.sayhello import SayHello
from processes.feature_count import FeatureCount
from processes.buffer import Buffer
from processes.area import Area


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--waitress', action='store_true')
    args = parser.parse_args()

    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pywps.cfg")

    processes = [
        FeatureCount(),
        SayHello(),
        Centroids(),
        UltimateQuestion(),
        Sleep(),
        Buffer(),
        Area()
    ]

    s = Server(processes=processes, config_file=config_file)

    # TODO: need to spawn a different process for different server
    if args.waitress:
        import waitress
        from pywps import config

        config.load_configuration(config_file)
        host = config.get_config_value('wps', 'serveraddress').split('://')[1]
        port = int(config.get_config_value('wps', 'serverport'))

        waitress.serve(s.app, host=host, port=port)
    else:
        s.run()


if __name__ == '__main__':
    main()
