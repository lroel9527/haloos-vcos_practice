#!/usr/bin/env python3
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
VCOS API Usage Example

This script demonstrates the proper usage of VCOS wrapper API
with improved configuration management and error handling.
"""

import os,sys
import yaml
from pathlib import Path
from typing import List, Dict, Any
CUR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(CUR_FILE_PATH, "..", "vcos_wrapper"))
sys.path.append(os.path.join(CUR_FILE_PATH))
from api import (
    load_project, 
    save_project, 
    import_arxml,
    data_mapping,
    port_mapping,
    service_mapping,
    export_taskmapping_xlsx,
    task_mapping_by_excel, 
    task_mapping_by_list,
    generate_schedule_tables,
    validate_project, 
    generate_code,
    VCOS_LOGGER
)
from exceptions import VCOSError
from copy_arxml import copy_arxml_files
from integrate_script.merge_taskmapping_excel import merge_taskmapping_excel
from vcos_wrapper.logger import setup_logger
log = setup_logger(__name__)

# ========== Project Configuration ==========
INTEGRATE_CONFIG_PATH = os.path.join(CUR_FILE_PATH, '..', '..', 'auto_integrate','integrate_cfg.yaml')
with open(INTEGRATE_CONFIG_PATH, 'r') as f:
    INTEGRATE_CONFIG = yaml.safe_load(f)


# Constants for configuration
class Config:
    """Centralized configuration for Integrate"""
    
    # Path configurations
    FILE_PATHS = {
        "Interface_File":   os.path.join(CUR_FILE_PATH, '..', '..', 'input_files', 'interface.xlsx'),
        "TaskMapping_BSW":  os.path.join(CUR_FILE_PATH, '..', '..', 'input_files'),
        "TaskMapping":  os.path.join(CUR_FILE_PATH, '..', '..', 'input_files', 'taskmapping.xlsx'),
        "Project_Path":     os.path.join(CUR_FILE_PATH, '..', '..', '..', '..', '..', 'apps/rt_demo/system_cfg/a2g_tc397_5v_tft/rt_demo.vcosproject'),
        "ARXML_Path":       os.path.join(CUR_FILE_PATH, '..', '..', '..', '..', '..', 'apps/rt_demo/system_cfg/a2g_tc397_5v_tft/config/asw'),
    }
    
    # Mapping method selection
    TASK_MAPPING_METHOD = "excel"  # "excel" or "list"
    
    # Data mapping configuration
    DATAMAPPING_LIST: List[Dict[str, Any]] = [
        {
            "component": "",
            "direction": "Tx",
            "prefix": None,
            "postfix": None,
            "ignore_match_whole_word": True,
            "ignore_match_case": False,
            "allow_multi_signal": True,
            "log_save": True,
            "match_compatibility": True
        },
        {
            "component": "",
            "direction": "Rx",
            "prefix": None,
            "postfix": None,
            "ignore_match_whole_word": True,
            "ignore_match_case": False,
            "allow_multi_signal": True,
            "log_save": True,
            "match_compatibility": True
        }
    ]
    
    # Port mapping configuration
    PORTMAPPING_LIST: List[Dict[str, Any]] = [
        {
            "component": None,
            "direction": "Tx",
            "prefix": None,
            "postfix": None,
            "allow_split": True,
            "allow_merge": False,
            "ignore_match_whole_word": False,
            "ignore_match_case": False,
            "log_save": True,
        },
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
    ]
    
    # Service mapping configuration
    SERVICEMAPPING_LIST: List[Dict[str, Any]] = [
        {
            "component": None,
            "direction": "Tx",
            "prefix": None,
            "postfix": None,
            "allow_split": True,
            "allow_merge": False,
            "ignore_match_whole_word": False,
            "ignore_match_case": False,
            "log_save": True,
        },
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
    ]
    

    def get_task_mapping_list() -> List[Dict[str, Any]]:
        """
        Dynamically load task mapping configuration from external source.
        
        Returns:
            List of task mapping configurations
        """
        # Replace this with actual implementation to load from:
        # - Database
        # - JSON/YAML config file
        # - External API
        # - etc.
        
        # Example: Loading from CSV file
        # import pandas as pd
        # df = pd.read_csv("task_mapping.csv")
        # return df.to_dict('records')
        
        # For demo purposes, return sample data
        return [
            {
                "task_name": "Default_BSW_Task_Core0",
                "swc_name": "Client1",
                "runnable_name": "Client1_Test_Runnable",
                "position": 0
            }
        ]
    
    def get_task_mapping_excel() -> Path:
        """
        Get the path to the task mapping Excel file.
        
        Note: In real usage, this would export from VCOS project first,
        then return the path to the populated Excel file.
        
        Returns:
            Path: Path to the task mapping Excel file
        """
        # In production, you would:
        # 1. Export the template from VCOS project
        # 2. Populate it with required mappings
        # 3. Return the final path
        
        # For demo purposes, return a fixed path
        # return Path("path/to/taskmapping.xlsx")
        return merge_taskmapping_excel(Config.FILE_PATHS["Interface_File"],
                                      Config.FILE_PATHS["TaskMapping_BSW"] + '/TaskMapping_BSW.xlsx',
                                      Config.FILE_PATHS["TaskMapping"])


def run_vcos_workflow() -> int:
    """
    Execute the complete VCOS workflow with proper error handling.
    
    Returns:
        int: 0 on success, 1 on failure
    """
    try:
        VCOS_LOGGER.init_default_handler(log_path=CUR_FILE_PATH)  # VCOS Log
        # 1. Load project
        log.info("Loading VCOS project...")
        load_project(Config.FILE_PATHS["Project_Path"])
        
        # 2. Import ARXML
        if INTEGRATE_CONFIG["Integration_steps"]["ImportArxml"]:
            if INTEGRATE_CONFIG["Integration_steps"]["CopyArxml"]:
                src_dict = {"local_arxml": os.path.join(CUR_FILE_PATH, '..', '..', 'input_files/arxml')}
                copy_arxml_files(src_dict, Config.FILE_PATHS["ARXML_Path"])
            log.info("Importing ARXML file...")
            import_arxml(Config.FILE_PATHS["ARXML_Path"])

        # 3. Task mapping
        if INTEGRATE_CONFIG["Integration_steps"]["TaskMapping"]:
            log.info("Performing task mapping...")
            if Config.TASK_MAPPING_METHOD == "excel":
                export_taskmapping_xlsx(Config.FILE_PATHS["TaskMapping_BSW"])
                task_mapping_excel_path = Config.get_task_mapping_excel()
                task_mapping_by_excel(task_mapping_excel_path)
            else:
                task_mapping_list = Config.get_task_mapping_list()
                task_mapping_by_list(task_mapping_list)
        
        # 4. Port mapping
        if INTEGRATE_CONFIG["Integration_steps"]["PortMapping"]:
            log.info("Performing port mapping...")
            port_mapping(Config.PORTMAPPING_LIST)
        
        # 5. Service mapping
        if INTEGRATE_CONFIG["Integration_steps"]["ServiceMapping"]:
            log.info("Performing service mapping...")
            service_mapping(Config.SERVICEMAPPING_LIST)
        
        # 6. Data mapping
        if INTEGRATE_CONFIG["Integration_steps"]["DataMapping"]:
            log.info("Performing data mapping...")
            data_mapping(Config.DATAMAPPING_LIST)
        
        # 7. Generate all schedule tables
        if INTEGRATE_CONFIG["Integration_steps"]["GenAllSchedule"]:
            log.info("Generating schedule tables...")
            generate_schedule_tables()
        
        # 8. Validate project
        if INTEGRATE_CONFIG["Integration_steps"]["Validation"]:
            log.info("Validating project, with mode [os, rte] ...")
            validate_project(["Os", "Rte"], "no limit")  # "no limit" for demo prj
        
        # 9. Generate code
        if INTEGRATE_CONFIG["Integration_steps"]["CodeGeneration"]:
            log.info("Generating code...")
            generate_code()
        
        # 10. Save project
        log.info("Saving project...")
        save_project()
        log.info("All operations completed successfully!")
        return 0
        
    except VCOSError as e:
        log.info(f"\nError: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        log.info(f"\nUnexpected error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_vcos_workflow())