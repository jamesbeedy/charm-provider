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

    @property
    def _relation(self):
        return self.framework.model.get_relation(self._relation_name)

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")
        logger.debug(f"NODE_INFO: {self.charm.state.node_info}")

        if self.charm.state.slurm_installed:
            logger.debug("SLURM INSTALLED SETTING RELATION DATA")
            event.relation.data[self.model.unit]['hostname'] = self.hostname
            event.relation.data[self.model.unit]['inventory'] = self.charm.state.node_info
            event.relation.data[self.model.unit]['partition'] = "rat"
            event.relation.data[self.model.unit]['default'] = "False"
        else:
            logger.debug("SLURM NOT INSTALLED DEFERING SETTING RELATION DATA")
            event.defer()
            return


        #if self.state.slurm_installed:
        #    logger.debug("SHARED STATE RECOGNIZED")
        #    logger.debug("SHARED STATE RECOGNIZED")
        #    logger.debug("SHARED STATE RECOGNIZED")

        #logger.debug(self._relation)
        #event.relation.data[self.model.unit]['hostname'] = self.hostname
        #event.relation.data[self.model.app]['hostname'] = self.hostname
        #logger.debug(self._relation)

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")
        logger.debug(f"NODE_INFO: {self.charm.state.node_info}")

        #logger.debug(self._relation)
        #logger.debug(event.relation.data)
        #logger.debug("################ LOGGING EVENT DATA in RELATION JOINED ####################")
        #logger.debug(event.relation.data[self.model.app])
        #logger.debug(event.relation.data[self.model.unit])
        #logger.debug("################ LOGGING SELF RELATION DATA in RELATION JOINED ####################")
        #logger.debug(self._relation)
        #logger.debug(self._relation.data)

    def _on_relation_changed(self, event):
        logger.debug(f"NODE_INFO: {self.charm.state.node_info}")
        logger.debug("################ LOGGING RELATION CHANGED ####################")
        
    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")


class ProviderCharm(CharmBase):

    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.hostname = socket.gethostname()

        self.state.set_default(slurm_installed=False)
        self.state.set_default(node_info=str())
        
        self.slurmd_provider = TestingProviderRelation(self, "slurmd")
        
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)

    def on_install(self, event):
        pass

    def on_start(self, event):
        self.state.node_info = self.get_node_info()
        self.state.slurm_installed = True

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
