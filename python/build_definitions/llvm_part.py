# Copyright (c) Yugabyte, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations
# under the License.

from yugabyte_db_thirdparty.build_definition_helpers import *  # noqa


class LlvmPartDependencyBase(Dependency):
    """
    Not a real dependency, but a base class for various dependencies corresponding to parts of the
    LLVM project. Allows to reuse the same download and the same archive directory.
    """
    def __init__(self, name: str, build_group: str, version: str) -> None:
        assert name.startswith('llvm_'), f'Invalid name: {name}'
        github_org = 'yugabyte' if '-yb-' in version else 'llvm'
        super(LlvmPartDependencyBase, self).__init__(
            name=name,
            version=version,
            url_pattern=(
                'https://github.com/%s/llvm-project/archive/llvmorg-{}.tar.gz' % github_org
            ),
            archive_name_prefix='llvm',
            build_group=build_group)
        llvm_major_version = int(self.version.split('.')[0])
        if llvm_major_version in [15, 16]:
            self.patches = ['llvm15-16-libunwind-force-asm-as-c.patch']

    def get_source_dir_basename(self) -> str:
        return f'llvm-{self.version}'
