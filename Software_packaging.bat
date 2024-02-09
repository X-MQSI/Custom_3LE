:: 软件封装调试专用
::
:: Author: BY7030SWL and BG7ZCM
:: Date: 2024/02/09
:: Version: 0.0.0 formal_edition
:: LICENSE: GNU General Public License v3.0

CHCP 65001

pyinstaller --onefile --clean -F -w -i "UI/CelesTrak.ico" "Custom_Query.py"
pyinstaller --onefile --clean --uac-admin -F -w -i "UI/Custom 3LE.ico" "Custom_GUI.py"

move .\dist\Custom_GUI.exe .\
move .\dist\Custom_Query.exe .\

del Custom_GUI.spec
echo 已删除文件: Custom_GUI.spec

del Custom_Query.spec
echo 已删除文件: Custom_Query.spec

rmdir /s /q dist
echo 已删除目录: dist

rmdir /s /q build
echo 已删除目录: build

(
echo ;0.0.0 official version configuration file.
echo [Path]
echo.
echo [FileName]
echo filename = Custom.txt
echo.
echo [Update]
echo.
echo [NORAD_List]
) > date.ini

:: 打包完成后启动 Custom_GUI.exe
start Custom_GUI.exe
