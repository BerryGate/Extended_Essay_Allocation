"""
This is the newest version of the software, replacing V1.0.
This enhances the optimization algorithms and makes several slight improvements based on V2.0

Created by Benji Xu.
Finished on 14th July 2023, in Beijing.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt  # DO NOT DELETE THIS. THIS IS USED.
import pandas as pd
import sys

student_info = {}  # Key = student name. Value = [1st choice, 2nd choice, 3rd choice]. Allocated choice is appended to the list.
student_info_copy = {}  # Copy initial student info to allow multiple allocations
capacity = {}  # Key = subject. Value = [capacity, number of already allocated choices]
unlucky_students = {}  # Similar to student_info.
displayed_subjects_num = 0
import_success, allocate_success = False, False
# Ensure that the window and widgets do not change size based on the machine they are on.
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class Ui_MainWindow(object):
    """
    Overall architecture:

    1. Initialization
    Includes the function setupUi

    2. Creating widgets
    Includes functions: create_button, create_subject_labels, create_spin_box, create_allocation_result_labels, create_bars, create_other_labels
    These create widgets, but don't necessarily show them. They are called from within setupUi

    3. Process data
    Includes the 6 functions under the Process Data label.
    The first 5 are called from within main_process_data, which is called from interactions() when the import button is clicked.
    These are for converting dataframes into other data structures, cleaning data, etc

    4. Allocation
    Includes the 12 functions under the Allocation label.
    The first 11 are called from within main_allocate, which is called from interactions() when the allocate button is clicked.
    These are for allocating students by modifying the student_info dictionary.

    5. Output
    Includes the 3 functions under the Output label.
    The first 2 are called from within main_output, which is called from interactions() when the output button is clicked.
    These are for outputting the result as an Excel or csv.

    6. Interactions
    Includes the interactions() function, which connects the buttons with other functions.
    """

    '''
    Initialization
    '''
    def setupUi(self, MainWindow):
        # Initialization
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1387, 790)
        MainWindow.setMinimumSize(QtCore.QSize(1387, 790))
        MainWindow.setMaximumSize(QtCore.QSize(1387, 790))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background-color: rgb(250, 250, 240);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Creating visible widgets
        self.create_buttons()
        self.create_subject_labels()
        self.create_spin_box()
        self.create_allocation_result_labels()
        self.create_bars()
        self.create_other_labels()  # Need to call this last so the error label overwrites the other labels

        # Handle other tasks
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1387, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "Extended Essay Allocation"))
        self.interactions()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    '''
    Creating widgets: 
    '''
    def create_buttons(self):
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setUnderline(False)

        # Import Student Info Button
        self.importButton = QtWidgets.QPushButton(self.centralwidget)
        self.importButton.setGeometry(QtCore.QRect(60, 60, 241, 71))
        self.importButton.setFont(font)
        self.importButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.importButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.importButton.setAutoFillBackground(False)
        self.importButton.setStyleSheet("background-color: rgba(10, 140, 75, 1);\n"
                                        "color: rgba(255, 255, 255, 1);\n"
                                        "border-color: rgba(255, 255, 255, 1);\n"
                                        "border-style:solid;\n"
                                        "border-width:5px;\n"
                                        "border-radius:25px;")
        self.importButton.setIconSize(QtCore.QSize(16, 16))
        self.importButton.setAutoRepeat(False)
        self.importButton.setObjectName("importButton")
        self.importButton.setFont(QtGui.QFont('Artifakt Element', 17))
        self.importButton.setText("Import Student Choices")

        # Allocate Button
        self.allocateButton = QtWidgets.QPushButton(self.centralwidget)
        self.allocateButton.setGeometry(QtCore.QRect(60, 350, 241, 71))
        self.allocateButton.setFont(font)
        self.allocateButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.allocateButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.allocateButton.setAutoFillBackground(False)
        self.allocateButton.setStyleSheet("background-color: rgba(10, 140, 75, 1);\n"
                                        "color: rgba(255, 255, 255, 1);\n"
                                        "border-color: rgba(255, 255, 255, 1);\n"
                                        "border-style:solid;\n"
                                        "border-width:5px;\n"
                                        "border-radius:25px;")
        self.allocateButton.setIconSize(QtCore.QSize(16, 16))
        self.allocateButton.setAutoRepeat(False)
        self.allocateButton.setObjectName("allocateButton")
        self.allocateButton.setFont(QtGui.QFont('Artifakt Element', 17))
        self.allocateButton.setText("Allocate")

        # Output Button
        self.outputButton = QtWidgets.QPushButton(self.centralwidget)
        self.outputButton.setGeometry(QtCore.QRect(60, 630, 241, 71))
        self.outputButton.setFont(font)
        self.outputButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.outputButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.outputButton.setAutoFillBackground(False)
        self.outputButton.setStyleSheet("background-color: rgba(10, 140, 75, 1);\n"
                                        "color: rgba(255, 255, 255, 1);\n"
                                        "border-color: rgba(255, 255, 255, 1);\n"
                                        "border-style:solid;\n"
                                        "border-width:5px;\n"
                                        "border-radius:25px;")
        self.outputButton.setIconSize(QtCore.QSize(16, 16))
        self.outputButton.setAutoRepeat(False)
        self.outputButton.setObjectName("outputButton")
        self.outputButton.setFont(QtGui.QFont('Artifakt Element', 17))
        self.outputButton.setText("Output")

    # Hide subject labels by setting transparency (can also adjust position to hide)
    def create_subject_labels(self):
        font = QtGui.QFont()
        font.setFamily("Artifakt Element")
        font.setPointSize(16)

        for i in range(1, 50):  # Creating 50 labels, which is more than enough. Should be the same as the num of spinbox in function create_spin_box
            exec(f"self.subjectLabel{i} = QtWidgets.QLabel(self.centralwidget)")
            eval(f"self.subjectLabel{i}.setGeometry(QtCore.QRect(430, 180, 140, 21))")  # Positions will be adjusted later
            eval(f"self.subjectLabel{i}.setFont(font)")
            eval(f"self.subjectLabel{i}.setFrameShape(QtWidgets.QFrame.NoFrame)")
            eval(f"self.subjectLabel{i}.setFrameShadow(QtWidgets.QFrame.Raised)")
            eval(f'self.subjectLabel{i}.setStyleSheet("color: rgba(0, 0, 0, 0);")')  # Set transparency as 0. Hide labels
            eval(f'self.subjectLabel{i}.setStyleSheet("background-color: rgba(0, 0, 0, 0);")')
            eval(f'self.subjectLabel{i}.setObjectName("subjectLabel{i}")')
            eval(f'self.subjectLabel{i}.setAlignment(Qt.AlignTop)')

    # # Hide spin boxes by adjusting position
    def create_spin_box(self):
        font = QtGui.QFont()
        font.setFamily("Artifakt Element")
        font.setPointSize(15)

        for i in range(1, 50):  # Should be the same number as the num of subject labels in the function create_subject_labels
            exec(f"self.spinBox{i} = QtWidgets.QSpinBox(self.centralwidget)")
            # Set spinbox out of screen so it's not initially visible. Use position instead of transparency to hide spinbox because it's hard to hide a spinbox using transparency.
            eval(f"self.spinBox{i}.setGeometry(QtCore.QRect(2000, 680, 48, 24))")
            eval(f'self.spinBox{i}.setStyleSheet("color: rgba(0, 143, 53, 1);")')
            eval(f'self.spinBox{i}.setObjectName("spinBox{i}")')
            eval(f'self.spinBox{i}.setFont(font)')

    # Hide labels at first by not giving them text. They should not have text because unsure of allocation result.
    def create_allocation_result_labels(self):
        # Allocation result label
        self.allocationResultLabel = QtWidgets.QLabel(self.centralwidget)
        self.allocationResultLabel.setGeometry(QtCore.QRect(1050, 271, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Artifakt Element")
        font.setPointSize(21)
        self.allocationResultLabel.setFont(font)
        self.allocationResultLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.allocationResultLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.allocationResultLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.allocationResultLabel.setObjectName("allocationResultLabel")
        # Hide label by not giving it text

        small_font = QtGui.QFont()
        small_font.setFamily("Artifakt Element")
        small_font.setPointSize(16)

        # First choice label
        self.firstChoiceLabel = QtWidgets.QLabel(self.centralwidget)
        self.firstChoiceLabel.setGeometry(QtCore.QRect(1000, 321, 200, 31))
        self.firstChoiceLabel.setFont(small_font)
        self.firstChoiceLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.firstChoiceLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.firstChoiceLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.firstChoiceLabel.setObjectName("firstChoiceLabel")

        # Second choice label
        self.secondChoiceLabel = QtWidgets.QLabel(self.centralwidget)
        self.secondChoiceLabel.setGeometry(QtCore.QRect(1000, 371, 200, 31))
        self.secondChoiceLabel.setFont(small_font)
        self.secondChoiceLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.secondChoiceLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.secondChoiceLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.secondChoiceLabel.setObjectName("secondChoiceLabel")

        # Third choice label
        self.thirdChoiceLabel = QtWidgets.QLabel(self.centralwidget)
        self.thirdChoiceLabel.setGeometry(QtCore.QRect(1000, 421, 200, 31))
        self.thirdChoiceLabel.setFont(small_font)
        self.thirdChoiceLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.thirdChoiceLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.thirdChoiceLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.thirdChoiceLabel.setObjectName("thirdChoiceLabel")

        # Allocation summary label
        self.allocationSummaryLabel = QtWidgets.QLabel(self.centralwidget)
        self.allocationSummaryLabel.setGeometry(QtCore.QRect(950, 471, 365, 31))
        self.allocationSummaryLabel.setFont(small_font)
        self.allocationSummaryLabel.setStyleSheet("color: rgba(0, 143, 53, 1);")
        self.allocationSummaryLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.allocationSummaryLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.allocationSummaryLabel.setObjectName("allocationSummaryLabel")

        # Unallocated student label
        self.unallocatedStudentLabel = QtWidgets.QLabel(self.centralwidget)
        self.unallocatedStudentLabel.setGeometry(QtCore.QRect(950, 471, 361, 31))
        self.unallocatedStudentLabel.setFont(small_font)
        self.unallocatedStudentLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.unallocatedStudentLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.unallocatedStudentLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.unallocatedStudentLabel.setObjectName("unallocatedStudentLabel")

    # Hide bars at first by adjusting position
    def create_bars(self):
        # Left bar
        self.leftBar = QtWidgets.QFrame(self.centralwidget)
        self.leftBar.setGeometry(QtCore.QRect(9999, 260, 21, 258))  # Move out to hide bar at first
        self.leftBar.setStyleSheet("color: rgba(0, 143, 53, 1);\n"
                                   "background-color: rgba(255, 255, 255, 0);")
        self.leftBar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.leftBar.setLineWidth(4)
        self.leftBar.setFrameShape(QtWidgets.QFrame.VLine)
        self.leftBar.setObjectName("leftBar")

        # Right bar
        self.rightBar = QtWidgets.QFrame(self.centralwidget)
        self.rightBar.setGeometry(QtCore.QRect(9999, 260, 21, 258))
        self.rightBar.setStyleSheet("color: rgba(0, 143, 53, 1);\n"
                                    "background-color: rgba(255, 255, 255, 0);")
        self.rightBar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rightBar.setLineWidth(4)
        self.rightBar.setFrameShape(QtWidgets.QFrame.VLine)
        self.rightBar.setObjectName("rightBar")

        # Top bar
        self.topBar = QtWidgets.QFrame(self.centralwidget)
        self.topBar.setGeometry(QtCore.QRect(9999, 246, 402, 31))
        self.topBar.setStyleSheet("color: rgba(0, 143, 53, 1);\n"
                                  "background-color: rgba(0, 0, 0, 0)")
        self.topBar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.topBar.setLineWidth(4)
        self.topBar.setFrameShape(QtWidgets.QFrame.HLine)
        self.topBar.setObjectName("topBar")

        # Bottom bar
        self.bottomBar = QtWidgets.QFrame(self.centralwidget)
        self.bottomBar.setGeometry(QtCore.QRect(9999, 501, 400, 31))
        self.bottomBar.setStyleSheet("color: rgba(0, 143, 53, 1);\n"
                                     "background-color: rgba(0, 0, 0, 0)")
        self.bottomBar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bottomBar.setLineWidth(4)
        self.bottomBar.setFrameShape(QtWidgets.QFrame.HLine)
        self.bottomBar.setObjectName("bottomBar")

    # Hide labels at first by adjusting position
    def create_other_labels(self):
        font = QtGui.QFont()
        font.setFamily("Artifakt Element")
        font.setPointSize(18)

        # Import Successful Label
        self.importSuccLabel = QtWidgets.QLabel(self.centralwidget)
        self.importSuccLabel.setGeometry(QtCore.QRect(9999, 80, 185, 30))  # Move out to hide labels
        self.importSuccLabel.setFont(font)
        self.importSuccLabel.setStyleSheet("color: rgba(0, 143, 53, 1);")
        self.importSuccLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.importSuccLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.importSuccLabel.setObjectName("importSuccLabel")
        self.importSuccLabel.setText('Import Successful ✓')

        # Import Unsuccessful Label
        self.importUnsuccLabel = QtWidgets.QLabel(self.centralwidget)
        self.importUnsuccLabel.setGeometry(QtCore.QRect(9999, 80, 600, 30))
        self.importUnsuccLabel.setFont(font)
        self.importUnsuccLabel.setStyleSheet("color: rgba(200, 20, 20, 1);")
        self.importUnsuccLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.importUnsuccLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.importUnsuccLabel.setObjectName("importUnsuccLabel")
        self.importUnsuccLabel.setText('Spreadsheet format incorrect. Please check and try again.')

        # Enter subject capacity label
        self.enterCapLabel = QtWidgets.QLabel(self.centralwidget)
        self.enterCapLabel.setGeometry(QtCore.QRect(9999, 120, 250, 31))
        self.enterCapLabel.setFont(font)
        self.enterCapLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enterCapLabel.setStyleSheet("color: rgba(0, 0, 0, 1);")
        self.enterCapLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.enterCapLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.enterCapLabel.setObjectName("enterCapLabel")
        self.enterCapLabel.setText('Enter Subject Capacity:')

        # Import first label
        self.importFirstLabel = QtWidgets.QLabel(self.centralwidget)
        self.importFirstLabel.setGeometry(QtCore.QRect(9999, 435, 315, 30))
        self.importFirstLabel.setFont(font)
        self.importFirstLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.importFirstLabel.setStyleSheet("color: rgba(200, 20, 20, 1);")
        self.importFirstLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.importFirstLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.importFirstLabel.setObjectName("importFirstLabel")
        self.importFirstLabel.setText('Please import student choices first')

        # Allocate first label
        self.allocateFirstLabel = QtWidgets.QLabel(self.centralwidget)
        self.allocateFirstLabel.setGeometry(QtCore.QRect(9999, 715, 315, 30))
        self.allocateFirstLabel.setFont(font)
        self.allocateFirstLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.allocateFirstLabel.setStyleSheet("color: rgba(200, 20, 20, 1);")
        self.allocateFirstLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.allocateFirstLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.allocateFirstLabel.setObjectName("allocateFirstLabel")
        self.allocateFirstLabel.setText('Please allocate first')

        # notSpreadsheetLabel
        self.notSpreadsheetLabel = QtWidgets.QLabel(self.centralwidget)
        self.notSpreadsheetLabel.setGeometry(QtCore.QRect(9999, 350, 600, 80))
        self.notSpreadsheetLabel.setFont(font)
        self.notSpreadsheetLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.notSpreadsheetLabel.setStyleSheet("color: rgba(200, 20, 20, 1);")
        self.notSpreadsheetLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notSpreadsheetLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.notSpreadsheetLabel.setObjectName("notSpreadsheetLabel")
        self.notSpreadsheetLabel.setText(
            'Import format incorrect.\nPlease ensure you are importing a spreadsheet (xlxs or csv)')

        # Error label
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(9999, 350, 600, 80))
        self.errorLabel.setFont(font)
        self.errorLabel.setStyleSheet("color: rgba(200, 20, 20, 1);")
        self.errorLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.errorLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setText(
            'An error occurred. We apologize for the inconvenience.\nPlease contact the developer for help.')


    '''
    Process data
    '''
    def convert_data_type(self, df):
        # Convert df into dictionary for student choices

        names_reference = {
            'business': 'Business',
            'environment': 'ESS',
            'computer': 'ComSci',
            'self': 'SSSTL'
        }  # English is complex

        if df.shape[1] == 6:  # 6 columns: timestamp, name, 1st, 2nd, 3rd, email
            if df.columns[0] == 'Timestamp' and (df.columns[-1] == 'Email address' or df.columns[1] == 'Email address'):
                df.drop(['Email address'], axis=1, inplace=True)
            else:
                print('ERROR: Spreadsheet format not as expected')
                self.importUnsuccLabel.setGeometry(QtCore.QRect(370, 80, 600, 30))
                return False

        if df.shape[1] == 5 and df.columns[0] == 'Timestamp':  # 5 columns: timestamp, name, 1st, 2nd, 3rd
            for index, row in df.iterrows():

                for i in range(2, 5):  # Change subject names to shorter names
                    for keyword, short_name in names_reference.items():
                        if keyword in row[df.columns[i]].lower().strip():
                            row[df.columns[i]] = short_name
                            break

                if row[df.columns[1]] not in student_info.keys():
                    student_info[row[df.columns[1]]] = [row[df.columns[2]], row[df.columns[3]], row[df.columns[4]]]
                else:  # Exact same name
                    student_info[f'{row[df.columns[1]]}_2'] = [row[df.columns[2]], row[df.columns[3]], row[df.columns[4]]]  # SMALL ISSUE: THIS DOES NOT CONSIDER THE CASE WHEN THERE ARE 3 NAMES THAT RE EXACTLY THE SAME
        else:
            print('ERROR: Spreadsheet format not as expected')
            self.importUnsuccLabel.setGeometry(QtCore.QRect(370, 80, 600, 30))
            return False

        return True

    def check_choice_repetition(self):
        global student_info_copy
        for choices in student_info.values():
            if choices[0] == choices[1] and choices[0] == choices[2]:
                choices[1], choices[2] = 'VIOLATION', 'VIOLATION'
            elif choices[0] == choices[1]:
                choices[1] = 'VIOLATION'
            elif choices[0] == choices[2] or choices[1] == choices[2]:
                choices[2] = 'VIOLATION'
        capacity['VIOLATION'] = [0, 0]

        # Copy info
        for name, choices in student_info.items():
            student_info_copy[name] = choices.copy()

    def process_subjects(self):
        del_lis = []

        # Set up data structure of capacity based on subjects in student choices
        for choices in student_info.values():  # SMALL ISSUE: THIS FOR LOOP IS NOT INTEGRATED INTO THE CHECK CHOICE REPETITION FUNCTION BECAUSE THEY DO DIFFERENT THINGS. IDK IF THEY SHOULD BE INTEGRATED. BASICALLY, PRIORITIZE FUNCTION CATEGORIZATION OR SPEED?
            for choice in choices:
                if choice not in capacity.keys():
                    capacity[choice] = [0, 0]

        # Check for white space and capitalization - name variation of same subject
        for key in capacity.keys():
            if key in del_lis:
                continue
            for key_2 in capacity.keys():
                if key != key_2 and key.lower().strip() == key_2.lower().strip():
                    # Variations of the same subject exist
                    print(f"NOTE: Name variation of the same subject exists ({key} AND {key_2})")
                    del_lis.append(key_2)  # SMALL ISSUE: BY DIRECTLY DELETING KEY_2, I DO NOT KNOW WHICH KEY IS INCORRECTLY FORMATTED - I MIGHT BE DELETING THE CORRECTLY FORMATTED KEY. BUT CHECKING WHICH KEY (KEY OR KEY_2) IS CORRECTLY FORMATTED TAKES MORE TIME.
        for subject in del_lis:
            capacity.pop(subject)

    def show_subject_labels(self, subjects):
        global displayed_subjects_num
        # Move label to correct place. Set color.
        # Move spinbox to correct place.

        if len(subjects) > 34:  # 34 is the max number of subjects that can be displayed
            print('ERROR: Too many subjects to display!')
            self.errorLabel.setGeometry(QtCore.QRect(450, 350, 600, 80))
            return False

        margins = {}  # 1:[140, 57]    140 is y starting positionfirst subject of the . 57 is space between lines of subjects
        for i in range(1, 35):
            if i <= 22:
                margins[str(i)] = [140, 57]
            elif i == 23 or i == 24:
                margins[str(i)] = [140, 50]
            elif i == 25 or i == 26:
                margins[str(i)] = [110, 50]
            elif i == 27 or i == 28:
                margins[str(i)] = [110, 47]
            elif i == 29 or i == 30:
                margins[str(i)] = [110, 45]
            elif i == 31 or i == 32:
                margins[str(i)] = [110, 42]
            elif i == 33 or i == 34:
                margins[str(i)] = [110, 38]

        for i in range(1, len(subjects) + 1):

            # Change position of label and spinbox
            if i <= (len(subjects) // 2) + (len(subjects) % 2):
                eval(
                    f'self.subjectLabel{i}.setGeometry(QtCore.QRect(390, {margins[str(len(subjects))][0]} + (i - 1) * {margins[str(len(subjects))][1]}, 160, 39))')
                eval(
                    f"self.spinBox{i}.setGeometry(QtCore.QRect(550, {margins[str(len(subjects))][0]} + (i - 1) * {margins[str(len(subjects))][1]}, 48, 24))")
            else:
                eval(
                    f'self.subjectLabel{i}.setGeometry(QtCore.QRect(670, {margins[str(len(subjects))][0]} + (i - (len(subjects) // 2) - (len(subjects)) % 2 - 1) * {margins[str(len(subjects))][1]}, 160, 39))')
                eval(
                    f"self.spinBox{i}.setGeometry(QtCore.QRect(830, {margins[str(len(subjects))][0]} + (i - (len(subjects) // 2) - (len(subjects)) % 2 - 1) * {margins[str(len(subjects))][1]}, 48, 24))")

            # Set color
            if i % 2 == 1:
                eval(f'self.subjectLabel{i}.setStyleSheet("color: rgba(0, 143, 53, 1);")')
                eval(f'self.spinBox{i}.setStyleSheet("color: rgba(0, 143, 53, 1);")')
            elif i % 2 == 0:
                eval(f'self.subjectLabel{i}.setStyleSheet("color: rgba(0, 0, 0, 1);")')
                eval(f'self.spinBox{i}.setStyleSheet("color: rgba(0, 0, 0, 1);")')

            # Handle long names
            if len(subjects[i - 1]) > 16 and len(subjects[i - 1]) <= 28:  # Split into 2 lines
                subject_name = f'{subjects[i - 1][:16]}\n{subjects[i - 1][16:]}'
                eval(f'self.subjectLabel{i}.setText(subject_name)')
            elif len(subjects[i - 1]) > 28:  # Cannot fit into 2 lines, use ...
                subject_name = f'{subjects[i - 1][:16]}\n{subjects[i - 1][16:27]}...'
                eval(f'self.subjectLabel{i}.setText(subject_name)')
            else:
                eval(f'self.subjectLabel{i}.setText(subjects[{i - 1}])')

            # Reset spinbox value
            eval(f'self.spinBox{i}.setValue(0)')

        # Update variable. Used in hiding labels
        displayed_subjects_num = len(subjects)

        # Show other labels
        self.importSuccLabel.setGeometry(QtCore.QRect(90, 140, 185, 30))
        if len(subjects) > 24:  # If not many subjects, leave more space so it's more aesthetically pleasing.
            self.enterCapLabel.setGeometry(QtCore.QRect(530, 55, 220, 31))
        else:
            self.enterCapLabel.setGeometry(QtCore.QRect(530, 75, 220, 31))
        return True

    def hide_labels(self):
        self.importSuccLabel.setGeometry(QtCore.QRect(9999, 80, 185, 30))
        self.importUnsuccLabel.setGeometry(QtCore.QRect(9999, 80, 600, 30))
        self.errorLabel.setGeometry(QtCore.QRect(9999, 350, 600, 80))
        self.enterCapLabel.setGeometry(QtCore.QRect(9999, 120, 201, 31))
        self.importFirstLabel.setGeometry(QtCore.QRect(9999, 435, 315, 30))
        self.allocateFirstLabel.setGeometry(QtCore.QRect(9999, 715, 315, 30))
        self.notSpreadsheetLabel.setGeometry(QtCore.QRect(9999, 350, 600, 80))

        self.leftBar.setGeometry(QtCore.QRect(9999, 260, 21, 258))
        self.rightBar.setGeometry(QtCore.QRect(9999, 260, 21, 258))
        self.topBar.setGeometry(QtCore.QRect(9999, 246, 402, 31))
        self.bottomBar.setGeometry(QtCore.QRect(9999, 501, 400, 31))

        self.allocationResultLabel.setGeometry(QtCore.QRect(9999, 271, 191, 31))
        self.firstChoiceLabel.setGeometry(QtCore.QRect(9999, 321, 200, 31))
        self.secondChoiceLabel.setGeometry(QtCore.QRect(9999, 371, 200, 31))
        self.thirdChoiceLabel.setGeometry(QtCore.QRect(9999, 421, 200, 31))
        self.allocationSummaryLabel.setGeometry(QtCore.QRect(9999, 471, 365, 31))
        self.unallocatedStudentLabel.setGeometry(QtCore.QRect(9999, 471, 361, 31))

        for i in range(displayed_subjects_num):  # When first allocating, displayed_s_num = 0, won't run loop
            eval(f'self.subjectLabel{i + 1}.setGeometry(QtCore.QRect(9999, 0, 1, 1))')
            eval(f'self.spinBox{i + 1}.setGeometry(QtCore.QRect(9999, 0, 1, 1))')

    def main_process_data(self):
        global student_info, student_info_copy, unlucky_students, capacity, import_success, allocate_success
        import_is_spread = True

        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            if filename[-5:] == '.xlsx':
                df = pd.read_excel(filename)
            elif filename[-4:] == '.csv':
                df = pd.read_csv(filename)
            else:
                # Imported a file, but file is NOT spreadsheet
                import_is_spread = False
        else:
            # User cancels pop up window. Nothing gets imported
            return None

        # Hide labels when newly importing
        self.hide_labels()

        # Reset all variables
        student_info, student_info_copy, unlucky_students, capacity = {}, {}, {}, {}
        allocate_success = False

        if not import_is_spread:
            # This goes below the should_reset if statement, because we want to show label after hiding al labels.
            self.notSpreadsheetLabel.setGeometry(QtCore.QRect(450, 350, 600, 80))
            import_success = False
            return None

        if self.convert_data_type(df):
            self.check_choice_repetition()
            self.process_subjects()
            subjects = list(capacity.keys())
            if 'VIOLATION' in subjects:
                subjects.pop(subjects.index('VIOLATION'))
            import_success = self.show_subject_labels(subjects)
        else:
            import_success = False


    '''
    Allocation
    '''
    def process_capacity(self):
        global capacity, unlucky_students, student_info
        count = 1
        for subject, caps in capacity.items():
            if subject != 'VIOLATION':
                caps[0] = eval(f'self.spinBox{count}.value()')
                count += 1
            caps[1] = 0

        unlucky_students = {}
        for key, val in student_info_copy.items():
            # To allocate again, must retrieve original data from student_info_copy because student_info is modified
            student_info[key] = val.copy()

    def allocate_1st_choice(self):
        for name, choices in student_info.items():
            if choices[0] not in capacity.keys():  # Error check
                print("ERROR - Student's subject is recorded not in the capacity dictionary")
            if capacity[choices[0]][1] < capacity[choices[0]][0]:
                capacity[choices[0]][1] += 1
                choices.append(f'1st CHOICE - {choices[0]}')

    def allocate_2nd_choice(self):
        for name, choices in student_info.items():
            if len(choices) == 3:
                if capacity[choices[1]][1] < capacity[choices[1]][0]:  # If capacity of 2nd choice not full
                    capacity[choices[1]][1] += 1
                    choices.append(f'2nd CHOICE - {choices[1]}')
                else:
                    unlucky_students[name] = choices.copy()  # Using copy() is important. Otherwise lists are linked

    def first_optimize(self):
        del_list = []
        for unlucky_name, unlucky_choices in unlucky_students.items():
            swicthed = False  # Use this variable to break because codes below have nested loops
            for name_1, choices_1 in student_info.items():
                if swicthed:
                    break
                if '1st CHOICE' in choices_1[-1] and unlucky_choices[0] == choices_1[0]:
                    # Algo 1 (13 or 10 --> 12)
                    if capacity[choices_1[1]][0] > capacity[choices_1[1]][1]:
                        capacity[choices_1[1]][1] += 1
                        choices_1[-1] = f'2nd CHOICE - {choices_1[1]}'
                        student_info[unlucky_name].append(f'1st CHOICE - {unlucky_choices[0]}')
                        del_list.append(unlucky_name)
                        break
                elif '2nd CHOICE' in choices_1[-1] and unlucky_choices[1] == choices_1[1]:
                    # Algo 2 (123 or 120 --> 122)
                    for name_2, choices_2 in student_info.items():
                        if '1st CHOICE' in choices_2[-1] and choices_1[0] == choices_2[0] and capacity[choices_2[1]][0] > capacity[choices_2[1]][1]:  # No need name != name
                            capacity[choices_2[1]][1] += 1
                            choices_1[-1] = f'1st CHOICE - {choices_1[0]}'
                            choices_2[-1] = f'2nd CHOICE - {choices_2[1]}'
                            student_info[unlucky_name].append(f'2nd CHOICE - {unlucky_choices[1]}')
                            del_list.append(unlucky_name)
                            swicthed = True
                            break
        for student in del_list:
            unlucky_students.pop(student)

    def allocate_3rd_choice(self):
        del_list = []
        for name, choices in unlucky_students.items():
            if capacity[choices[2]][0] > capacity[choices[2]][1]:
                capacity[choices[2]][1] += 1
                del_list.append(name)
                student_info[name].append(f'3rd CHOICE - {choices[2]}')
        for student in del_list:
            unlucky_students.pop(student)

    def optimization_helper(self, increased_subject, choice_1, choice_1_num, choice_2, choice_2_num, unlucky_name, unlucky_choices, unlucky_num):
        capacity[increased_subject][1] += 1
        ref = ['1st CHOICE', '2nd CHOICE', '3rd CHOICE']
        choice_1[-1] = f'{ref[choice_1_num]} - {choice_1[choice_1_num]}'
        if choice_2 is not False:
            choice_2[-1] = f'{ref[choice_2_num]} - {choice_2[choice_2_num]}'
        student_info[unlucky_name].append(f'{ref[unlucky_num]} - {unlucky_choices[unlucky_num]}')
        return True

    def optimize_round_1(self, unlucky_name, unlucky_choices):
        for name_1, choices_1 in student_info.items():
            if '1st CHOICE' in choices_1[-1] and capacity[choices_1[1]][0] > capacity[choices_1[1]][1]:
                if choices_1[0] == unlucky_choices[1]:
                    # Algo 11 (10 --> 22)
                    return self.optimization_helper(choices_1[1], choices_1, 1, False, False, unlucky_name, unlucky_choices, 1)
                else:
                    for name_2, choices_2 in student_info.items():
                        if '1st CHOICE' in choices_2[-1] and choices_2[0] == unlucky_choices[0] and choices_1[0] == choices_2[1] and name_1 != name_2:
                            # Algo 3 (110 --> 122)
                            return self.optimization_helper(choices_1[1], choices_1, 1, choices_2, 1, unlucky_name, unlucky_choices, 0)

    def optimize_round_2(self, unlucky_name, unlucky_choices):
        for name_1, choices_1 in student_info.items():
            if '1st CHOICE' in choices_1[-1] and choices_1[0] == unlucky_choices[0]:
                if capacity[choices_1[2]][0] > capacity[choices_1[2]][1]:
                    # Algo 6 (10 --> 13)
                    return self.optimization_helper(choices_1[2], choices_1, 2, False, False, unlucky_name, unlucky_choices, 0)
                else:
                    for name_2, choices_2 in student_info.items():
                        if '2nd CHOICE' in choices_2[-1] and choices_1[1] == choices_2[1] and capacity[choices_2[2]][0] > capacity[choices_2[2]][1]:
                            # Algo 5 (120 --> 123)
                            return self.optimization_helper(choices_2[2], choices_2, 2, choices_1, 1, unlucky_name, unlucky_choices, 0)
            elif '2nd CHOICE' in choices_1[-1] and choices_1[1] == unlucky_choices[1] and capacity[choices_1[2]][0] > capacity[choices_1[2]][1]:
                # Algo 7 (20 --> 23)
                return self.optimization_helper(choices_1[2], choices_1, 2, False, False, unlucky_name, unlucky_choices, 1)

    def optimize_round_3(self, unlucky_name, unlucky_choices):
        for name_1, choices_1 in student_info.items():
            if '1st CHOICE' in choices_1[-1]:
                if choices_1[0] == unlucky_choices[1] and capacity[choices_1[2]][0] > capacity[choices_1[2]][1]:
                    # Algo 12 (10 --> 23)
                    return self.optimization_helper(choices_1[2], choices_1, 2, False, False, unlucky_name, unlucky_choices, 1)
                elif choices_1[0] == unlucky_choices[2] and capacity[choices_1[1]][0] > capacity[choices_1[1]][1]:
                    # Algo 13 (10 --> 23)
                    return self.optimization_helper(choices_1[1], choices_1, 1, False, False, unlucky_name, unlucky_choices, 2)
                else:
                    for name_2, choices_2 in student_info.items():
                        if '1st CHOICE' in choices_2[-1] and choices_1[0] == unlucky_choices[0] and name_1 != name_2:
                            if choices_1[1] == choices_2[0] and capacity[choices_2[2]][0] > capacity[choices_2[2]][1]:
                                # Algo 4 (110 --> 123)
                                return self.optimization_helper(choices_2[2], choices_2, 2, choices_1, 1, unlucky_name, unlucky_choices, 0)
                            elif choices_1[2] == choices_2[0] and capacity[choices_2[1]][0] > capacity[choices_2[1]][1]:
                                # Algo 8 (110 --> 123)
                                return self.optimization_helper(choices_2[1], choices_2, 1, choices_1, 2, unlucky_name, unlucky_choices, 0)

    def optimize_round_4(self, unlucky_name, unlucky_choices):
        for name_1, choices_1 in student_info.items():
            if '2nd CHOICE' in choices_1[-1] and capacity[choices_1[2]][0] > capacity[choices_1[2]][1]:
                if choices_1[1] == unlucky_choices[2]:
                    # Algo 15 (20 --> 33)
                    return self.optimization_helper(choices_1[2], choices_1, 2, False, False, unlucky_name, unlucky_choices, 2)
                else:
                    for name_2, choices_2 in student_info.items():
                        if '1st CHOICE' in choices_2[-1] and choices_2[0] == unlucky_choices[0] and choices_1[1] == choices_2[2]:
                            # Algo 10 (120 --> 133)
                            return self.optimization_helper(choices_1[2], choices_1, 2, choices_2, 2, unlucky_name, unlucky_choices, 0)

    def optimize_round_5(self, unlucky_name, unlucky_choices):
        for name_1, choices_1 in student_info.items():
            if '1st CHOICE' in choices_1[-1] and capacity[choices_1[2]][0] > capacity[choices_1[2]][1]:
                if choices_1[0] == unlucky_choices[2]:
                    # Algo 14 (10 --> 33)
                    return self.optimization_helper(choices_1[2], choices_1, 2, False, False, unlucky_name, unlucky_choices, 2)
                else:
                    for name_2, choices_2 in student_info.items():
                        if '1st CHOICE' in choices_2[-1] and choices_2[0] == unlucky_choices[0] and choices_1[0] == choices_2[2] and name_1 != name_2:
                            # Algo 9 (110 --> 133)
                            return self.optimization_helper(choices_1[2], choices_1, 2, choices_2, 2, unlucky_name, unlucky_choices, 0)

    def final_help_unlucky(self):
        global unlucky_students
        del_list = []
        for unlucky_name, unlucky_choices in unlucky_students.items():
            failed = False
            # Each round contains several optimizations of the same level of superiority.
            # The earlier a round occurs, it means it's preferred over other rounds.
            # Refer to algorithms ranking at the bottom.
            if not self.optimize_round_1(unlucky_name, unlucky_choices):
                if not self.optimize_round_2(unlucky_name, unlucky_choices):
                    if not self.optimize_round_3(unlucky_name, unlucky_choices):
                        if not self.optimize_round_4(unlucky_name, unlucky_choices):
                            if not self.optimize_round_5(unlucky_name, unlucky_choices):
                                failed = True
            if not failed:
                del_list.append(unlucky_name)
        for name in del_list:
            unlucky_students.pop(name)

    def summarize_results(self):
        record = {
            '1st': 0,
            '2nd': 0,
            '3rd': 0
        }
        for choices in student_info.values():
            if '1st' in choices[-1]:
                record['1st'] += 1
            elif '2nd' in choices[-1]:
                record['2nd'] += 1
            elif '3rd' in choices[-1]:
                record['3rd'] += 1

        _translate = QtCore.QCoreApplication.translate
        self.allocationResultLabel.setText(_translate("MainWindow", "Allocation Result:"))
        self.firstChoiceLabel.setText(_translate("MainWindow", f"1st Choice Receivers: {record['1st']}"))
        self.secondChoiceLabel.setText(_translate("MainWindow", f"2nd Choice Receivers: {record['2nd']}"))
        self.thirdChoiceLabel.setText(_translate("MainWindow", f"3rd Choice Receivers: {record['3rd']}"))

        self.allocationResultLabel.setGeometry(QtCore.QRect(1050, 271, 191, 31))
        self.firstChoiceLabel.setGeometry(QtCore.QRect(1000, 321, 200, 31))
        self.secondChoiceLabel.setGeometry(QtCore.QRect(1000, 371, 200, 31))
        self.thirdChoiceLabel.setGeometry(QtCore.QRect(1000, 421, 200, 31))
        self.allocationSummaryLabel.setGeometry(QtCore.QRect(950, 471, 365, 31))

        self.leftBar.setGeometry(QtCore.QRect(920, 260, 21, 258))
        self.rightBar.setGeometry(QtCore.QRect(1325, 260, 21, 258))
        self.topBar.setGeometry(QtCore.QRect(929, 246, 407, 31))
        self.bottomBar.setGeometry(QtCore.QRect(930, 501, 405, 31))

        if len(unlucky_students) == 0:
            self.allocationSummaryLabel.setText(_translate("MainWindow", f"Allocation Complete: {len(student_info)}/{len(student_info)} students allocated"))
            self.unallocatedStudentLabel.setGeometry(QtCore.QRect(9999, 471, 361, 31))
            self.allocationSummaryLabel.setStyleSheet("color: rgba(0, 143, 53, 1);")
        else:  # There are students who received no choice: extend left bar right bar, lower bottom bar, lower allocation text, change color, add unallocated stats
            self.allocationSummaryLabel.setText(_translate("MainWindow", f"Allocation Incomplete: {sum(record.values())}/{len(student_info)} students allocated"))
            self.allocationSummaryLabel.setStyleSheet("color: rgba(200, 50, 50, 1);")
            self.allocationSummaryLabel.setGeometry(QtCore.QRect(950, 521, 375, 31))
            self.unallocatedStudentLabel.setGeometry(QtCore.QRect(1000, 471, 361, 31))
            self.unallocatedStudentLabel.setText(_translate("MainWindow", f"Unallocated Students: {len(unlucky_students)}"))
            self.leftBar.setGeometry(QtCore.QRect(920, 260, 21, 300))
            self.rightBar.setGeometry(QtCore.QRect(1325, 260, 21, 300))
            self.bottomBar.setGeometry(QtCore.QRect(930, 543, 405, 31))

    def main_allocate(self):
        global allocate_success
        if import_success:
            self.allocateFirstLabel.setGeometry(QtCore.QRect(9999, 715, 315, 30))
            self.process_capacity()
            self.allocate_1st_choice()
            self.allocate_2nd_choice()
            if len(unlucky_students) != 0:
                self.first_optimize()
            self.allocate_3rd_choice()
            if len(unlucky_students) != 0:
                # Series of tricks to ensure that no students receive 3rd choice.
                self.final_help_unlucky()
            self.summarize_results()
            allocate_success = True
        else:
            allocate_success = False
            self.importFirstLabel.setGeometry(QtCore.QRect(41, 435, 315, 30))


    '''
    Output
    '''
    def form_result_df(self):
        data = {}
        data['Name'] = [name for name in student_info.keys()]
        data['Allocated Choice'] = []
        for choices in student_info.values():
            if len(choices) == 3:
                data['Allocated Choice'].append("Didn't Receive a Choice")
            else:
                data['Allocated Choice'].append(choices[-1].split(' - ')[-1])
        data['1st Choice'] = [choices[0] for choices in student_info.values()]
        data['2nd Choice'] = [choices[1] for choices in student_info.values()]
        data['3rd Choice'] = [choices[2] for choices in student_info.values()]
        return pd.DataFrame(data)

    def output_df(self, df):
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName()
            if file_name[-4:] == '.csv':
                df.to_csv(file_name, index=False)
            elif file_name[-5:] == '.xlsx':
                df.to_excel(file_name, index=False)
            else:
                file_name = file_name + '.xlsx'
                df.to_excel(file_name, index=False)
        except:
            print('ERROR - Error in exporting')
            pass

    def main_output(self):
        if allocate_success:
            df = self.form_result_df()
            self.output_df(df)
        else:
            self.allocateFirstLabel.setGeometry(QtCore.QRect(90, 715, 315, 30))


    '''
    Interactions
    '''
    def interactions(self):
        self.importButton.clicked.connect(self.main_process_data)
        self.allocateButton.clicked.connect(self.main_allocate)
        self.outputButton.clicked.connect(self.main_output)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except:
        print('ERROR - Master error')




'''
Notes for future improvements:
1. Implement a typo check functionality for exporting, such that even when a user types .xlsx or .csv wrong, the 
software still recognizes it and successful exports. 
2. Perform checks to ensure that the results being displayed are the actual results. 
3. Add more optimization algorithms, including more optimizations for final_help_unlucky AND one final optimization after all optimizations are done to improve results. 
4. Colors, fonts, more friendly error messages, music. 
'''

'''
Terminal command to turn .py script into .exe: 
pyinstaller --onefile scriptname.py
In this case, this is:
pyinstaller --onefile V3.0.py
This needs to be done in the same directory as the .py file. 

Alternative code:
pyinstaller -F -w scriptname.py
pyinstaller -F -w V3.0.py

Alternative code:
pyinstaller --onefile -w scriptname.py
pyinstaller --onefile -w V3.0.py
'''

"""
Optimization algorithms:

Algo rankings:
A (good optimization): 1, 2
B (round 1): 3 (110 --> 122, no 3rd choice resulted)
C (round 2): 5 (120 --> 123), 6 (10 --> 13), 7 (20 --> 23)
D (round 3): 4 (110 --> 123), 8 (110 --> 123)
E (round 4): 10 (120 --> 133)
F (round 5): 9 (110 --> 133)

1.
Conditions:
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice
A and B have the same 1st choice
A's 2nd choice is available
Result:
A drops 1st choice, gets 2nd choice
B gets 1st choice
Good optimization (13 or 10 --> 12)

2.
Conditions:
Student A: got 1st choice
Student B: got 2nd choice
Student C: no 1st choice, no 2nd choice
B and C have the same 2nd choice
A and B have the same 1st choice
A's 2nd choice is available
Result:
A drops 1st choice, gets 2nd choice
B drops 2nd choice, gets 1st choice
C gets 2nd choice
Good optimization (123 or 120 --> 122)

3.
Conditions: 
Student A: got 1st choice
Student B: got 1st choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
B and C have the same 1st choice
B's 2nd choice = A's 1st choice
A's 2nd choice is available
Result:
A drops 1st choice, gets 2nd choice
B drops 1st choice, gets 2nd choice
C gets 1st choice
110 --> 122 (round 1)

4. 
Conditions: 
Student A: got 1st choice
Student B: got 1st choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
A and C have the same 1st choice
A's 2nd choice = B's 1st choice
B's 3rd choice is available (2nd choice not available)
Result:
B drops 1st choice, gets 3rd choice
A drops 1st choice, gets 2nd choice
C gets 1st choice
110 --> 123 (round 3)

5.
Conditions: 
Student A: got 1st choice
Student B: got 2nd choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
A and C have the same 1st choice
A and B have the same 2nd choice
B's 3rd choice is available
Result:
B drops 2nd choice, gets 3rd choice
A drops 1st choice, gets 2nd choice
C gets 1st choice
120 --> 123 (round 2)

6.
Conditions: 
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A and B have the same 1st choice
A's 3rd choice is available
Result:
A drops 1st choice, gets 3rd choice
B gets 1st choice
10 --> 13 (round 2)

7.
Conditions: 
Student A: got 2nd choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A and B have the same 2nd choice
A's 3rd choice is available
Result:
A drops end choice, gets 3rd choice
B gets 2nd choice
20 --> 23 (round 2)

8.
Conditions: 
Student A: got 1st choice
Student B: got 1st choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
A and C have the same 1st choice
B's 1st choice = A's 3rd choice
B's 2nd choice is available
Result:
B drops 1st choice, gets 2nd choice
A drops 1st choice, gets 3rd choice
C gets 1st choice
110 --> 123 (round 3)

9.
Conditions:
Student A: got 1st choice
Student B: got 1st choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
B and C have the same 1st choice
A's 1st choice = B's 3rd choice
A's 3rd choice is available (2nd choice not available)
Result:
B drops 1st choice, gets 3rd choice
A drops 1st choice, gets 3rd choice
C gets 1st choice
110 --> 133 (round 5)

10.
Conditions: 
Student A: got 2nd choice
Student B: got 1st choice
Student C: no 1st choice, no 2nd choice, no 3rd choice
B and C have the same 1st choice
A's 2nd choice = B's 3rd choice
A's 3rd choice is available
Result:
A drops 2nd choice, gets 3rd choice
B drops 1st choice, gets 3rd choice
C gets 1st choice
120 --> 133 (round 4)

11
Conditions:
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A's 1st choice = B's 2nd choice
A's 2nd choice is available
Result:
A gets 2nd choice
B gets 2nd choice
10 --> 22 (round 1)

12
Conditions:
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A's 1st choice = B's 2nd choice
A's 3rd choice is available (2nd choice not available)
Result:
A gets 3rd choice
B gets 2nd choice
10 --> 23 (round 3)

13
Conditions:
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A's 1st choice = B's 3rd choice
A's 2nd choice available
Result:
A gets 2nd choice
B gets 3rd choice
10 --> 23 (round 3)

14 
Conditions:
Student A: got 1st choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A's 1st choice = B's 3rd choice
A's 3rd choice is available (2nd choice not available)
Result: 
A gets 3rd choice
B gets 3rd choice
10 --> 33 (round 5)

15: 
Conditions: 
Student A: got 2nd choice
Student B: no 1st choice, no 2nd choice, no 3rd choice
A's 3rd choice is available
A's 2nd choice = B's 3rd choice
Result: 
A gets 3rd
B gets 3rd
20 --> 33 (round 4)
"""
























