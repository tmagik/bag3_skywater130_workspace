# -*- coding: utf-8 -*-

from typing import Dict, Any

import pkg_resources
from pathlib import Path

from bag.design.module import Module
from bag.design.database import ModuleDB
from bag.util.immutable import Param


# noinspection PyPep8Naming
class aib_ams__aib_frontend(Module):
    """Module for library aib_ams cell aib_frontend.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                str(Path('netlist_info',
                                                         'aib_frontend.yaml')))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            fe_params='frontend schematic parameters.',
            nd_params='N-diode schematic parameters.',
            pd_params='P-diode schematic parameters.',
            ms_params='metal short schematic parameters.',
        )

    def design(self, fe_params: Param, nd_params: Param, pd_params: Param, ms_params: Param
               ) -> None:
        self.instances['XFE'].design(**fe_params)
        self.instances['XND'].design(**nd_params)
        self.instances['XPD'].design(**pd_params)
        self.instances['XMS'].design(**ms_params)
