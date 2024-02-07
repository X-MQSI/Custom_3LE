# -*- coding: utf-8 -*-
"""
GUI program for Custom 3LE

This program is a graphical user interface implemented using PyQt, 
mainly used to obtain software running parameters.

Author: BY7030SWL and BG7ZCM
Date: 2024/02/08
Version: 0.0.0 beta
LICENSE: GNU General Public License v3.0
"""

import sys
import ast
import ctypes
import subprocess
from configparser import RawConfigParser
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QPlainTextEdit, QMessageBox

# 组件样式
title_style = 'color: #3063AB; font-family: 微软雅黑; font: bold 12pt;'
common_style = 'color: #3063AB; font-family: 微软雅黑; font: bold 10pt;'
Common_button_style = 'QPushButton {background-color: #3498db; color: #ffffff; border-radius: 5px; padding: 6px; font-size: 12px;} QPushButton:hover {background-color: #2980b9;} QPushButton:pressed {background-color: #21618c;}'
Update_button_style = 'QPushButton {background-color: #FFFFFF; color: #000000; border: 1px solid #CCCCCC; border-radius: 4px; font-size: 12px;} QPushButton:hover {background-color: #89CFF0;} QPushButton:pressed {background-color:#B6D0E2;}'
Update_choose_button_style = 'QPushButton {background-color: #FFFFFF; color: #6495ED; border: 1px solid #CCCCCC; border-radius: 4px; font-size: 12px;} QPushButton:hover {background-color: #89CFF0;} QPushButton:pressed {background-color:#B6D0E2;}'
TextEdit_style = 'QPlainTextEdit {background-color: #FFFFFF; color: #3063AB; border: 1px solid #3498db; border-radius: 5px; padding: 1px; font-family: 微软雅黑; font-size: 12px;}'

config = RawConfigParser()
config.optionxform = str
config.read("date.ini")

# 程序主窗口
class Custom_3LE_GUI(QWidget):

    # 设置窗口与程序图标
    def __init__(self):
        super().__init__()

        # 窗口属性
        icon = QIcon('UI/Custom 3LE.ico')
        self.setWindowIcon(icon)
        self.resize(800, 500)
        self.setFixedSize(800, 500)
        self.setWindowTitle('Custom 3LE By BY7030SWL - Ver 0.0.0')
        self.setStyleSheet('QWidget { background-color: rgb(223,237,249); }')
        self.setWindowOpacity(0.90)

        # 设置主程序图标
        global waiting, correct, warning, error
        waiting = QPixmap('UI/waiting.svg')
        correct = QPixmap('UI/correct.svg')
        warning = QPixmap('UI/warning.svg')
        error = QPixmap('UI/error.svg')

        # 初始化字典
        self.Status_dict = {
            "Path_selection_pilot_lamp": "waiting",
            "Update_frequency_pilot_lamp": "waiting",
            "Satellite_NARAD_input_pilot_lamp": "waiting",
            "Update_frequency": " ",
        }

        # 强制管理员权限运行
        def check_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if check_admin():
            print("正在以管理员权限运行。")
            # 在这里执行需要管理员权限的操作
        else:
            QMessageBox.information(None, "提示：", "本程序需要使用管理员权限运行！")
            sys.exit()

        self.UI()

    # 主窗口
    def UI(self):

        '''左栏'''
        # 路径选择部分
        self.Path_selection_pilot_lamp = QLabel(self)
        self.Path_selection_pilot_lamp.setPixmap(waiting)
        self.Path_selection_pilot_lamp.move(40, 28)

        self.Path_selection_label = QLabel(self)
        self.Path_selection_label.setText("请选择自定义星历的更新存储路径：")
        self.Path_selection_label.move(65, 25)
        self.Path_selection_label.setStyleSheet(title_style)

        self.Path_selection_button = QPushButton("选择", self)
        self.Path_selection_button.setGeometry(320, 22, 50, 27)
        self.Path_selection_button.setStyleSheet(Common_button_style)
        self.Path_selection_button.clicked.connect(self.Path_selection)

        self.Path_output = QPlainTextEdit(self)
        self.Path_output.setReadOnly(True)
        self.Path_output.setGeometry(40, 60, 330, 50)
        self.Path_output.setStyleSheet(TextEdit_style)
        self.Path_output.clear()

        # 更新频率选择部分
        self.Update_frequency_pilot_lamp = QLabel(self)
        self.Update_frequency_pilot_lamp.setPixmap(waiting)
        self.Update_frequency_pilot_lamp.move(40, 128)

        self.Update_frequency_OnLogon_label = QLabel(self)
        self.Update_frequency_OnLogon_label.setText("请选择星历自动更新触发器：")
        self.Update_frequency_OnLogon_label.move(65, 125)
        self.Update_frequency_OnLogon_label.setStyleSheet(title_style)

        self.Update_frequency_OnLogon_button = QPushButton("自动更新：每次开机时(推荐)", self)
        self.Update_frequency_OnLogon_button.setGeometry(40, 155, 330, 32)
        self.Update_frequency_OnLogon_button.setStyleSheet(Update_button_style)
        self.Update_frequency_OnLogon_button.clicked.connect(self.Update_frequency_OnLogon)

        self.Update_frequency_Daily_button = QPushButton("自动更新：每天一次", self)
        self.Update_frequency_Daily_button.setGeometry(40, 190, 330, 32)
        self.Update_frequency_Daily_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Daily_button.clicked.connect(self.Update_frequency_Daily)

        self.Update_frequency_Weekly_button = QPushButton("自动更新：每周一次", self)
        self.Update_frequency_Weekly_button.setGeometry(40, 225, 330, 32)
        self.Update_frequency_Weekly_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Weekly_button.clicked.connect(self.Update_frequency_Weekly)

        self.Update_frequency_Monthly_button = QPushButton("自动更新：每月一次", self)
        self.Update_frequency_Monthly_button.setGeometry(40, 260, 330, 32)
        self.Update_frequency_Monthly_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Monthly_button.clicked.connect(self.Update_frequency_Monthly)

        self.Update_frequency_label = QLabel(self)
        self.Update_frequency_label.setText("您选择的更新方式是：")
        self.Update_frequency_label.move(45, 300)
        self.Update_frequency_label.setStyleSheet(title_style)

        self.Update_frequency_output = QPlainTextEdit(self)
        self.Update_frequency_output.setReadOnly(True)
        self.Update_frequency_output.setGeometry(40, 335, 330, 45)
        self.Update_frequency_output.setStyleSheet(TextEdit_style)

        # 项目开源与致谢
        self.Github_repository_title_label = QLabel(self)
        self.Github_repository_title_label.setText("项目开源：")
        self.Github_repository_title_label.move(40, 400)
        self.Github_repository_title_label.setStyleSheet(common_style)

        self.Github_repository_label = QLabel('<style> a {text-decoration: none; vertical-align: top;} </style><a href="https://github.com/X-MQSI/Custom_3LE"><img src="UI/github.svg" >  GitHub开源项目</a>', self)
        self.Github_repository_label.linkActivated.connect(self.handle_link_activated)
        self.Github_repository_label.move(40, 425)
        self.Github_repository_label.setStyleSheet(common_style)
        self.Github_repository_label.setOpenExternalLinks(True)
        self.Github_repository_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.Acknowledgments_label = QLabel(self)
        self.Acknowledgments_label.setText("致谢：")
        self.Acknowledgments_label.move(40, 455)
        self.Acknowledgments_label.setStyleSheet(common_style)

        self.Github_repository_label = QLabel('<style> a {text-decoration: none; vertical-align: top;} </style><a href="https://icons.getbootstrap.com/"><img src="UI/bootstrap.svg" >  Bootstrap Icon  |  </a><a href="https://celestrak.org/"><img src="UI/CelesTrak.ico" >  CelesTrak  |  </a><a href="https://www.n2yo.com/"><img src="UI/N2YO.ico" >  N2YO</a>', self)
        self.Github_repository_label.linkActivated.connect(self.handle_link_activated)
        self.Github_repository_label.move(80, 455)
        self.Github_repository_label.setStyleSheet(common_style)
        self.Github_repository_label.setOpenExternalLinks(True)
        self.Github_repository_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        '''右栏'''
        # 卫星NORAD编号参考
        self.Satellite_NARAD_title_label = QLabel(self)
        self.Satellite_NARAD_title_label.setText("参考编号(在右下角查看更多)：")
        self.Satellite_NARAD_title_label.move(420, 25)
        self.Satellite_NARAD_title_label.setStyleSheet(title_style)

        self.Satellite_NARAD_reference_label = QLabel(self)
        self.Satellite_NARAD_reference_label.setText("紫丁香2号: 40908     SO-50: 27607        ISS: 25544\nTEVEL-2:   51069     TEVEL-3: 50988     TEVEL-4: 51063\nTEVEL-5:   50998     TEVEL-6: 50999     TEVEL-7: 51062")
        self.Satellite_NARAD_reference_label.move(420, 60)
        self.Satellite_NARAD_reference_label.setStyleSheet(common_style)

        # 卫星NORAD编号输入
        self.Satellite_NARAD_input_pilot_lamp = QLabel(self)
        self.Satellite_NARAD_input_pilot_lamp.setPixmap(waiting)
        self.Satellite_NARAD_input_pilot_lamp.move(420, 128)

        self.Satellite_NARAD_input_title_label = QLabel(self)
        self.Satellite_NARAD_input_title_label.setText("请输入目标卫星的编号（每行一个）：")
        self.Satellite_NARAD_input_title_label.move(445, 125)
        self.Satellite_NARAD_input_title_label.setStyleSheet(title_style)

        self.Satellite_NARAD_input = QPlainTextEdit(self)
        self.Satellite_NARAD_input.setGeometry(420, 155, 330, 65)
        self.Satellite_NARAD_input.setStyleSheet(TextEdit_style)

        self.Path_selection_button = QPushButton("确认", self)
        self.Path_selection_button.setGeometry(420, 228, 50, 27)
        self.Path_selection_button.setStyleSheet(Common_button_style)
        self.Path_selection_button.clicked.connect(self.NORAD_Query)

        # 卫星查询输出
        self.Satellite_NARAD_output_title_label = QLabel(self)
        self.Satellite_NARAD_output_title_label.setText("这是将自动更新的卫星名：")
        self.Satellite_NARAD_output_title_label.move(420, 262)
        self.Satellite_NARAD_output_title_label.setStyleSheet(title_style)

        self.Satellite_NARAD_output = QPlainTextEdit(self)
        self.Satellite_NARAD_output.setReadOnly(True)
        self.Satellite_NARAD_output.setGeometry(420, 290, 330, 90)
        self.Satellite_NARAD_output.setStyleSheet(TextEdit_style)
        self.Satellite_NARAD_output.clear()

        # 提示
        self.hint_label = QLabel(self)
        self.hint_label.setText("请仔细检查如上信息，无误后方可点击保存！")
        self.hint_label.move(420, 400)
        self.hint_label.setStyleSheet(common_style)

        # 查看卫星编号、保存
        self.Commonly_used_satellites_button = QPushButton("查看常用卫星", self)
        self.Commonly_used_satellites_button.setGeometry(520, 440, 90, 32)
        self.Commonly_used_satellites_button.setStyleSheet(Common_button_style)
        self.Commonly_used_satellites_button.clicked.connect(self.Commonly_used_satellites)

        self.save_button = QPushButton("保存", self)
        self.save_button.setGeometry(630, 440, 50, 32)
        self.save_button.setStyleSheet(Common_button_style)
        self.save_button.clicked.connect(self.save_date)

        self.exit_button = QPushButton("取消", self)
        self.exit_button.setGeometry(700, 440, 50, 32)
        self.exit_button.setStyleSheet(Common_button_style)
        self.exit_button.clicked.connect(QApplication.instance().quit)

        '''自动选择'''
        # 全局变量
        global save_path, Satellite_Names, User_NORAD_input
        try:
            # 获取预置NORAD编号与名称
            Satellite_Names = config.options("NORAD_List")
            User_NORAD_input = []
            if Satellite_Names:
                self.Satellite_NARAD_output.appendPlainText('\n'.join(Satellite_Names))
                for satellite_name in Satellite_Names:
                    try:
                        satellite_value = config.get("NORAD_List", satellite_name)
                        User_NORAD_input.append(satellite_value)
                    except Exception as e:
                        # 处理获取 NORAD_List 中配置值的异常
                        print(e)
                self.Satellite_NARAD_input.appendPlainText('\n'.join(User_NORAD_input))

            self.Assembly(User_NORAD_input, Satellite_Names)

            # 获取更新路径
            try:
                save_path = config.get("Path", "SavePath")
                self.Path_output.appendPlainText(f"路径：{save_path}")
                if len(save_path) != 0:
                    self.Path_selection_pilot_lamp.setPixmap(correct)
                    self.Status_dict["Path_selection_pilot_lamp"] = "correct"
            except Exception as e:
                # 处理获取 Path 中配置值的异常
                print(e)

            # 获取更新频率
            try:
                Update_keys = config.get("Update", "Frequency")
                if Update_keys == 'OnLogon':
                    self.Update_frequency_OnLogon()
                elif Update_keys == 'Daily':
                    self.Update_frequency_Daily()
                elif Update_keys == 'Weekly':
                    self.Update_frequency_Weekly()
                elif Update_keys == 'Monthly':
                    self.Update_frequency_Monthly()
                else:
                    self.Update_frequency_pilot_lamp.setPixmap(error)
                    self.Status_dict["Update_frequency_pilot_lamp"] = "error"
                    QMessageBox.warning(self, "错误！", "配置文件配置错误，已忽略错误配置。")
            except Exception as e:
                # 处理获取 Update 中配置值的异常
                print(e)

        except Exception as e:
            # 处理其他异常
            QMessageBox.information(self, "提示：", f"未读取到预置参数，请自行选择！")


    # 路径选择函数
    def Path_selection(self):
        global save_path
        save_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        save_path = save_path.strip()
        if save_path:
            self.Path_output.clear()
            self.Path_selection_pilot_lamp.setPixmap(correct)
            self.Status_dict["Path_selection_pilot_lamp"] = "correct"
            self.Path_output.appendPlainText(f"路径：{save_path}")
            try:
                config.set("Path", "SavePath", save_path)
                with open("date.ini", "w") as configfile:
                    config.write(configfile)
            except Exception as e:
                self.Status_dict["Path_selection_pilot_lamp"] = "error"
                QMessageBox.critical(self, "错误", f"存储信息到配置文件失败！\n{e}")
        else:
            self.Path_selection_pilot_lamp.setPixmap(warning)
            self.Status_dict["Path_selection_pilot_lamp"] = "warning"
            QMessageBox.warning(self, "警告！", "请您选择存储路径！")


    # 处理链接激活事件，打开浏览器访问链接
    def handle_link_activated(self, link):
        QDesktopServices.openUrl(QUrl(link))

    # 触发器：每次开机时
    def Update_frequency_OnLogon(self):
        self.Status_dict["Update_frequency"] = "OnLogon"
        self.Update_frequency_output.clear()
        self.Update_frequency_output.appendPlainText("自动更新：每次开机时")
        self.Update_frequency_pilot_lamp.setPixmap(correct)
        self.Status_dict["Update_frequency_pilot_lamp"] = "correct"
        self.Update_frequency_OnLogon_button.setStyleSheet(Update_choose_button_style)
        self.Update_frequency_Daily_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Weekly_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Monthly_button.setStyleSheet(Update_button_style)
        QMessageBox.information(self, "更新频率", "星历将在每次开机时自动更新。")

    # 触发器：每天一次
    def Update_frequency_Daily(self):
        self.Status_dict["Update_frequency"] = "Daily"
        self.Update_frequency_output.clear()
        self.Update_frequency_output.appendPlainText("自动更新：每天一次")
        self.Update_frequency_pilot_lamp.setPixmap(correct)
        self.Status_dict["Update_frequency_pilot_lamp"] = "correct"
        self.Update_frequency_OnLogon_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Daily_button.setStyleSheet(Update_choose_button_style)
        self.Update_frequency_Weekly_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Monthly_button.setStyleSheet(Update_button_style)
        QMessageBox.information(self, "更新频率", "星历将每天自动更新。")

    # 触发器：每周一次
    def Update_frequency_Weekly(self):
        self.Status_dict["Update_frequency"] = "Weekly"
        self.Update_frequency_output.clear()
        self.Update_frequency_output.appendPlainText("自动更新：每周一次")
        self.Update_frequency_pilot_lamp.setPixmap(correct)
        self.Status_dict["Update_frequency_pilot_lamp"] = "correct"
        self.Update_frequency_OnLogon_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Daily_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Weekly_button.setStyleSheet(Update_choose_button_style)
        self.Update_frequency_Monthly_button.setStyleSheet(Update_button_style)
        QMessageBox.information(self, "更新频率", "星历每个周将自动更新。")

    # 触发器：每月一次
    def Update_frequency_Monthly(self):
        self.Status_dict["Update_frequency"] = "Monthly"
        self.Update_frequency_output.clear()
        self.Update_frequency_output.appendPlainText("自动更新：每月一次")
        self.Update_frequency_pilot_lamp.setPixmap(correct)
        self.Status_dict["Update_frequency_pilot_lamp"] = "correct"
        self.Update_frequency_OnLogon_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Daily_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Weekly_button.setStyleSheet(Update_button_style)
        self.Update_frequency_Monthly_button.setStyleSheet(Update_choose_button_style)
        QMessageBox.information(self, "更新频率", "星历每个月将自动更新。")

    # NORAD 编号与卫星名称对应
    def Assembly(self, User_NORAD_input, Satellite_Names):
        mapping_dict = dict(zip(User_NORAD_input, Satellite_Names))
        Satellite_output_dict = {str(satellite_name): int(norad) for norad, satellite_name in mapping_dict.items()}
        self.Status_dict["Satellite_output"] = Satellite_output_dict

    # 传参到Query程序进行查询
    def NORAD_Query(self):
        NORAD_ID = self.Satellite_NARAD_input.toPlainText()
        try:
            User_NORAD_input = NORAD_ID.strip().splitlines()
            User_NORAD_input = [int(item) for item in User_NORAD_input]

            lines = NORAD_ID.strip().split('\n')
            NORAD_ID = ' '.join(lines)
            if len(NORAD_ID) != 0:
                command = f"Custom_Query.exe {NORAD_ID}"
                QMessageBox.information(self, "提示：", "正在查询验证，程序可能会无响应，请耐心等待。\n\n读到这行文字，你就可以关闭这个提示窗口了。")
    
                try:
                    Satellite_Names = subprocess.run(command, shell=True, capture_output=True, text=True)
                except Exception as e:
                    QMessageBox.critical(self, "致命错误！", f"请检查程序完整性！\n{e}")
                print("Satellite_Names:", Satellite_Names)
                Satellite_Names = Satellite_Names.stdout.strip()
                print("Satellite_Names:", Satellite_Names)
                Satellite_Names = ast.literal_eval(Satellite_Names)
    
                if "#*Error*#" in Satellite_Names or len(Satellite_Names) == 0:
                    # 获取错误信息
                    error_message = Satellite_Names
                    if len(Satellite_Names) == 0:
                        error_message = "未获得返回，请检查程序完整性！"
                    QMessageBox.critical(self, "查询错误", f"查询过程中发生错误：{error_message}")
                    self.Satellite_NARAD_input_pilot_lamp.setPixmap(error)
                    self.Status_dict["Satellite_NARAD_input_pilot_lamp"] = "error"
                else:
                    self.Satellite_NARAD_input_pilot_lamp.setPixmap(correct)
                    self.Status_dict["Satellite_NARAD_input_pilot_lamp"] = "correct"
                    self.Satellite_NARAD_output.clear()
                    self.Satellite_NARAD_output.appendPlainText(str('\n'.join(Satellite_Names)))
                    self.Assembly(User_NORAD_input, Satellite_Names)
                    QMessageBox.information(self, "更新频率", "您选择的卫星的星历将按配置自动更新！")
            else:
                self.Satellite_NARAD_input_pilot_lamp.setPixmap(warning)
                self.Status_dict["Satellite_NARAD_input_pilot_lamp"] = "warning"
                QMessageBox.information(self, "提示：", "您还没有输入卫星的NORAD编号！")
        except Exception as e:
            self.Satellite_NARAD_input_pilot_lamp.setPixmap(error)
            self.Status_dict["Satellite_NARAD_input_pilot_lamp"] = "error"
            NORAD_ID == ''
            QMessageBox.warning(self, "错误", f"格式化失败，请检查您的输入！\n{e}")

    # 点击打开常用业余卫星窗口
    def Commonly_used_satellites(self):
        self.Commonly_used_satellites_window = None
        if not self.Commonly_used_satellites_window:
            self.Commonly_used_satellites_window = Commonly_used_satellites()
        self.Commonly_used_satellites_window.show()

    # 保存程序参数、退出
    def save_date(self):
        # 读取状态指示
        path_selection_state = self.Status_dict.get("Path_selection_pilot_lamp", "waiting")
        update_frequency_state = self.Status_dict.get("Update_frequency_pilot_lamp", "waiting")
        satellite_narad_input_state = self.Status_dict.get("Satellite_NARAD_input_pilot_lamp", "waiting")
        Update_frequency = self.Status_dict.get("Update_frequency", " ")

        # 判断是否完成所有操作
        if path_selection_state != 'correct':
            QMessageBox.information(self, "提示：", "您还没有选择有效保存路径！")
            self.Path_selection()
        elif update_frequency_state != 'correct':
            QMessageBox.information(self, "提示：", "您还没有选择更新频率！")
        elif satellite_narad_input_state != 'correct':
            QMessageBox.information(self, "提示：", "请检查是否正确输入卫星NORAD编号！")


        else:  # 所有操作已完成，进行存储执行
            try:

                config.remove_section("NORAD_List")
                config.add_section("NORAD_List")

                # 更新或添加新的配置项
                config.set("Path", "SavePath", save_path)
                config.set("Update", "Frequency", Update_frequency)
                for satellite, NORAD_number in self.Status_dict["Satellite_output"].items():
                    config.set("NORAD_List", satellite, str(NORAD_number))

                # 写入新的配置
                with open("date.ini", "w") as configfile:
                    config.write(configfile)

            except Exception as e:
                self.Status_dict["Path_selection_pilot_lamp"] = "error"
                QMessageBox.critical(self, "错误", f"存储信息到配置文件失败！\n{e}")


            # 设置计划任务
            try:
                command = f"Task_Scheduler.bat {Update_frequency}"
                subprocess.run(command, shell=True)
            except Exception as e:
                self.Update_frequency_pilot_lamp.setPixmap(error)
                self.Status_dict["Update_frequency_pilot_lamp"] = "error"
                QMessageBox.critical(self, "错误", f"添加到计划任务时发生错误：{e}")
                print(e)

            QMessageBox.information(self, "感谢使用", "所有操作已完成，配置已存储！")
            sys.exit()

    
    # 窗口关闭事件处理
    def closeEvent(self, event):
        warn = QMessageBox.question(self, "提示", "您尚未保存，是否退出？（可能会造成意想不到的后果）", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if warn == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

# 常用业余卫星窗口
class Commonly_used_satellites(QWidget):

    # 设置窗口与程序图标
    def __init__(self):
        super().__init__()

        # 窗口属性
        icon = QIcon('UI/Custom 3LE.ico')
        self.setWindowIcon(icon)
        self.resize(400, 500)
        self.setFixedSize(400, 500)
        self.setWindowTitle('常用业余卫星NORAD编号：')
        self.setStyleSheet('QWidget { background-color: rgb(223,237,249); }')
        self.setWindowOpacity(0.90)

        self.Satellite_UI()

    # 常用业余卫星窗口
    def Satellite_UI(self):

        # 常用业余卫星编号表
        self.Satellite_NARAD_title_label = QLabel(self)
        self.Satellite_NARAD_title_label.setText("常用业余卫星参考编号：")
        self.Satellite_NARAD_title_label.move(20, 25)
        self.Satellite_NARAD_title_label.setStyleSheet(title_style)

        self.Satellite_NARAD_reference_label = QLabel(self)
        self.Satellite_NARAD_reference_label.setText("紫丁香2号: 40908     SO-50:    27607     国际空间站:25544\n\nTEVEL-2:   51069     TEVEL-3: 50988     TEVEL-4:    51063\n\nTEVEL-5:   50998     TEVEL-6: 50999     TEVEL-7:    51062\n\nCAS-4A:   42761     CAS-4B:  42759     FO-29:       24278\n\nAO-109:   47311     AO-73:    39444     AO-7:        7530\n\nAO-91:     43017     AO-92:    43137     NO-44:     26931\n\nIO-117:     53106     IO-86:     40931     QO-100:   43700\n\nJAISAT-1: 44419     JO-97:     43803     PO-101:   43678")
        self.Satellite_NARAD_reference_label.move(20, 70)
        self.Satellite_NARAD_reference_label.setStyleSheet(common_style)

        # 查看卫星编号、保存
        self.Query_satellites_NORAD_button = QPushButton("搜索更多卫星编号", self)
        self.Query_satellites_NORAD_button.setGeometry(230, 350, 150, 32)
        self.Query_satellites_NORAD_button.setStyleSheet(Common_button_style)
        self.Query_satellites_NORAD_button.clicked.connect(self.Query_satellites_NORAD)

    # 处理链接激活事件，打开浏览器访问链接
    def Query_satellites_NORAD(self):
        QDesktopServices.openUrl(QUrl("https://www.n2yo.com/database/"))

# 主事件
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Custom_3LE_GUI()
    GUI.show()
    sys.exit(app.exec())