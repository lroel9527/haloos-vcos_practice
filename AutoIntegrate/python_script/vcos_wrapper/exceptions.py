# This Python file uses the following encoding: utf-8
############################################################################
# Copyright (c) 2025 Li Auto Inc. and its affiliates
# Licensed under the Apache License, Version 2.0(the "License");
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
############################################################################

class VCOSError(Exception):
    """Base exception for all VCOS related errors"""
    pass


class ProjectLoadError(VCOSError):
    """Failed to load project"""
    pass


class ProjectSaveError(VCOSError):
    """Failed to save project"""
    pass


class ImportError(VCOSError):
    """Failed to import ARXML"""
    pass


class ExportError(VCOSError):
    """Failed to export"""
    pass


class MappingError(VCOSError):
    """Base class for mapping related errors"""
    pass


class TaskMappingError(MappingError):
    """Failed to perform task mapping"""
    pass


class DataMappingError(MappingError):
    """Failed to perform data mapping"""
    pass


class PortMappingError(MappingError):
    """Failed to perform port mapping"""
    pass


class ServiceMappingError(MappingError):
    """Failed to perform service mapping"""
    pass


class SpinLockError(VCOSError):
    """Failed to create spinlock"""
    pass


class ValidationError(VCOSError):
    """Validation failed"""
    pass


class CodeGenerationError(VCOSError):
    """Code generation failed"""
    pass