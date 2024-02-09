# -*- coding: utf-8 -*-
"""
Query program for Custom 3LE

This program is the main functional program,
mainly used for processing specified parameters and querying data.

Author: BY7030SWL and BG7ZCM
Date: 2024/02/09
Version: 0.0.0 formal_edition
LICENSE: GNU General Public License v3.0
"""

import os
import requests
import sys
import subprocess
import json
import concurrent.futures
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser

# 错误处置
def GUI_jump():
    jump = 0
    if len(sys.argv) < 2 and jump == 0:
        custom_gui_path = "Custom_GUI.exe"
        command = f'{custom_gui_path}'
        subprocess.run(command, shell=True)
        jump = jump+1
    else:
        print('')

# 读取配置文件
def read_config():
    config = ConfigParser(allow_no_value=True)
    try:
        config.read("date.ini")
    except Exception as e:
        print(f"#*Error*# 1: 读取配置文件时错误: {e}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()
    return config

# 读取存储路径
def read_save_path(config):
    try:
        save_path = config["Path"]["SavePath"]
    except KeyError:
        print("#*Error*# 2: 配置文件中的存储路径可能存在错误，没有找到 'Path' 或 'SavePath'。\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()
        # 如果这里出错，确保退出函数或提前返回一个默认值
        return "default_save_path"
    return save_path


# 读取NORAD表
def read_norad_ids(config):
    try:
        norad_ids = [json.loads(value) for value in config["NORAD_List"].values()]
    except KeyError:
        print("#*Error*# 3: 配置文件中没有发现 NORAD_List。\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()
    except (json.JSONDecodeError, ValueError) as e:
        print(f"#*Error*# 4: 无法解析 NORAD ID：{e}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()
    return norad_ids

# 将TLE列表保存到文件
def save_tle_to_file(tle_list, save_path, custom_file_name):
    try:
        file_name = f"{custom_file_name}" if custom_file_name else "Custom.txt"
        file_path = os.path.abspath(os.path.join(save_path, file_name))

        os.makedirs(save_path, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            for tle_text in tle_list:
                file.write(tle_text + '\n\n')
    except Exception as e:
        print(f"#*Error*# 5: 存储星历到文件时错误: \n{e}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()

# 构造并查询
def query_satellite(norad_id, tle_list, satellite_names):
    try:
        url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=3LE"
        response = requests.get(url)

        if response.status_code == 200:
            raw_text = response.text
            cleaned_text = '\n'.join(line.strip() for line in raw_text.split('\n'))

            lines = cleaned_text.split('\n')
            if lines[1][0] != '1' or lines[2][0] != '2':
                print(f"#*Error*# 6: 返回数据有误：{cleaned_text}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
                GUI_jump()

            # 将 TLE 和卫星名分别附加到相应的列表中
            tle_list.append(cleaned_text)
            satellite_names.append(lines[0])

        else:
            print(f"#*Error*# 7: HTTP请求失败，状态码: {response.status_code}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
            messagebox.showinfo("HTTP请求失败", f"状态码: {response.status_code}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
            GUI_jump()

    except Exception as e:
        print(f"#*Error*# 8: 查询{norad_id}出现错误：{e}，请检查你的编号是否正确。\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()

# 多线程并发查询
def run_query_script_parallel(norad_ids=None):
    config = read_config()
    save_path = read_save_path(config)
    
    try:
        if not norad_ids:
            norad_ids = read_norad_ids(config)

        # 创建每个线程独立的列表
        tle_lists = [[] for _ in norad_ids]
        satellite_names_lists = [[] for _ in norad_ids]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 将 tle_list 和 satellite_names 作为参数传递给 query_satellite 函数
            futures = [executor.submit(query_satellite, norad_id, tle_list, satellite_names)
                       for norad_id, tle_list, satellite_names in zip(norad_ids, tle_lists, satellite_names_lists)]
            concurrent.futures.wait(futures)

    except Exception as e:
        print(f"#*Error*# 9: 多线程查询时发生错误：{e}\n\n如果无法解决，请在我们的GitHub仓库提交issue。")
        GUI_jump()

    # 合并每个线程的结果
    tle_list = [tle for tle_list in tle_lists for tle in tle_list]
    satellite_names = [name for names_list in satellite_names_lists for name in names_list]

    custom_file_name = config["FileName"].get("FileName", "")
    save_tle_to_file(tle_list, save_path, custom_file_name)

    print(satellite_names)
    sys.exit()


# 主事件
if __name__ == "__main__":
    if len(sys.argv) < 2:
        run_query_script_parallel()
        print("更新完成：自定义星历已按指定参数自动更新。")
    else:
        command_line_norad_ids = sys.argv[1:]
        run_query_script_parallel(command_line_norad_ids)
        print("更新完成：自定义星历已按文件配置自动更新。")