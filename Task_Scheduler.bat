:: Task Scheduler module for Custom 3LE
:: This module is mainly used to create scheduled tasks (temporary solutions),
:: which will be integrated into the GUI program later.
::
:: Author: BY7030SWL and BG7ZCM
:: Date: 2024/02/08
:: Version: 0.0.0 beta
:: LICENSE: GNU General Public License v3.0

CHCP 65001
@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 提示：请以管理员权限运行此脚本。
    exit /b 1
)
set TASK_NAME=Custom_3LE_Query
set EXE_PATH=\"%CD%\Custom_Query.exe\"
echo "%EXE_PATH%"

schtasks /query /tn "%TASK_NAME%" 2>nul
if %errorlevel% equ 0 (
    schtasks /delete /tn "%TASK_NAME%" /f
    timeout /t 2 /nobreak  >nul
)

if "%1"=="" (
    echo 请提供参数！
    exit /b 1
) else (
    if "%1"=="OnLogon" (
        schtasks /create /tn "%TASK_NAME%" /tr "%EXE_PATH%" /sc ONLOGON
    )

    if "%1"=="Daily" (
        schtasks /create /tn "%TASK_NAME%" /tr "%EXE_PATH%" /sc DAILY /st 11:00
    )

    if "%1"=="Weekly" (
        schtasks /create /tn "%TASK_NAME%" /tr "%EXE_PATH%" /sc WEEKLY /d MON /st 11:00
    )

    if "%1"=="Monthly" (
        schtasks /create /tn "%TASK_NAME%" /tr "%EXE_PATH%" /sc MONTHLY /mo 1 /st 11:00
    )

    if not "%1"=="OnLogon" if not "%1"=="Daily" if not "%1"=="Weekly" if not "%1"=="Monthly" (
        echo 无效的参数！
        exit /b 1
    )
)
