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

import argparse

from bag.core import BagProject
from bag.simulation.core import DesignManager


def parse_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate transistor characterization database.')
    parser.add_argument('specs', help='Transistor characterization specs file name.')
    parser.add_argument('--no-gen', dest='generate', action='store_false', default=True,
                        help='disable generation')
    parser.add_argument('--no-meas', dest='measure', action='store_false', default=True,
                        help='disable measurement')
    parser.add_argument('--load', dest='load_from_file', action='store_true', default=False,
                        help='enable loading from file.')
    args = parser.parse_args()
    return args


def run_main(prj: BagProject, args: argparse.Namespace) -> None:
    sim = DesignManager(prj, args.specs)
    sim.characterize_designs(generate=args.generate, measure=args.measure,
                             load_from_file=args.load_from_file)


if __name__ == '__main__':
    _args = parse_options()

    local_dict = locals()
    if '_prj' not in local_dict:
        print('creating BAG project')
        _prj = BagProject()
    else:
        print('loading BAG project')
        _prj = local_dict['_prj']

    run_main(_prj, _args)
