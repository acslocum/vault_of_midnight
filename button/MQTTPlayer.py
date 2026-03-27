import configparser
import paho.mqtt.client as mqtt
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    pyqtProperty
)

from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QLineEdit,
    QVBoxLayout
)

class MqttPublisher(QObject):
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = pyqtSignal()
    disconnected = pyqtSignal()

    stateChanged = pyqtSignal(int)
    hostnameChanged = pyqtSignal(str)
    portChanged = pyqtSignal(int)
    keepAliveChanged = pyqtSignal(int)
    cleanSessionChanged = pyqtSignal(bool)
    protocolVersionChanged = pyqtSignal(int)

    messageSignal = pyqtSignal(str)

    def __init__(self, config : configparser.ConfigParser, parent=None):
        super().__init__(parent)

        self.config = config
        self.section = 'mqtt_pub'
        self.m_hostname = self.config.get(self.section, 'host')
        self.m_port = int(self.config.get(self.section, 'port')) #1883
        self.topic = self.config.get(self.section, 'topic')
        self.randomKeyword = config.get('general', 'random')
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttPublisher.MQTT_3_1
        self.m_state = MqttPublisher.Disconnected
        self.m_client =  mqtt.Client(clean_session=self.m_cleanSession,
            protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_publish = self.on_publish
        self.m_client.on_disconnect = self.on_disconnect

    @pyqtSlot(str)
    def triggered(self, filename : str):
        if len(filename) > 0 and filename != self.randomKeyword:
            print(f'Playing: {filename}')
        else:
            filename = self.randomKeyword
            print(f'Sending random request: {filename}')
        result = self.m_client.publish(self.topic, filename)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish message: {mqtt.error_string(result.rc)}")

    @pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state: return
        self.m_state = state
        self.stateChanged.emit(state) 

    @pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname: return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port: return
        self.m_port = port
        self.portChanged.emit(port)

    @pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive: return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession: return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion: return
        if protocolVersion in (MqttPublisher.MQTT_3_1, MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    @pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname, 
                port=self.port, 
                keepalive=self.keepAlive)

            self.state = MqttPublisher.Connecting
            self.m_client.loop_start()

    @pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttPublisher.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_publish(self, client, userdata, mid, reason_code=None, properties=None):
        print(f"Message {mid} published successfully.")

    def on_connect(self, *args):
        #print("on_connect", args)
        self.state = MqttPublisher.Connected
        self.connected.emit()
        self.m_client.subscribe(self.topic)

    def on_disconnect(self, *args):
        # print("on_disconnect", args)
        self.state = MqttPublisher.Disconnected
        self.disconnected.emit()

if __name__ == '__main__':
    import sys

    def read_configuration():
        config_ini = configparser.ConfigParser(allow_unnamed_section=True)
        config_ini.read("config.ini")
        return config_ini

    class Widget(QWidget):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)

            lay = QVBoxLayout(self)
            self.le = QLineEdit()
            lay.addWidget(self.le)

            cfg = read_configuration()
            self.client = MqttClient(cfg, self)
            self.client.stateChanged.connect(self.on_stateChanged)
            self.client.messageSignal.connect(self.on_messageSignal)

            self.client.connectToHost()

        @pyqtSlot(int)
        def on_stateChanged(self, state):
            if state == MqttClient.Connected:
                print(state)
                self.client.subscribe(self.client.topic)

        @pyqtSlot(str)
        def on_messageSignal(self, msg):
            try:
                self.le.setText(msg)
            except Exception as e:
                print(f"error: {e}")

    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())
