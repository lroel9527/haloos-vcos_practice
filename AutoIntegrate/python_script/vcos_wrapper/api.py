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

"""
This file is a Python wrapper interface for VCOS, 
mainly used to interact with the underlying API of VCOS, provide a more user-friendly Python interface, 
and integrate functions such as logging, exception handling, and performance monitoring.
"""
import os
import sys
import time
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Import original VCOS API
_CUR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
_VCOS_PATH = os.path.join(_CUR_FILE_PATH, "..", "..", "..", "..","vcos_studio/Configurator")
sys.path.append(str(_VCOS_PATH))
sys.path.append(os.path.join(_VCOS_PATH, "cmd_api"))
sys.path.append(os.path.join(_VCOS_PATH, "cmd_adaptor"))
sys.path.append(os.path.join(_VCOS_PATH, "third_party"))

from cmd_api.auto_cli_api import AutoCliApi  # type: ignore
from cmd_adaptor.cmd_interaction.cmd_logger import logger as VCOS_LOGGER

from exceptions import *
from logger import setup_logger

# Initialize module logger
log = setup_logger()


def _log_execution_time(func):
    """Decorator to log function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        log.info(f"Starting {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            runtime = time.time() - start_time
            log.info(f"{func.__name__} completed in {runtime:.2f} seconds")
            return result
        except Exception as e:
            runtime = time.time() - start_time
            log.error(f"{func.__name__} failed after {runtime:.2f} seconds: {str(e)}")
            raise
    return wrapper


@_log_execution_time
def load_project(project_path: Union[str, Path]) -> None:
    """
    Load a VCOS project.
    
    Args:
        project_path: Path to the project file
        
    Raises:
        ProjectLoadError: If project loading fails
    """
    project_path = str(Path(project_path).absolute())
    log.debug(f"Loading project from {project_path}")
    
    if not AutoCliApi.load_project(project_path):
        raise ProjectLoadError(f"Failed to load project: {project_path}")


@_log_execution_time
def save_project() -> None:
    """
    Save the current project.
    
    Raises:
        ProjectSaveError: If project saving fails
    """
    if not AutoCliApi.save_project():
        raise ProjectSaveError("Failed to save project")


@_log_execution_time
def import_arxml(arxml_path: Union[str, Path]) -> None:
    """
    Import ARXML file into the current project.
    
    Args:
        arxml_path: Path to the ARXML file
        
    Raises:
        ImportError: If import fails
    """
    arxml_path = str(Path(arxml_path).absolute())
    log.debug(f"Importing ARXML from {arxml_path}")
    
    if not AutoCliApi.import_asw(arxml_path):
        raise ImportError(f"Failed to import ARXML: {arxml_path}")


@_log_execution_time
def task_mapping_by_excel(excel_path: Union[str, Path]) -> None:
    """
    Perform task mapping using an Excel file.
    
    Args:
        excel_path: Path to the Excel mapping file
        
    Raises:
        TaskMappingError: If mapping fails
    """
    excel_path = str(Path(excel_path).absolute())
    log.debug(f"Performing task mapping with {excel_path}")
    
    if not AutoCliApi.excute_task_mapping_by_file(excel_path):
        raise TaskMappingError(f"Failed to perform task mapping with file: {excel_path}")


@_log_execution_time
def task_mapping_by_list(mapping_list: List[Dict[str, Any]]) -> None:
    """
    Perform task mapping using a list of mappings.
    
    Args:
        mapping_list: List of task mappings
    Raises:
        TaskMappingError: If mapping fails
    Example:
        task_mapping_by_list(
            [{
                task_name: "Task1",
                swc_name: "SWC1",
                runnable_name: "Runnable1",
                position: 1,
            }]
        )
    """
    log.debug(f"Performing task mapping with list of {len(mapping_list)} items")
    
    if not AutoCliApi.excute_task_mapping(mapping_list):
        raise TaskMappingError("Failed to perform task mapping with list")


@_log_execution_time
def data_mapping(mapping_list: List[Dict[str, Any]]) -> None:
    """
    Perform data mapping between components.
    
    Args:
        mapping_list: List of data mappings     
    Raises:
        DataMappingError: If mapping fails
    Example:
        data_mapping(
            [{
                "component": "ASW_step",
                "direction": "Rx",
                "prefix": None,
                "postfix": None,
                "ignore_match_whole_word": True,
                "ignore_match_case": False,
                "allow_multi_signal": True,
                "log_save": True,
                "match_compatibility": True
            }]
        )
    """
    log.debug(f"Performing data mapping with {len(mapping_list)} items")
    
    if not AutoCliApi.excute_data_mapping(mapping_list):
        raise DataMappingError("Failed to perform data mapping")


@_log_execution_time
def port_mapping(mapping_list: List[Dict[str, Any]]) -> None:
    """
    Perform port mapping between components.
    
    Args:
        mapping_list: List of port mappings
    Raises:
        PortMappingError: If mapping fails
    Example:
        port_mapping([
            {
                "component": None,
                "direction": "Rx",
                "prefix": None,
                "postfix": None,
                "allow_split": True,
                "allow_merge": False,
                "ignore_match_whole_word": False,
                "ignore_match_case": False,
                "log_save": True,
            }
        ])
    """
    log.debug(f"Performing port mapping with {len(mapping_list)} items")
    
    if not AutoCliApi.excute_port_mapping(mapping_list):
        raise PortMappingError("Failed to perform port mapping")


@_log_execution_time
def service_mapping(mapping_list: List[Dict[str, Any]]) -> None:
    """
    Perform service interface mapping.
    
    Args:
        mapping_list: List of service mappings    
    Raises:
        ServiceMappingError: If mapping fails
    Example:
        service_mapping([
            {
                "component": None,
                "direction": "Rx",
                "prefix": None,
                "postfix": None,
                "allow_split": False,
                "allow_merge": False,
                "ignore_match_whole_word": False,
                "ignore_match_case": False,
                "log_save": True,
            }
        ])
    """
    log.debug(f"Performing service mapping with {len(mapping_list)} items")
    
    if not AutoCliApi.excute_service_mapping(mapping_list):
        raise ServiceMappingError("Failed to perform service mapping")


@_log_execution_time
def create_spinlocks(spinlock_list: List[Dict[str, Any]]) -> None:
    """
    Create spinlocks from a list of spinlock definitions.
    
    Args:
        spinlock_list: List of spinlock configurations
        
    Raises:
        SpinLockError: If any spinlock creation fails
    Example:
        create_spinlocks(
            [{
                "spinlock_id": "SL1",
                "spinlock_method": "LOCK_ALL_INTERRUPTS",
                "app_name_list": ['app1', 'app2', 'app3']
            }]
        )
    """
    log.debug(f"Creating {len(spinlock_list)} spinlocks")
    
    for spinlock_info in spinlock_list:
        try:
            if not AutoCliApi.add_spinlock(spinlock_info.copy()):
                raise SpinLockError(f"Failed to create spinlock: {spinlock_info.get('spinlock_id')}")
        except Exception as e:
            raise SpinLockError(f"Error creating spinlock: {str(e)}")


@_log_execution_time
def generate_schedule_tables() -> None:
    """
    Generate all schedule tables.
    
    Raises:
        VCOSError: If generation fails
    """
    if not AutoCliApi.generate_all_schedule_table():
        raise VCOSError("Failed to generate schedule tables")


@_log_execution_time
def validate_project(modules: Optional[List[str]] = None, log_level: str = "warnning") -> None:
    """
    Validate the project.
    
    Args:
        modules: List of modules to validate (default: ["Os", "Rte"])
        log_level: Log level for validation ("no limit"、"warning"、"error")
        
    Raises:
        ValidationError: If validation fails
    """
    modules = modules or ["Os", "Rte"]
    log.debug(f"Validating modules: {', '.join(modules)}")
    
    results, result_logs = AutoCliApi.excute_validation(modules, log_level)
    error_modules = [module for module, result in results.items() if not result]
    
    if error_modules:
        raise ValidationError(f"Validation failed for modules: {', '.join(error_modules)}")


@_log_execution_time
def generate_code(modules: Optional[List[str]] = None, 
                 is_debug: bool = False, 
                 force: bool = True) -> Dict[str, bool]:
    """
    Generate code for specified modules.
    
    Args:
        modules: List of modules to generate (default: ["Os", "Rte"])
        is_debug: Generation mode can be selected as debug or release, (default: release)
        force: Whether to force full quantity generation, default to full quantity
        
    Returns:
        Dictionary of module generation results
        
    Raises:
        CodeGenerationError: If generation fails
    """
    modules = modules or ["Os", "Rte"]
    log.debug(f"Generating code for modules: {', '.join(modules)}")
    
    results = AutoCliApi.excute_generation(modules, is_debug, force)
    
    if isinstance(results, bool):
        if not results:
            raise CodeGenerationError("Code generation failed")
        return {module: True for module in modules}
    
    error_modules = [module for module, result in results.items() if not result]
    if error_modules:
        raise CodeGenerationError(f"Code generation failed for modules: {', '.join(error_modules)}")
    
    return results


@_log_execution_time
def export_taskmapping_xlsx(export_path: str) -> bool:
    """Export TaskMapping data to an Excel file.
    
    This function exports the TaskMapping information from the currently opened VCOS project
    to an Excel file at the specified path. The project must be opened before calling this
    function and should be closed afterward.
    
    Args:
        export_path: Directory path where the Excel file will be saved. The filename 
                    "TaskMapping_BSW.xlsx" will be automatically appended.
                    
    Returns:
        bool: True if export succeeded, False otherwise.
        
    Raises:
        ExportError: If the export operation fails due to VCOS/AutoCliApi errors.
        FileNotFoundError: If the specified export directory doesn't exist.
        PermissionError: If there's no write permission for the export directory.
    """
    # Validate export path exists and is writable
    if not os.path.isdir(export_path):
        raise FileNotFoundError(f"Export directory does not exist: {export_path}")
    if not os.access(export_path, os.W_OK):
        raise PermissionError(f"No write permission for directory: {export_path}")

    # Construct full file path with platform-independent path separator
    file_path = os.path.join(export_path, "TaskMapping_BSW.xlsx")
    
    try:
        log.debug(f"Attempting to export TaskMapping to: {file_path}")
        result = AutoCliApi.export_task_mapping(file_path)
        
        if not result:
            error_msg = "AutoCliApi.export_task_mapping returned False"
            log.error(error_msg)
            raise ExportError(error_msg)
            
        log.info(f"Successfully exported TaskMapping to: {file_path}")
        return True
        
    except Exception as e:
        log.error(f"Failed to export TaskMapping: {str(e)}")
        raise ExportError(f"TaskMapping export failed: {str(e)}") from e
