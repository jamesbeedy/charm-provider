#! /usr/bin/env python3
from ops.charm import CharmBase

from ops.main import main


import logging
import socket
import json

from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
    StoredState,
)


logger = logging.getLogger()


class RenderConfigAndRestartEvent(EventBase):
    pass


class SlurmClusterRequiresRelationEvents(ObjectEvents):
    """SlurmCluster Relation Events"""
    render_config_and_restart = EventSource(
        RenderConfigAndRestartEvent
    )


class SlurmClusterRequiresRelation(Object):

    on = SlurmClusterRequiresRelationEvents()
    
    _state = StoredState()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.charm = charm
        self._relation_name = relation_name
        self.hostname = socket.gethostname()

        self.state.set_default(controller_config_acquired=False)
        self.state.set_default(controller_config=dict())

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
    def controller_config_acquired(self):
        return self._state.controller_config_acquired

    @property
    def controller_config(self):
        return self._state.controller_config

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")

        # 1) Ensure that we have data to access from the charm state object.
        # 2) Use data from the main charm state to fulfil sending the relation data.
        if self.charm.state.slurm_installed:
            event.relation.data[self.model.unit]['hostname'] = \
                self.charm.hostname
            event.relation.data[self.model.unit]['inventory'] = \
                self.charm.slurm_ops_manager.inventory
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

        controller_config = event.relation.data[event.app].get('controller_config')
        if controller_config:
            # Turn this into something that can be event emmited
            # transformation of controller config into an event object
            #self._state.controller_config_acquired = True
            #self.charm.slurm_ops_manager.on.reconfigure_and_restart.emit(controller_config.event_object)
    
    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")


class SlurmdCharm(CharmBase):

    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self.config = self.model.config
        self.hostname = socket.gethostname()

        self.slurm_ops_manager = SlurmOpsManager(self, 'slurmd')
        self.slurm_cluster = SlurmClusterRequiresRelation(self, "slurm-cluster")
        
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)

        self.framework.observe(self.on.start, self._on_start)


    def _on_install(self, event):
        self.slurm_ops_manager.prepare_system_for_slurm()

    def _on_start(self, event):
        if self.slurm_cluster.controller_config_acquired and self.slurm_ops_manager.slurm_installed:
            self.slurm_ops_manager.on.render_config_and_restart.emit()
        else:
            if not self.slurm_cluster.controller_config_acquired:
                self.unit.status = BlockedStatus("Need relation to slurm controller.")
            elif not self.slurm_ops_manager.slurm_installed:
                self.unit.status = WaitingStatus("Waiting on slurm install to complete...")
            event.defer()
            return 
    


if __name__ == "__main__":
    main(SlurmdCharm)
