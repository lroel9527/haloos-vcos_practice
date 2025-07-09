@echo off
cd /d "%~dp0\..\..\..\"

REM 判断虚拟环境的激活脚本是否存在
if exist ".venv\Scripts\activate.bat" (
    echo 检测到虚拟环境已存在，跳过初始化和依赖安装
) else (
    echo 未检测到虚拟环境，正在初始化...
    REM 这里你可以用 pip/conda/python -m venv 创建虚拟环境的命令
    python -m venv .venv
    call .\.venv\Scripts\activate.bat
    REM 如需初始化环境，可解开下面一行注释
    python ./vcos_studio/configurator/init_env.py -a
)

REM 激活虚拟环境
call .\.venv\Scripts\activate.bat
REM 在虚拟环境中安装pandas
pip install pandas 
cd %~dp0
cd ..\python_script\integrate_script
python auto_integrate.py
pause
