# This file is part of Checkbox.
#
# Copyright 2014 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# Checkbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# Checkbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Checkbox.  If not, see <http://www.gnu.org/licenses/>.

"""
:mod:`plainbox.impl.unit.file` -- file unit
===========================================
"""

import logging
import os

from plainbox.i18n import gettext as _
from plainbox.i18n import gettext_noop as N_
from plainbox.impl.symbol import SymbolDef
from plainbox.impl.unit.job import propertywithsymbols
from plainbox.impl.unit.unit import Unit, UnitValidator
from plainbox.impl.unit.validators import CorrectFieldValueValidator
from plainbox.impl.validation import Problem
from plainbox.impl.validation import Severity

__all__ = ['FileRole', 'FileUnit']


logger = logging.getLogger("plainbox.unit.file")


class FileRole(SymbolDef):
    """
    Symbols that correspond to the role that a particular file plays.

    Each file in a particular provider can be classified to belong to one
    of the following roles. It is possible that the set of roles is not
    exhaustive and new roles will be added in the futurte.
    """
    unit_source = 'unit-source'
    legacy_whitelist = 'legacy-whitelist'
    script = 'script'  # architecture independent executable
    binary = 'binary'  # architecture dependent executable
    data = 'data'  # data file
    i18n = 'i18n'  # translation catalog
    manage_py = 'manage.py'  # management script
    legal = 'legal'  # license & copyright
    docs = 'docs'  # documentation
    unknown = 'unknown'  # unknown / unclassified
    build = 'build'  # build artefact
    invalid = 'invalid'  # invalid file that will never be used
    vcs = 'vcs'  # version control system data
    src = 'src'  # source


class FileUnitValidator(UnitValidator):
    """
    Validator for the FileUnit class.

    The sole purpose of this class is to have a custom :meth:`explain()`
    so that we can skip the 'field' part as nobody is really writing file
    units and the notion of a field may be confusing.
    """

    def explain(self, unit, field, kind, message):
        stock_msg = self._explain_map.get(kind)
        if message or stock_msg:
            return message or stock_msg


class FileUnit(Unit):
    """
    Unit that describes a single file.

    Every file that is a part of a provider has a corresponding file unit.
    Units like this are automatically generated by the provider itself.

    The file unit can be still defined to provide any additional meta-data.
    The file unit is used for contextual validation of job definitions and
    other unit types. The sole purpose, for now, is to advise against using
    the ``.txt`` or the ``.txt.in`` extensions in favour of the new one
    ``.pxu``
    """

    def __str__(self):
        """
        Same as .path
        """
        return self.path

    def __repr__(self):
        return "<FileUnit path:{!r}, role:{!r}>".format(self.path, self.role)

    @property
    def path(self):
        """
        Absolute path of the file this unit describes

        Typically you may wish to construct a relative path, using some other
        directory as the base directory, depending on context.
        """
        return self.get_record_value('path')

    @propertywithsymbols(symbols=FileRole)
    def role(self):
        """
        Role of the file within the provider
        """
        return self.get_record_value('role')

    class Meta:

        name = N_('file')

        validator_cls = FileUnitValidator

        class fields(SymbolDef):
            """
            Symbols for each field that a FileUnit can have
            """
            path = 'path'
            role = 'role'
            base = 'base'

        field_validators = {
            fields.path: [
                CorrectFieldValueValidator(
                    lambda value: os.path.splitext(value)[1] == '.pxu',
                    Problem.deprecated, Severity.advice,
                    onlyif=lambda unit: unit.role == FileRole.unit_source,
                    message=_(
                        "please use .pxu as an extension for all"
                        " files with plainbox units, see: {}"
                    ).format(
                        'http://plainbox.readthedocs.org/en/latest/author/'
                        'faq.html#faq-1'
                    )),
            ],
            fields.role: [
                CorrectFieldValueValidator(
                    lambda value: value in FileRole.get_all_symbols(),
                    message=_('valid values are: {}').format(
                        ', '.join(str(sym) for sym in sorted(
                            FileRole.get_all_symbols())))),
            ]
        }
