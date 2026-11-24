"""
Profiler Assistant - Maya 2026
"""
import os
import maya.cmds as cmds
from pathlib import Path
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QThread, Signal
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import re

import profiler_recording
import profiler_evaluatio_speedUp

from ProfilerAssistant_ui_v2 import Ui_Widget


# Shared palette — slice with [:n] to fit any number of bars/wedges
PALETTE = ['#378ADD', '#1D9E75', '#D85A30', '#BA7517', '#D4537E']


class EvaluateWorker(QThread):
    progress = Signal(int)
    finished = Signal(object)  # passes results back

    def __init__(self, files, top_n):
        super().__init__()
        self.files = files
        self.top_n = top_n

    def run(self):
        result = profiler_evaluatio_speedUp.execute_profiling(
            self.files, self.top_n, self.progress.emit
        )
        self.finished.emit(result)


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(facecolor='#2b2b2b')
        self.fig.subplots_adjust(left=0.08, right=0.97, top=0.95, bottom=0.35)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.ax.set_facecolor('#2b2b2b')
        self.ax.set_axis_off()
        self.ax.text(0.5, 0.5, "Nothing has been evaluated",
                     transform=self.ax.transAxes,
                     ha='center', va='center',
                     color='grey', fontsize=12)
        self.setParent(parent)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.updateGeometry()

    def plot_bar(self, labels, values):
        self.ax.clear()
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#555555')
        self.ax.bar(labels, values, color=PALETTE[:len(labels)])
        self.ax.tick_params(axis='x', rotation=15)
        # Fixed margins — avoid tight_layout for predictable centering
        self.fig.subplots_adjust(left=0.10, right=0.97, top=0.92, bottom=0.25)
        self.draw()

    def plot_pie(self, labels, values):
        self.ax.clear()
        self.ax.pie(
            values, labels=labels,
            colors=PALETTE[:len(labels)],
            autopct='%1.1f%%',
            textprops={'color': 'white'}
        )
        # Fixed margins — avoid tight_layout for predictable centering
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        self.draw()

    def plot_column(self, labels, values):
        self.ax.clear()
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        self.ax.set_ylabel('ms', color='white', fontsize=9)

        # Cleaner look: hide top/right spines, color the rest
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        for spine in ('left', 'bottom'):
            self.ax.spines[spine].set_edgecolor('#555555')

        wrapped = [wrap_label(l) for l in labels]
        colors = PALETTE[:len(labels)]

        bars = self.ax.bar(wrapped, values, width=0.5, color=colors)

        # Value labels on top of each bar so the y-axis is secondary
        self.ax.bar_label(bars, fmt='%.1f', color='white', padding=3, fontsize=8)

        # Symmetric padding centers the bars in the axes
        self.ax.set_xlim(-0.7, len(labels) - 0.3)
        self.ax.tick_params(axis='x', rotation=0, colors='white', labelsize=9)

        # Fixed margins — no tight_layout so positioning is stable across renders
        self.fig.subplots_adjust(left=0.12, right=0.97, top=0.92, bottom=0.25)
        self.draw()


class WidgetSetup(QtWidgets.QWidget, Ui_Widget):
    targetdir = None
    startFrame = None
    endFrame = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # widgets are now direct attributes, no findChild needed

        self.chartView.setStyleSheet("background: #2b2b2b;")

        self.bar_evaluationProgress.setVisible(False)
        # Timer for progress bar animation
        self.stripe_offset = 0
        self.stripe_timer = QtCore.QTimer()
        self.stripe_timer.timeout.connect(self.animate_stripes)
        self.stripe_timer.setInterval(30)
        self.bar_evaluationProgress.setFormat("%p%")
        self.bar_evaluationProgress.setAlignment(QtCore.Qt.AlignCenter)
        self.bar_evaluationProgress.setStyleSheet("""
            QProgressBar {
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk { ... }
        """)

        # Chart setup
        chart_layout = QtWidgets.QVBoxLayout(self.chartView)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(0)

        # Switch buttons row
        switch_layout = QtWidgets.QHBoxLayout()
        switch_layout.addStretch()

        self.btn_overview = QtWidgets.QPushButton("Overview")
        self.btn_detail = QtWidgets.QPushButton("Detail")
        self.btn_overview.setCheckable(True)
        self.btn_detail.setCheckable(True)
        self.btn_overview.setChecked(True)

        btn_group = QtWidgets.QButtonGroup(self)
        btn_group.addButton(self.btn_overview)
        btn_group.addButton(self.btn_detail)

        switch_layout.addWidget(self.btn_overview)
        switch_layout.addWidget(self.btn_detail)
        chart_layout.addLayout(switch_layout)

        # Stack - for switching graphs
        self.stack = QtWidgets.QStackedWidget()
        self.stack.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        chart_layout.addWidget(self.stack)

        # Connect buttons
        self.btn_overview.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_detail.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # Page 0 - overview chart
        self.overview_chart = ChartCanvas()
        self.stack.addWidget(self.overview_chart)

        # Page 1 - drilldown chart
        self.detail_chart = ChartCanvas()
        self.stack.addWidget(self.detail_chart)

        self.stack.setCurrentIndex(0)

        # Folder buttons setup
        self.setup_folder_button(self.btn_folder)
        self.setup_folder_button(self.btn_folder_2)

        # Restore persisted state
        self.txt_folderPath.setPlainText(WidgetSetup.targetdir or "")

        # Setup cause label
        self.lbl_cause.setVisible(False)

        # Setup buttons
        self.btn_top1.setVisible(False)
        self.btn_top2.setVisible(False)
        self.btn_top3.setVisible(False)

        # Signals
        self.btn_folder.clicked.connect(self.select_folder_clicked)
        self.btn_folder_2.clicked.connect(self.select_files_clicked)
        self.btn_profiling.clicked.connect(self.profiling_clicked)
        self.btn_evaluate.clicked.connect(self.evaluate_clicked)

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker.isRunning():
            QtWidgets.QMessageBox.warning(
                self,
                "Evaluation in progress",
                "Please wait for the evaluation to finish before closing."
            )
            event.ignore()
        else:
            event.accept()

    def setup_folder_button(self, btn):
        pm_closed = QtGui.QPixmap(":/folder-closed.png").scaled(
            28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        pm_open = QtGui.QPixmap(":/folder-open.png").scaled(
            28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        btn.setIcon(QtGui.QIcon(pm_closed))
        btn.setIconSize(QtCore.QSize(28, 28))
        btn.setStyleSheet("QPushButton { border: none; }")
        btn.enterEvent = lambda e: btn.setIcon(QtGui.QIcon(pm_open))
        btn.leaveEvent = lambda e: btn.setIcon(QtGui.QIcon(pm_closed))

    def select_folder_clicked(self):
        folder = choose_directory()
        if folder:
            WidgetSetup.targetdir = folder
            self.txt_folderPath.setPlainText(folder)

    def profiling_clicked(self):
        # Get start and end frame from lineedit
        startFrame = self.txt_startFrame.text()
        endFrame = self.txt_endFrame.text()

        # Get the name of file to name txt files
        output_name = get_default_filename()

        # Start recording function
        profiler_recording.recordFrames(
            int(startFrame), int(endFrame),
            WidgetSetup.targetdir, output_name
        )

    def select_files_clicked(self):
        self.list_selectedFiles.clear()
        files = getRecordedData()
        for file in files:
            self.list_selectedFiles.addItem(file)

    def evaluate_clicked(self):
        top_n = 3
        files = [self.list_selectedFiles.item(i).text()
                 for i in range(self.list_selectedFiles.count())]

        self.bar_evaluationProgress.setVisible(True)
        self.stripe_timer.start()
        self.bar_evaluationProgress.setValue(0)
        self.btn_evaluate.setEnabled(False)  # prevent double-click while running

        self.worker = EvaluateWorker(files, top_n)
        self.worker.progress.connect(self.bar_evaluationProgress.setValue)
        self.worker.finished.connect(self.on_evaluate_finished)
        self.worker.start()

    def on_evaluate_finished(self, result):
        list_of_events, bound_type, eval_time, render_time = result

        self.bar_evaluationProgress.setVisible(False)
        self.btn_evaluate.setEnabled(True)

        event_names, durations = zip(*[(d['event_name'], d['median_duration']) for d in list_of_events])

        self.detail_chart.plot_column(event_names, durations)
        self.overview_chart.plot_pie(
            ['Evaluation', 'Render'],
            [eval_time, render_time]
        )

        # UI changes based on result
        self.lbl_cause.setVisible(True)
        if bound_type == "EB":
            self.lbl_cause.setText("Your scene takes long to: Evaluate")
            select_btn_setup(self.btn_top1, event_names[0])
            select_btn_setup(self.btn_top2, event_names[1])
            select_btn_setup(self.btn_top3, event_names[2])
        else:
            self.lbl_cause.setText("Your scene takes long to: Render")

        self.stripe_timer.stop()
        self.bar_evaluationProgress.setVisible(False)

    def animate_stripes(self):
        self.stripe_offset = (self.stripe_offset + 2) % 20
        o = self.stripe_offset
        self.bar_evaluationProgress.setStyleSheet(f"""
                QProgressBar {{
                    color: white;
                    font-weight: bold;
                }}
    
              QProgressBar::chunk {{
                  background: qlineargradient(
                      spread:repeat, x1:{o / 100}, y1:0, x2:{(o + 20) / 100}, y2:0,
                      stop:0 #378ADD,
                      stop:0.5 #2a6fba,
                      stop:1 #378ADD
                  );
              }}
          """)


def select_btn_setup(btn, event):
    result = cmds.ls(event)
    print(f"Node: '{event}' | cmds.ls: {result}")
    btn.setVisible(True)
    try:
        btn.clicked.disconnect()
    except RuntimeError:
        pass
    valid = bool(cmds.ls(event))
    if valid:
        btn.setEnabled(True)
        btn.clicked.connect(lambda: open_in_nodeeditor(event))
        btn.setText(event)
    else:
        btn.setEnabled(False)
        btn.setText("Not a selectable node")


def open_in_nodeeditor(event):
    # Select node
    cmds.select(event)
    # Open Node Editor and graph selection
    if not cmds.window("nodeEditorPanel1", exists=True):
        cmds.NodeEditorWindow()
    else:
        cmds.showWindow("nodeEditorPanel1")
    # Focus on selection
    selected = cmds.ls(sl=True)
    if selected:
        # Clear current view
        cmds.nodeEditor('nodeEditorPanel1NodeEditorEd', edit=True, rootNode='')
        cmds.nodeEditor('nodeEditorPanel1NodeEditorEd', edit=True, removeUnselected=True)

        # Add selected node and graph upstream and downstream connections
        cmds.nodeEditor('nodeEditorPanel1NodeEditorEd', edit=True,
                        rootNode=selected,
                        upstream=True,
                        downstream=True,
                        traversalDepthLimit=3)
        cmds.nodeEditor('nodeEditorPanel1NodeEditorEd', edit=True, frameAll=True)


def choose_directory():
    result = cmds.fileDialog2(fileMode=3, caption="Select output folder")
    return result[0] if result else None


def get_default_filename():
    name = Path(cmds.file(q=True, sn=True, shn=True)).stem
    return name or "untitled_scene"


def getRecordedData():
    results = cmds.fileDialog2(fileMode=4, caption="Select recorded frames to evaluate")
    print(results)
    return results if results else None


def wrap_label(label, max_len=14):

    if len(label) <= max_len:
        return label
    mid = len(label) // 2
    candidates = [m.start() for m in re.finditer(r'[:|]', label)]
    if candidates:
        split = min(candidates, key=lambda i: abs(i - mid))
        return label[:split + 1] + '\n' + label[split + 1:]
    return label[:mid] + '\n' + label[mid:]


def openWindow():
    if QtWidgets.QApplication.instance():
        for win in QtWidgets.QApplication.allWidgets():
            if 'ProfilerAssistant' in win.objectName():
                win.close()
                win.deleteLater()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)

    WidgetSetup.window = WidgetSetup(parent=mayaMainWindow)
    WidgetSetup.window.setObjectName('ProfilerAssistant')
    WidgetSetup.window.setWindowTitle('Profiler Assistant')
    WidgetSetup.window.setWindowFlags(QtCore.Qt.Window)
    WidgetSetup.window.setFixedSize(804, 814)
    WidgetSetup.window.show()
    WidgetSetup.window.raise_()