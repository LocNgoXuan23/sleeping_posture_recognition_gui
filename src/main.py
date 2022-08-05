from shelve import Shelf
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel
from PyQt5.uic import loadUi
from engine import registerUser, loginUser, addPatientData, showCamera
from utils import readJson, writeJson, readJsonByRole, updateJsonByKey

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("loginPage.ui", self)
        self.openRegisterBtn.clicked.connect(self.goToRegister)
        self.loginBtn.clicked.connect(self.loginFunction)

    def goToRegister(self):
        register = Register()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginFunction(self):
        state, payload = loginUser(self.emailInput.text(), self.passwordInput.text())

        if state == 1:
            ROLE = payload[0]
            NAME = payload[1]
            if ROLE == 'doctor':
                doctorHome = DoctorHome(ROLE, NAME)
                widget.addWidget(doctorHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            elif ROLE == 'patient':
                patientHome = PatientHome(ROLE, NAME)
                widget.addWidget(patientHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            elif ROLE == 'nurse':
                nurseHome = NurseHome(ROLE, NAME)
                widget.addWidget(nurseHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)

        elif state == -1:
            self.alertLabel.setText("Vui Lòng nhập đầy đủ thông tin")
            self.alertLabel.setStyleSheet("color: Red")

        elif state == -2:
            self.alertLabel.setText("Email không tồn tại, vui lòng nhập lại")
            self.alertLabel.setStyleSheet("color: Red")

        elif state == -3:
            self.alertLabel.setText("Sai password, Vui lòng nhập lại")
            self.alertLabel.setStyleSheet("color: Red")

class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("registerPage.ui", self)
        self.openLoginBtn.clicked.connect(self.goToLogin)
        self.registerBtn.clicked.connect(self.registerFunction)
    
    def goToLogin(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def registerFunction(self):
        state = registerUser(self.nameInput.text(), self.emailInput.text(), self.passwordInput.text())

        if state == 1:
            self.nameInput.setText("")
            self.emailInput.setText("")
            self.passwordInput.setText("")
            self.alertLabel.setText("")
            self.goToLogin()
        
        elif state == -1:
            self.alertLabel.setText("Tài khoản đã tồn tại")
            self.alertLabel.setStyleSheet("color: Red")
        
        elif state == -2:
            self.alertLabel.setText("Vui lòng nhập đầy đủ thông tin")
            self.alertLabel.setStyleSheet("color: Red")

class DoctorHome(QDialog):
    def __init__(self, role, name):
        super(DoctorHome, self).__init__()
        loadUi("doctorHomePage.ui", self)
        self.role = role
        self.name = name
        self.currentPatient = {'name': '', 'cameraID': ''}
        # initial
        self.initComponent()
        self.patientTable.setColumnWidth(0, 150)
        self.patientTable.setColumnWidth(1, 150)
        self.patientTable.setColumnWidth(2, 150)
        self.loadDataPatientTable()
        self.nurseTable.setColumnWidth(0, 100)
        self.loadDataNurseTable()
        
        # event
        self.logoutBtn.clicked.connect(self.logoutFunction) 
        self.addPatientBtn.clicked.connect(self.gotoAddPatient)
        self.editPatienTableBtn.clicked.connect(self.editPatientFunction)
        self.patientTable.selectionModel().selectionChanged.connect(self.selectTableChanged)
        self.showCameraBtn.clicked.connect(self.showCameraFunction)

    def showCameraFunction(self):
        showCamera(self.currentPatient['cameraID'])

    def editPatientFunction(self):
        patients = readJson('patientData.json')
        for i, patient in enumerate(patients):
            key = self.patientTable.item(i, 0).text()
            value = self.patientTable.item(i, 1).text()
            if self.patientTable.item(i, 2).text() != 'Không có y tá' and self.patientTable.item(i, 2).text() != '':
                nurses = readJson('nurseData.json')
                nurseCol = self.patientTable.item(i, 2).text().split(',')
                value += '/'
                for i, nurseName in enumerate(nurseCol):
                    if nurseName in nurses:
                        value += f'{nurseName}'
                        if i != len(nurseCol) - 1: value += ','

                        if nurses[nurseName] == '':
                            updateJsonByKey(nurseName, key, 'nurseData.json')
                        else:
                            patientList = nurses[nurseName].split('/')
                            if key not in patientList:
                                updateJsonByKey(nurseName, f'{nurses[nurseName]}/{key}', 'nurseData.json')
                            
                    else:
                        self.alertLabel.setText("Chưa có tên nurse trong danh sách")
                        self.alertLabel.setStyleSheet("color: Red")

            patients[patient] = value
        
        self.updatePatientTable(patients)
        writeJson(patients, 'patientData.json')

    def selectTableChanged(self, selected):
        for ix in selected.indexes():
            name = self.patientTable.item(ix.row(), 0).text()
            cameraID = self.patientTable.item(ix.row(), 1).text()
            print(ix.row(), ix.column(), name, cameraID)
            self.currentPatient['name'] = name
            self.currentPatient['cameraID'] = cameraID

    def loadDataNurseTable(self):
        nurses = readJson('nurseData.json')
        self.updateNurseTable(nurses)

    def loadDataPatientTable(self):
        patients = readJson('patientData.json')
        self.updatePatientTable(patients)

    def updateNurseTable(self, nurses):
        row = 0
        self.nurseTable.setRowCount(len(nurses))
        for nurse in nurses:
            name = nurse
            self.nurseTable.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            row += 1

    def updatePatientTable(self, patients):
        row = 0
        self.patientTable.setRowCount(len(patients))
        for patient in patients:
            name = patients[patient].split("/")[0]
            self.patientTable.setItem(row, 0, QtWidgets.QTableWidgetItem(patient))
            self.patientTable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            
            nurses = 'Không có y tá'
            if "/" in patients[patient]:
                nurses = patients[patient].split("/")[1]
            self.patientTable.setItem(row, 2, QtWidgets.QTableWidgetItem(nurses))
            row += 1

    def initComponent(self):
        self.nameLabel.setText(f'NAME : {self.name}')
    
    def logoutFunction(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoAddPatient(self):
        addPatient = AddPatient(self.role, self.name)
        widget.addWidget(addPatient)
        widget.setCurrentIndex(widget.currentIndex()+1)

class PatientHome(QDialog):
    def __init__(self, role, name):
        super(PatientHome, self).__init__()
        loadUi("patientHomePage.ui", self)
        self.role = role
        self.name = name
        self.initComponent()
        self.logoutBtn.clicked.connect(self.logoutFunction)

    def initComponent(self):
        self.nameLabel.setText(f'NAME : {self.name}')

    def logoutFunction(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class NurseHome(QDialog):
    def __init__(self, role, name):
        super(NurseHome, self).__init__()
        loadUi("nurseHomePage.ui", self)
        self.role = role
        self.name = name
        self.currentPatient = {'name': '', 'cameraID': ''}
        
        # Init component
        self.initComponent()
        self.patientTable.setColumnWidth(0, 150)
        self.patientTable.setColumnWidth(1, 150)
        self.loadDatapatientTable()

        # Event
        self.logoutBtn.clicked.connect(self.logoutFunction)
        self.patientTable.selectionModel().selectionChanged.connect(self.selectTableChanged)
        self.showCameraBtn.clicked.connect(self.showCameraFunction)

    def showCameraFunction(self):
        showCamera(self.currentPatient['cameraID'])

    def selectTableChanged(self, selected):
        for ix in selected.indexes():
            name = self.patientTable.item(ix.row(), 0).text()
            cameraID = self.patientTable.item(ix.row(), 1).text()
            print(ix.row(), ix.column(), name, cameraID)
            self.currentPatient['name'] = name
            self.currentPatient['cameraID'] = cameraID

    def loadDatapatientTable(self):
        patients = readJson('patientData.json')
        nurses = readJson('nurseData.json')
        if len(nurses) != 0:
            selectedPatients = nurses[self.name].split("/")
            self.updatepatientTable(patients, selectedPatients)

    def updatepatientTable(self, patients, selectedPatients):
        row = 0
        self.patientTable.setRowCount(len(selectedPatients))
        for patient in patients:
            if patient in selectedPatients:
                name = patients[patient].split("/")[0]
                self.patientTable.setItem(row, 0, QtWidgets.QTableWidgetItem(patient))
                self.patientTable.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                row += 1

    def initComponent(self):
        self.nameLabel.setText(f'NAME : {self.name}')

    def logoutFunction(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AddPatient(QDialog):
    def __init__(self, role, name):
        super(AddPatient, self).__init__()
        loadUi("addPatientPage.ui", self)
        self.role = role
        self.name = name

        self.addBtn.clicked.connect(self.addPatientFunction)
    
    def addPatientFunction(self):
        state = addPatientData(self.nameInput.text(), self.cameraIDInput.text())

        if state == -1:
            self.alertLabel.setText("Vui lòng nhập đầy đủ thông tin")
            self.alertLabel.setStyleSheet("color: Red")
        
        if state == -2:
            self.alertLabel.setText("Đã có tên bệnh nhân trong danh sách")
            self.alertLabel.setStyleSheet("color: Red")
        
        if state == 1:
            self.nameInput.setText("")
            self.cameraIDInput.setText("")
            self.gotoDoctorHome()
            

    def gotoDoctorHome(self):
        doctorHome = DoctorHome(self.role, self.name)
        widget.addWidget(doctorHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ShowPatientCamera(QDialog):
    def __init__(self, patientName, cameraID, role, name):
        super(ShowPatientCamera, self).__init__()
        loadUi("patientCamera.ui", self)
        self.patientName = patientName
        self.cameraID = cameraID
        self.role = role
        self.name = name

        # initial
        self.initComponent()

        # event
        self.backHomeBtn.clicked.connect(self.gotoDoctorHome)

    def gotoDoctorHome(self):
        doctorHome = DoctorHome(self.role, self.name)
        widget.addWidget(doctorHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.nameLabel.setText(f'Camera of patient : {self.patientName}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    login = Login()
    widget.addWidget(login)
    widget.setFixedHeight(612)
    widget.setFixedWidth(870)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exit !!!")
   

    


