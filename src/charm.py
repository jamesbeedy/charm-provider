#! /usr/bin/env python3
from ops.charm import CharmBase

from ops.main import main


import logging
import socket
import json

from ops.framework import (
    Object,
    ObjectEvents,
    StoredState,
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
            self.charm.on[self._relation_name].relation_created,
            self._on_relation_created
        )

        self.framework.observe(
            self.charm.on[self._relation_name].relation_joined,
            self._on_relation_joined
        )

        self.framework.observe(
            self.charm.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            self.charm.on[self._relation_name].relation_departed,
            self._on_relation_departed
        )

        self.framework.observe(
            self.charm.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")

        # 1) Ensure that we have data to access from the charm state object.
        # 2) Use data from the main charm state to fulfil sending the relation data.
        if self.charm.state.slurm_installed:
            event.relation.data[self.model.unit]['hostname'] = \
                self.charm.hostname
            event.relation.data[self.model.unit]['inventory'] = \
                self.charm.state.node_info
            event.relation.data[self.model.unit]['partition'] = \
                self.charm.config['partition']
            event.relation.data[self.model.unit]['default'] = \
                self.charm.config['default']
        else:
            # If we hit this hook before slurm is installed, defer.
            logger.debug("SLURM NOT INSTALLED DEFERING SETTING RELATION DATA")
            event.defer()
            return

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")
        
    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")


class ProviderCharm(CharmBase):

    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self.config = self.model.config
        self.hostname = socket.gethostname()
        self.state.set_default(node_info={})
        self.state.set_default(slurm_installed=False)
        
        self.slurmd_provider = TestingProviderRelation(self, "slurmd")
        
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)

    def on_install(self, event):
        pass

    def on_start(self, event):
        self.state.node_info = self.get_node_info()

    def get_node_info(self):
        return json.dumps({
            'NodeName': self.hostname,
            'CPUs': '4',
            'Boards': '1',
            'SocketsPerBoard': '1',
            'CoresPerSocket': '4',
            'ThreadsPerCore': '1',
            'RealMemory': '7852',
            'UpTime': '0-08:49:20',
            'gpus': 0,
        })


if __name__ == "__main__":
    main(ProviderCharm)
