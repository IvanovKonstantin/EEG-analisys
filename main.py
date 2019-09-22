from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
# import numpy as np
from eeg_render import EEGRender
from controller import Controller, Container
from signal_labels_render import SignalLabelsRender
from axes_render import AxesRender


if __name__ == "__main__":
    import sys
    sys_argv = sys.argv
    sys_argv += ['--style', 'Material']

    app = QGuiApplication(sys_argv)

    qmlRegisterType(EEGRender, 'EEGRender', 1, 0, 'EEGRender')
    qmlRegisterType(Container, 'Container', 1, 0, 'Container')
    qmlRegisterType(SignalLabelsRender, 'SignalLabelsRender', 1, 0, 'SignalLabelsRender')
    qmlRegisterType(AxesRender, 'AxesRender', 1, 0, 'AxesRender')

    app.setWindowIcon(QIcon("icons/app_icon.png"))
    # создаем движок для взаимодействия с QML
    engine = QQmlApplicationEngine()

    controller = Controller()
    engine.rootContext().setContextProperty("controller", controller)

    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
