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
File Copy Utility

This module provides utility functions for copying files and directories,
with a focus on .arxml file types commonly used in the automotive software domain.

Features:
- Copy single files, folders, or all .arxml files from multiple folders into a target folder.
- Robust error handling and informative logging.
"""

import os
import sys
import shutil
from typing import Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vcos_wrapper.logger import setup_logger

log = setup_logger(__name__)


def copy_file(src: str, dst: str) -> None:
    """
    Copy a single file from src to dst.

    Args:
        src (str): Path to the source file.
        dst (str): Path to the destination file.
    
    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If copying fails due to IO or OS reasons.
    """
    try:
        shutil.copy2(src, dst)
        # log.info(f"Copied file from {src} to {dst}")
    except FileNotFoundError as e:
        log.error(f"Source file not found: {src} - {e}")
        raise
    except OSError as e:
        log.error(f"Unable to copy file from {src} to {dst}: {e}")
        raise


def copy_folder(src_folder: str, dst_folder: str) -> None:
    """
    Copy an entire folder recursively from src_folder to dst_folder.

    Args:
        src_folder (str): The source directory.
        dst_folder (str): The destination directory.
    
    Raises:
        FileNotFoundError: If the source directory does not exist.
        OSError: If copying fails due to IO or OS reasons.
    """
    try:
        shutil.copytree(src_folder, dst_folder)
        log.info(f"Successfully copied folder from {src_folder} to {dst_folder}.")
    except FileNotFoundError as e:
        log.error(f"Source folder not found: {src_folder} - {e}")
        raise
    except FileExistsError as e:
        log.warning(f"Destination folder already exists: {dst_folder} - {e}")
        raise
    except OSError as e:
        log.error(f"Unable to copy directory from {src_folder} to {dst_folder}: {e}")
        raise


def copy_arxml_files(src_folders: Dict[str, str], dst_folder: str) -> None:
    """
    Copy all .arxml files from multiple source folders to a target folder.

    Args:
        src_folders (Dict[str, str]): Dictionary of source folder names to paths.
        dst_folder (str): Path to the destination folder.
    """
    if not os.path.exists(dst_folder):
        try:
            os.makedirs(dst_folder)
            log.info(f"Created destination folder: {dst_folder}")
        except Exception as e:
            log.error(f"Failed to create destination folder '{dst_folder}': {e}")
            return

    total_files_copied = 0
    for src_name, src_path in src_folders.items():
        if not os.path.isdir(src_path):
            log.warning(f"Skipping non-directory: {src_path}")
            continue
        arxml_count = 0
        for item in os.listdir(src_path):
            file_path = os.path.join(src_path, item)
            if os.path.isfile(file_path) and item.lower().endswith('.arxml'):
                dst_path = os.path.join(dst_folder, item)
                try:
                    copy_file(file_path, dst_path)
                    arxml_count += 1
                    total_files_copied += 1
                except Exception as e:
                    log.warning(f"Failed to copy {file_path} to {dst_path}: {e}")
                    continue
        log.info(f"{arxml_count} .arxml files have been copied from {src_path} to {dst_folder}")
    log.info(f"Total {total_files_copied} .arxml files have been copied to {dst_folder}")
