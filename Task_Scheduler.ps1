# Task Scheduler module for Custom 3LE
# This module is mainly used to create scheduled tasks (temporary solutions),
# which will be integrated into the GUI program later.
#
# Author: BY7030SWL and BG7ZCM
# Date: 2024/02/08
# Version: 0.0.0 beta
# LICENSE: GNU General Public License v3.0

# 设置输出编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 任务名称
$TaskName = "Custom_3LE_Query"

# 可执行文件路径
$ExePath = "$PSScriptRoot\Custom_Query.exe"
Write-Host "$ExePath"

# 检查任务是否已存在
$taskExists = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($taskExists) {
    # 如果任务已存在，则注销它
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Start-Sleep -Seconds 2
}

# 检查是否提供了参数
if (-not $args) {
    Write-Host "Please provide parameters!"
    exit 1
} else {
    # 如果参数是 "Remove"，则只执行移除任务计划的操作
    if ($args[0] -eq "Remove") {
        Write-Host "Remove scheduled tasks..."
        exit 0
    }

    # 根据提供的参数设置触发器
    switch ($args[0]) {
        "OnLogon" {
            $trigger = New-ScheduledTaskTrigger -AtLogon
            $location = "$PSScriptRoot"
        }
        "Daily" {
            $trigger = New-ScheduledTaskTrigger -Daily -At 11am
            $location = "$PSScriptRoot"
        }
        "Weekly" {
            $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 11am
            $location = "$PSScriptRoot"
        }
        "Monthly" {
            $trigger = New-ScheduledTaskTrigger -Monthly -At 11am -Months 1
            $location = "$PSScriptRoot"
        }
        default {
            Write-Host "Invalid parameter!"
            exit 1
        }
    }

    # 创建 Action 对象
    $action = New-ScheduledTaskAction -Execute "$ExePath" -WorkingDirectory $location

    # 注册计划任务
    Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $TaskName
}