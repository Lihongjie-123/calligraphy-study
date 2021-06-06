import csv
import os
import sys
import logging
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem

from src.main.main_windows import Ui_Form as main_gui
from src.main.calligrapher_model import Ui_Form as calligrapher_gui
from src.main.editor_model import Ui_Form as editor_gui
from src.main.user_model import Ui_Form as user_gui
from src.main.ranking_list_show import Ui_MainWindow as rank_list_gui

from PyQt5 import QtCore, QtWidgets
import sys


class MainUi(QtWidgets.QMainWindow, main_gui):
    def __init__(self):
        super(main_gui, self).__init__()
        self.setupUi(self)


class CalligrapherUi(QtWidgets.QMainWindow, calligrapher_gui):
    def __init__(self):
        super(calligrapher_gui, self).__init__()
        self.setupUi(self)


class EditorUi(QtWidgets.QMainWindow, editor_gui):
    def __init__(self):
        super(editor_gui, self).__init__()
        self.setupUi(self)


class PractiseUi(QtWidgets.QMainWindow, user_gui):
    def __init__(self):
        super(user_gui, self).__init__()
        self.setupUi(self)


class RankListUi(QtWidgets.QMainWindow, rank_list_gui):
    def __init__(self):
        super(rank_list_gui, self).__init__()
        self.setupUi(self)


def get_csv_value(csv_name):
    if not csv_name:
        return
    return_result = []
    csv_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "var",
            "grade", "%s.csv" % csv_name)
    csv_file = open(csv_file_path, "r")
    csv_data = csv.reader(csv_file)
    first_count = 0
    for i in csv_data:
        if not first_count:
            first_count = 1
            continue
        return_result.append(i)
        if 10 == len(return_result):
            break
    csv_file.close()
    return return_result


def set_table_item(item_list, rank_list_action):
    try:
        if not item_list:
            return

        for sub_row in item_list:
            for sub_item in sub_row:
                item = QTableWidgetItem(sub_item)
                item.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                rank_list_action.tableWidget.setItem(
                    item_list.index(sub_row),
                    sub_row.index(sub_item),
                    item
                )
    except Exception as e:
        logging.exception(e)


def init_button_function(
        main_action,
        calligrapher_action,
        editor_action,
        practise_action,
        rank_list_action
    ):
    """
    初始化按钮功能
    :param main_action:
    :param calligrapher_action:
    :param editor_action:
    :param practise_action:
    :return:
    """
    main_action.calligrapher_button.clicked.connect(
        lambda: {
            main_action.change_prompt(),
            calligrapher_action.change_prompt(main_action.prompt_value),
            main_action.close(),
            calligrapher_action.show()
        }
    )
    main_action.editor_button.clicked.connect(
        lambda: {
            main_action.change_prompt(),
            editor_action.change_prompt(main_action.prompt_value),
            main_action.close(),
            editor_action._load_default(),
            editor_action.show()
        }
    )
    main_action.practise_button.clicked.connect(
        lambda: {
            main_action.change_prompt(),
            practise_action.change_prompt(main_action.prompt_value),
            main_action.close(),
            practise_action._load_default(),
            practise_action.show()
        }
    )
    main_action.exit_button.clicked.connect(lambda: {main_action.close()})

    calligrapher_action.return_index_button.clicked.connect(
        lambda: {
            calligrapher_action.truncate_board(),
            calligrapher_action.close(),
            main_action.show()
        }
    )

    editor_action.return_index_button.clicked.connect(
        lambda: {
            editor_action.truncate_board(),
            editor_action.close(),
            main_action.show()
        }
    )

    practise_action.return_index_button.clicked.connect(
        lambda: {
            practise_action.truncate_board(),
            practise_action.close(),
            main_action.show()
        }
    )

    practise_action.ranking_list_button.clicked.connect(
        lambda: {
            practise_action.close(),
            rank_list_action.label.setText(
                QtCore.QCoreApplication.translate(
                    "MainWindow",
                    "【%s】字练习排行榜" % practise_action.model_name
                )
            ),
            set_table_item(
                get_csv_value(practise_action.model_name),
                rank_list_action
            ),
            rank_list_action.show()
        }
    )

    rank_list_action.return_button.clicked.connect(
        lambda: {
            rank_list_action.close(),
            practise_action.show()
        }
    )


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    _translate = QtCore.QCoreApplication.translate
    main_action = MainUi()
    calligrapher_action = CalligrapherUi()
    editor_action = EditorUi()
    rank_list_action = RankListUi()
    practise_action = PractiseUi()
    init_button_function(
        main_action,
        calligrapher_action,
        editor_action,
        practise_action,
        rank_list_action
    )
    main_action.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
