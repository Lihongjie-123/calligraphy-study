import configparser
import logging
import os
import sys

workdir = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)


def get_config_conf():
    try:
        config_map = {}
        config = configparser.ConfigParser()

        config.read(os.path.join(workdir,
                                 'etc', 'config.conf'),
                    encoding='utf-8')
        # presto 配置
        config_map["each_level_wait_time"] = \
            config.get('setting', 'each_level_wait_time').split(",")

        return config_map
    except Exception as exception:
        logging.exception(exception)
        sys.exit(1)
