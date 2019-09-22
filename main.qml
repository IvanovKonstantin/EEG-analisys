import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.2
import QtQuick.Controls.Material 2.3
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.3
import Qt.labs.platform 1.0 as Platform
import EEGRender 1.0
import Container 1.0
import SignalLabelsRender 1.0
import AxesRender 1.0


ApplicationWindow {
    visible: true
    width: 1600
    height: 900
    visibility: Window.Maximized

    Material.theme: Material.Dark
    Material.accent: Material.Purple

    onHeightChanged: eegRender.changeVisibleParametres()
    onWidthChanged: {
        eegRender.changeVisibleParametres()
    }

    /// ACTIONS

    Action {
        id: openAction
        text: qsTr("Открыть")
        onTriggered: fileDialog.open()
    }


    menuBar: MenuBar {
        Menu {
            title: qsTr("Файл")
            MenuItem {action: openAction}
        }
        Menu {
            title: qsTr("Амплитуда")

            ActionGroup {
                id: amlGroup
            }

            Action {
                text: qsTr("1 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(1)
            }

            Action {
                text: qsTr("3 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(3)
            }

            Action {
                text: qsTr("5 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(5)
            }

            Action {
                text: qsTr("7 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(7)
            }

            Action {
                text: qsTr("10 мкВ на мм")
                checkable: true
                checked: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(10)
            }

            Action {
                text: qsTr("15 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(15)
            }

            Action {
                text: qsTr("20 мкВ на мм")
                checkable: true
                ActionGroup.group: amlGroup
                onTriggered: eegRender.setAmplitude(20)
            }

        }
        Menu {
            title: qsTr("Помощь")
            Action {
                text: qsTr("Test container")
                onTriggered: eegRender.setContainer(containerGenerator.getContainer)
            }
        }
    }

    Image {
        id: image
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: 1031
        height: 745
        source: "icons/logo1.png"
    }

    ToolBar {
        id: toolBar
        anchors.left: parent.left
        anchors.right: parent.right

        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: openButton1
                Layout.preferredHeight: parent.height
                Layout.preferredWidth: parent.height * 1.22

                onClicked: fileDialog.open()

                Image {
                    source: "icons/open.png"
                    anchors.fill: parent
                    anchors.margins: 5
                }
            }

            Slider {
                id: eegSlider
                Layout.fillWidth: true
                onMoved: eegRender.shiftSignal(eegSlider.value)
            }
        }
    }

    RowLayout {
        anchors.top: toolBar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        SignalLabelsRender {
            id: signalLabelsReander
            Layout.fillHeight: true
            Layout.minimumWidth: 100
            Layout.preferredWidth: 100
            Layout.topMargin: 1
            Layout.bottomMargin: 1

            onWidgetTextChanged: {
                Layout.preferredWidth = widgetWidth
                Layout.minimumWidth = widgetWidth
            }
        }

        AxesRender {
            id: axesRender
            anchors.left: eegRender.left
            anchors.right: eegRender.right
            anchors.top: eegRender.top
            anchors.bottom: eegRender.bottom
        }

        EEGRender {
            id: eegRender
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.column: 1
            Layout.topMargin: 1
            Layout.bottomMargin: 1
            Layout.rightMargin: 1
            
            pixelDensity: Screen.pixelDensity
            onValidShiftChanged: {
                eegSlider.to = valShift
            }
        }

    }

    Connections {
        target: controller
        onEegSignalsChanged: {
            signalLabelsReander.setContainer(currContainer)
            eegRender.setContainer(currContainer)
            axesRender.setContainer(currContainer)
        }
    }



    /// DIALOGS

    FileDialog {
        id: fileDialog
        nameFilters: "*.edf"
        folder: "file:///D:/python-projects/eeg-analisys/edf-files/"
        onAccepted: {
            controller.loadSignalsFromEdf(this.fileUrl)
            eegSlider.value = 0
            image.visible = false
            //abductNameRect.fillNames('hello')
        }
    }
}
