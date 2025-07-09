# integrate 仓库说明

## 1. 简介

本仓库基于 VCOS Studio, 提供自动化集成实例，可一键完成 ASW ARXML 导入、Task Mapping、Port Mapping、Data Mapping、校验、代码生成等步骤，相关过程均支持用户灵活、高度自定义配置。

## 2. 代码目录

> ```python
> AutoIntegrate
> ├── README.md                   # 仓库的readme，用于介绍该代码仓库(即本文)
> ├── auto_integrate              # 集成脚本入口文件夹，包含bat脚本和配置文件
> │   ├── auto_integrate.bat      # 自动化集成启动脚本
> │   └── integrate_cfg.yaml      # 自动化集成配置文件
> ├── input_files                 # 集成输入文件存放目录
> │   ├── ARXML                   # 存放需导入的ARXML文件
> │   ├── interface.xlsx          # ASW Task部署信息示例
> │   ├── TaskMapping_BSW.xlsx    # 从基础工程中导出的BSW TASK部署信息
> │   └── TaskMapping.xlsx        # 全量TaskMapping信息
> └── python_script               # 自动化集成python脚本
>     ├── integrate_script        # 自动化集成核心脚本
>     └── vcos_wrapper            # VCOS API封装
> ```

## 3. 使用指南

### 3.1 依赖项说明

1. VCOS Studio与API：自动化集成脚本依赖于 VCOS Studio 及其 API，相关脚本需在 VCOS Studio 提供的虚拟环境下运行。详见：`https://gitee.com/haloos/vcos_studio`。
2. BSW基础工程：请确认在自动化集成前已完成 BSW 基础工程的 OS 配置、DBC 导入等操作。本示例默认 VCOS 工程路径为 haloosspace\apps\rt_demo (需使用 Git-Repo 从远程仓库拉取haloosspace。此工程暂不支持DataMapping)。
3. ASW ARXML：需满足 AUTOSAR 规范。

### 3.2 使用说明

#### 3.2.1 配置项

在本示例中，有两处可修改配置：

1. auto_integrate/integrate_cfg.yaml 文件包含配置项目基本信息及集成流程，每步可灵活开关：

   ```yaml
   Project: # 工程相关配置
     Prj_Name: ECU_A  # 项目名称
     Prj_File_Name: rte_demo.vcosproject   # VCOS 工程名称

   Integration_steps:        # 集成步骤配置
     CopyARXML: yes          # 是否将ASW ARXML拷贝到工程目录下
     ImportARXML: yes        # 是否导入ASW ARXML
     TaskMapping: yes        # 是否执行TaskMapping
     PortMapping: no         # 是否执行PortMapping
     DataMapping: no         # 是否执行DataMapping
     ServiceMapping: no      # 是否执行ServiceMapping
     GenAllSchedule: yes     # 是否生成调度表
     Validation: yes         # 是否执行校验
     CodeGeneration: yes     # 是否执行代码生成

   ```

2. python_script\integrate_script\auto_integrate.py 中的 Config 可以根据集成需要进行配置，例如工程路径、TaskMapping、PortMapping等配置项

   ```python
   class Config:

       # 文件路径配置
       FILE_PATHS = {
           "Interface_File":   '',  # ASW Task部署信息文件路径
           "TaskMapping_BSW":  '',  # 导出BSW TaskMapping文件目标路径
           "TaskMapping":  '',      # TaskMapping文件路径
           "Project_Path":     '',  # VCOS工程路径
           "ARXML_Path":       '',  # VCOS工程中 ASW ARXML文件路径
       }

       # 选择TaskMapping的方式，可在VCOS工程导出的excel基础上修改后导入，也可使用列表进行Mapping
       TASK_MAPPING_METHOD = "excel"  # "excel" or "list"

       # DataMapping 配置，配置项含义可参考 VCOS API 描述文档
       DATAMAPPING_LIST: List[Dict[str, Any]] = [
           {
               "component": "",  # 可选参数，SWC Component名称
               "direction": "Tx",  # 可选参数，接口方向
               "prefix": None,  # 可选参数，Signal前缀
               "postfix": None,  # 可选参数，Signal后缀
               "ignore_match_whole_word": True,  # 可选参数，是否忽略全词匹配
               "ignore_match_case": False,  # 可选参数，是否忽略大小写匹配
               "allow_multi_signal": False,  # 可选参数，是否允许一个Port连接多个Signal
               "log_save": True,  # 可选参数，是否保存日志
               "match_compatibility": True  # 可选参数，是否兼容数据类型
           },
           {
               "component": "CanLinInputs_5ms",
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

       # Port mapping 配置，具体配置项含义可参考VCOS API描述文档
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

       # Service mapping 配置，具体配置项含义可参考VCOS API描述文档
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

       # 返回TaskMapping 列表，可直接返回列表或从别的文件中提取出列表后返回
       def get_task_mapping_list() -> List[Dict[str, Any]]:
           """
           Dynamically load task mapping configuration from external source.

           Returns:
               List of task mapping configurations
           """
           return [
               {
                   "task_name": "Default_BSW_Task_Core0",
                   "swc_name": "Client1",
                   "runnable_name": "Client1_Test_Runnable",
                   "position": 0
               }
           ]

       # 获取TaskMapping excel表格的地址，可直接返回地址或处理完表格后再返回表格地址
       def get_task_mapping_excel() -> Path:
           """
           Get the path to the task mapping excel file.

           Note: In real usage, this would export from VCOS project first,
           then return the path to the populated excel file.

           Returns:
               Path: Path to the task mapping excel file
           """
           return Path("path/to/taskmapping.xlsx")
   ```

#### 3.2.2 输入项

1. ARXML 文件：可将待集成的 ASW ARXML 文件放置于 input_files/ARXML 目录。集成脚本会自动将其拷贝至工程目录并批量导入。
2. interface.xlsx：包含 ASW Task 部署信息。通过 merge_taskmapping_xlsx.py 脚本可在 BSW 工程的 TaskMapping 表基础上附加 ASW Runnable Mapping，在实际项目可按需定制（需同步调整脚本）。

#### 3.2.3 集成步骤说明

以下为自动化集成的核心流程，具体每步的开启与否可在 yaml 配置文件灵活设置：

```python
# 1. Load project (所有操作前必须先加载工程)
load_project(Config.FILE_PATHS["Project_Path"])

# 2. Import ARXML （导入ARXML，可选是否从指定目录拷贝到工程下）
if INTEGRATE_CONFIG["Integration_steps"]["ImportARXML"]:
    if INTEGRATE_CONFIG["Integration_steps"]["CopyARXML"]:
        src_dict = {"local_ARXML": os.path.join(CUR_FILE_PATH, '..', '..', 'input_files/ARXML')}
        copy_ARXML_files(src_dict, Config.FILE_PATHS["ARXML_Path"])
    import_ARXML(Config.FILE_PATHS["ARXML_Path"])

# 3. Task mapping （可选TaskMapping的方式，在本示例中先从工程中导出TaskMapping信息，增加ASW信息后重新导入）
if INTEGRATE_CONFIG["Integration_steps"]["TaskMapping"]:
    if Config.TASK_MAPPING_METHOD == "excel":
        export_taskmapping_xlsx(Config.FILE_PATHS["TaskMapping_BSW"])
        task_mapping_excel_path = Config.get_task_mapping_excel()
        task_mapping_by_excel(task_mapping_excel_path)
    else:
        task_mapping_list = Config.get_task_mapping_list()
        task_mapping_by_list(task_mapping_list)

# 4. Port mapping 
if INTEGRATE_CONFIG["Integration_steps"]["PortMapping"]:
    port_mapping(Config.PORTMAPPING_LIST)

# 5. Service mapping
if INTEGRATE_CONFIG["Integration_steps"]["ServiceMapping"]:
    service_mapping(Config.SERVICEMAPPING_LIST)

# 6. Data mapping
if INTEGRATE_CONFIG["Integration_steps"]["DataMapping"]:
    data_mapping(Config.DATAMAPPING_LIST)

# 7. Generate all schedule tables （如果工程中配置了OS调度表，可选择是否更新调度表）
if INTEGRATE_CONFIG["Integration_steps"]["GenAllSchedule"]:
    generate_schedule_tables()

# 8. Validate project  （校验，默认只校验 OS 和 RTE两个模块, 可选择校验等级）
if INTEGRATE_CONFIG["Integration_steps"]["Validation"]:
    validate_project(["Os", "Rte"],"warnning") 

# 9. Generate code （代码生成，默认只生成 OS 和 RTE两个模块代码）
if INTEGRATE_CONFIG["Integration_steps"]["CodeGeneration"]:
    generate_code()

# 10. Save project （集成结束后必须保存工程，否则更改不生效）
save_project()
```

#### 3.2.4 自动化集成

1. 配置工程及文件：
    准备好VCOS BSW工程与ASW ARXML文件，根据需求调整配置文件（如工程名、路径、ARXML文件名等）。
2. 按需调整yaml集成流程：
    修改 auto_integrate/integrate_cfg.yaml，只开启自己关注的步骤。
3. 执行自动化集成：
    直接双击 auto_integrate/auto_integrate.bat 开始自动化集成。
4. 核查结果：
    检查接口连接状态、生成的 RTE、OS 代码等，确认集成效果。

## 4. 建议与说明

1. 本示例为集成流程演示，不是通用性解决方案。用户可以根据实际项目需求，灵活调用 VCOS API。
2. 强烈建议充分阅读相关 VCOS API 文档。
3. 项目结构设计、excel 表格格式、mapping方式等，均可根据团队实际习惯和业务场景调整。
4. 如需二次开发或功能扩展，可在 python_script 内补充自定义脚本。
