# -*- coding: utf-8 -*-

from typing import Dict, Any, List, Tuple

import pkg_resources
from pathlib import Path

from bag.design.module import Module
from bag.design.database import ModuleDB
from bag.util.immutable import Param

from pybag.enum import TermType


# noinspection PyPep8Naming
class bag3_digital__comparator_wrapper(Module):
    """Module for library bag3_digital cell comparator_wrapper.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                str(Path('netlist_info',
                                                         'comparator_wrapper.yaml')))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            fes_params='Parameters for Front-end switch',
            comp_params='Parameters for Comparator + Output Stage',
            remove_pins_list='List of pins to be removed',
            reconn_comp_list='Modified terminal connections for Comparator',
            reconn_fes_list='Modified terminal connections for Front-end switch',
            rename_pins_list='List of pins to be renamed',
            extra_pins='Extra pins to be added',
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            remove_pins_list=[],
            reconn_comp_list=[],
            reconn_fes_list=[],
            rename_pins_list=[],
            extra_pins=None,
        )

    def design(self, fes_params: Param, comp_params: Param, remove_pins_list: List[str],
               reconn_comp_list: List[Tuple[str]], reconn_fes_list: List[Tuple[str]],
               rename_pins_list: List[Tuple[str]], extra_pins: Dict[str, list],) -> None:
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        # pins
        for pin in remove_pins_list:
            self.remove_pin(pin)

        for old_pin, new_pin in rename_pins_list:
            self.rename_pin(old_pin, new_pin)

        if extra_pins is not None:
            for pin_name in extra_pins['in']:
                self.add_pin(pin_name, TermType.input)
            for pin_name in extra_pins['out']:
                self.add_pin(pin_name, TermType.output)

        noconn_num = 0

        # comparator design
        self.instances['XCOMP'].design(**comp_params)
        for term, name in reconn_comp_list:
            if name == 'noconn':
                name = f'noconn<{noconn_num}>'
                noconn_num += 1
            self.reconnect_instance_terminal('XCOMP', term, name)

        # front end switch design
        self.instances['XFES'].design(**fes_params)
        for term, name in reconn_fes_list:
            if name == 'noconn':
                name = f'noconn<{noconn_num}>'
                noconn_num += 1
            self.reconnect_instance_terminal('XFES', term, name)

        # noconn instances
        if noconn_num == 0:
            self.remove_instance('XNC')
        elif noconn_num == 1:
            self.reconnect_instance_terminal('XNC', 'noConn', 'noconn<0>')
        else:
            suf = f'<{noconn_num-1}:0>'
            self.rename_instance('XNC', 'XNC' + suf, [('noConn', 'noconn' + suf)])