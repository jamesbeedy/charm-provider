#!/usr/bin/python3
import subprocess
from ops.charm import CharmBase

from ops.main import main


import logging
import socket
import json

from ops.framework import (
    Object,
    ObjectEvents,
)


logger = logging.getLogger()


class ProviderRelationEvents(ObjectEvents):
    """Provider Relation Events"""


class TestingProviderRelation(Object):

    on = ProviderRelationEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.charm = charm


        self._relation_name = relation_name
        self.hostname = socket.gethostname()

        self.framework.observe(
            self.on[self._relation_name].relation_created,
            self._on_relation_created
        )

        self.framework.observe(
            self.on[self._relation_name].relation_joined,
            self._on_relation_joined
        )

        self.framework.observe(
            self.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            self.on[self._relation_name].relation_departed,
            self._on_relation_departed
        )

        self.framework.observe(
            self.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")

    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")



class ProviderCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.hostname = socket.gethostname()
        
        self.slurmd_provider = TestingProviderRelation(self, "slurmd")
        
        self.framework.observe(
            self.on.install,
            self._on_install
        )

        self.framework.observe(
            self.on.start,
            self._on_start
        )

        self.framework.observe(
            self.on.config_changed,
            self._on_config_changed
        )

        self.framework.observe(
            self.on.stop,
            self._on_stop
        )

        self.framework.observe(
            self.on.remove,
            self._on_remove
        )

    def _on_install(self, event):
        logger.debug("################ LOGGING RELATION INSTALL ####################")

    def _on_start(self, event):
        logger.debug("################ LOGGING RELATION START ####################")

    def _on_config_changed(self, event):
        logger.debug("################ LOGGING RELATION CONFIG CHANGED ####################")

    def _on_stop(self, event):
        logger.debug("################ LOGGING RELATION STOP ####################")

    def _on_remove(self, event):
        logger.debug("################ LOGGING RELATION REMOVE ####################")

if __name__ == "__main__":
    main(ProviderCharm)
