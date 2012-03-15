
import os
import logging as log
import argparse

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DEFAULT_CONF_PATH = "etc/config.json"

import dokonico.env
import dokonico.core
import dokonico.app

class ArgParser:
    def __init__(self):
        self.init_parser()

    def init_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbose", action="store_true")
        parser.add_argument("--config", type=str, default=DEFAULT_CONF_PATH,
                metavar="filepath")
        subparsers = parser.add_subparsers(help="commands",dest="mode")

        self.init_sync_parser(subparsers)
        self.init_show_parser(subparsers)
        self.parser = parser

    def init_sync_parser(self, subpersers):
        sync_parser = subpersers.add_parser("sync", help="Execute sync")
        sync_parser.add_argument("-l", "--local", action="store_true")

    def init_show_parser(self, subparsers):
        show_parser = subparsers.add_parser("show", help="Show sessions.")

    def parse(self):
        return self.parser.parse_args()


class AppLoader:
    def __init__(self, conf="etc/config.json"):
        self.conf_path = conf

    def config(self):
        path = os.path.join(APP_ROOT, self.conf_path)
        return dokonico.core.Config(path)

    def env(self):
        factory = dokonico.env.EnvHelperFactory()
        return factory.create()

    def argoptions(self):
        parser = ArgParser()
        return parser.parse()

    def init_logger(self):
        log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')
        log.debug("Logger initialized.")

    def create_app(self, opts):
        if opts.mode == "show":
            return dokonico.app.SessionsPrinter(self.config(), self.env(), opts)
        elif opts.mode == "sync":
            return dokonico.app.Syncer(self.config(), self.env(), opts)
        else:
            raise ValueError("Invalid mode {}".format(opts.mode))
        

    def load(self):
        self.init_logger()
        opts = self.argoptions()
        return self.create_app(opts)

