# SPDX-License-Identifier: Apache-2.0
# Copyright 2019 Blue Cheetah Analog Design Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, Any, Optional

import pkg_resources
from pathlib import Path

from bag.design.module import Module
from bag.design.database import ModuleDB
from bag.util.immutable import Param


# noinspection PyPep8Naming
class bag3_testbenches__diode_tb_sp(Module):
    """Module for library bag3_testbenches cell diode_tb_sp.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                str(Path('netlist_info',
                                                         'diode_tb_sp.yaml')))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            dut_lib='DUT library name',
            dut_cell='DUT cell name',
            dut_conns='DUT connection dictionary'
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            dut_conns=None,
        )

    def design(self, dut_lib: str, dut_cell: str, dut_conns: Optional[Dict[str, str]]) -> None:
        inst_name = 'XDUT'
        # setup DUT
        self.replace_instance_master(inst_name, dut_lib, dut_cell, static=True,
                                     keep_connections=True)
        if dut_conns:
            inst = self.instances[inst_name]
            for term_name, net_name in dut_conns.items():
                inst.update_connection(inst_name, term_name, net_name)