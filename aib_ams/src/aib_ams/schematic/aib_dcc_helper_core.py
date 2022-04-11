# -*- coding: utf-8 -*-

from typing import Dict, Any

import pkg_resources
from pathlib import Path

from bag.design.module import Module
from bag.design.database import ModuleDB
from bag.util.immutable import Param


# noinspection PyPep8Naming
class aib_ams__aib_dcc_helper_core(Module):
    """Module for library aib_ams cell aib_dcc_helper_core.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                str(Path('netlist_info',
                                                         'aib_dcc_helper_core.yaml')))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            mux_params='clock mux parameters.',
            flop_params='divider flop parameters.',
            inv_params='inverter parameters.',
        )

    def design(self, mux_params: Param, flop_params: Param, inv_params: Param) -> None:
        self.instances['XMUXI'].design(**mux_params)
        self.instances['XMUXO'].design(**mux_params)
        self.instances['XDIV'].design(**flop_params)
        self.instances['XINV0'].design(dual_output=False, **inv_params)
        self.instances['XINV1'].design(dual_output=True, **inv_params)
