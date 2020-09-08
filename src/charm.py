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


class HttpProviderRelationEvents(ObjectEvents):
    """Http Provider Relation Events."""


class FlaskHttpProviderRelation(Object):
    """Provide the flask http port and hostname on relation data."""

    on = HttpProviderRelationEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)

        self._relation_name = relation_name

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
        # Set the application web server listening port and hostname on this unit's
        # relation data. 
        event.relation.data[self.model.unit]['port'] = "8080"
        event.relation.data[self.model.unit]['hostname'] = socket.gethostname()

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")

    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")



class FlaskCharm(CharmBase):

    def __init__(self, *args):
        """Observe the events of the http provider interface."""
        super().__init__(*args)

        self._flask_http = FlaskHttpProviderRelation(self, "http")
        
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

        # Grap the flask-snap resource and install it.
        resource_path = self.model.resources.fetch('flask-snap')
        subprocess.call([
            "snap",
            "install",
            str(resource_path),
            "--dangerous",
        ])

    def _on_start(self, event):
        logger.debug("################ LOGGING RELATION START ####################")

    def _on_config_changed(self, event):
        logger.debug("################ LOGGING RELATION CONFIG CHANGED ####################")

    def _on_stop(self, event):
        logger.debug("################ LOGGING RELATION STOP ####################")

    def _on_remove(self, event):
        logger.debug("################ LOGGING RELATION REMOVE ####################")

if __name__ == "__main__":
    main(FlaskCharm)
