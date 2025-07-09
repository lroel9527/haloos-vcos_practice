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

import os
import sys
import pandas as pd

# ========== Logger Setup ==========
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vcos_wrapper.logger import setup_logger

logger = setup_logger()


# ========== Core Logic Functions ==========
def extract_schedul_info(excel_path, sheet_name="TaskSchedule"):
    """
    Extract schedule information from the Excel file.

    Args:
        excel_path: Path to the Excel file.
        sheet_name: Name of the worksheet to read.

    Returns:
        DataFrame containing the selected columns and derived runnable information.
    """
    selected_cols = ['APP', 'Init_SWC', 'InitTask', 'SWC', 'CycleTask', 'SWC_Type', 'SWCMap']
    df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=selected_cols, dtype=str).fillna('')
    # Add new runnable columns
    df['cycle_runnable'] = None
    df['init_runnable'] = None

    def get_cycle_runnable(row):
        if row['SWC'] and row['CycleTask'] and row['SWC_Type']:
            return f"{row['SWC']}_step" if len(row['SWC']) > 1 else None
        return None

    def get_init_runnable(row):
        if row['Init_SWC'] and row['InitTask']:
            return f"{row['SWC']}_initialize"
        return None

    df['cycle_runnable'] = df.apply(get_cycle_runnable, axis=1)
    df['init_runnable'] = df.apply(get_init_runnable, axis=1)
    return df


def fill_out_interface(schedule_df, bsw_task_xlsx, output_xlsx):
    """
    Update (fill in) the TaskMapping table using the extracted scheduling information.

    Args:
        schedule_df: DataFrame containing the schedule info and runnables.
        bsw_task_xlsx: Input path of the original TaskMapping_BSW file.
        output_xlsx: Output path to save the updated Excel file.
    """
    bsw_df = pd.read_excel(bsw_task_xlsx, sheet_name=0, header=0)
    columns = bsw_df.columns
    max_rows = bsw_df.shape[0]

    for idx, row in schedule_df.iterrows():
        if str(row['SWCMap']).strip().lower() == 'yes':
            # Fill cyclic SWC
            task_col = None
            for col in columns:
                name_lines = str(col).split('\n')
                if len(name_lines) < 3:
                    continue
                app_name, task_name = name_lines[0].strip(), name_lines[1].strip()
                if app_name == row['APP'] and task_name == row['CycleTask']:
                    task_col = col
                    break
            if task_col and row['cycle_runnable']:
                col_data = bsw_df[task_col].tolist()
                # 判断是否已存在
                if row['cycle_runnable'] not in col_data:
                    insert_pos = next((i for i, val in enumerate(col_data[1:], start=1) if pd.isna(val)), len(col_data))
                    if insert_pos < max_rows:
                        bsw_df.at[insert_pos, task_col] = row['cycle_runnable']
                    else:
                        bsw_df.loc[max_rows, task_col] = row['cycle_runnable']
                        max_rows += 1
            # Fill Init SWC
            task_col = None
            for col in columns:
                name_lines = str(col).split('\n')
                if len(name_lines) < 3:
                    continue
                app_name, task_name = name_lines[0].strip(), name_lines[1].strip()
                if app_name == row['APP'] and task_name == row['InitTask']:
                    task_col = col
                    break
            if task_col and row['init_runnable']:
                col_data = bsw_df[task_col].tolist()
                # 判断是否已存在
                if row['init_runnable'] not in col_data:
                    insert_pos = next((i for i, val in enumerate(col_data[1:], start=1) if pd.isna(val)), len(col_data))
                    if insert_pos < max_rows:
                        bsw_df.at[insert_pos, task_col] = row['init_runnable']
                    else:
                        bsw_df.loc[max_rows, task_col] = row['init_runnable']
                        max_rows += 1
    bsw_df.to_excel(output_xlsx, index=False, sheet_name='Sheet')


def merge_taskmapping_excel(interface_file, taskmapping_bsw, taskmapping_out):
    """
    Main entry point: Extract the schedule info from the interface excle and fill in the TaskMapping Excel.
    """
    try:
        schedule_df = extract_schedul_info(interface_file)
        fill_out_interface(schedule_df, taskmapping_bsw, taskmapping_out)
        logger.info('TaskMapping merge completed, output: %s', taskmapping_out)
        return taskmapping_out
    except Exception as e:
        logger.error("Processing failed: %s", e)
        sys.exit(1)
