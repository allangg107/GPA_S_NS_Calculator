import re

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

currQuarter = 1
numClasses = 0
gpa = 0
classesGPA = []
classesSNS = []


class GPACalc(App):
    pass


class MainGrid(GridLayout):
    def calculate(self):
        global numClasses
        global gpa
        numClasses = 0
        gpa = 0
        # calculate GPA based on given grades and S/NSs
        for number in range(0, len(classesGPA)):
            if classesSNS[number].active is False and classesGPA[number].text != "":
                gpa += float(classesGPA[number].text)
                numClasses += 1

        if numClasses != 0:
            gpa = gpa / numClasses

        self.ids.gpa_label.text = "GPA: " + str(gpa)


class MainScrollView(ScrollView):
    pass


class QuartersGrid(GridLayout):
    def __init__(self, **kwargs):
        super(QuartersGrid, self).__init__(**kwargs)

        button = Button(text="Add quarter", size_hint=(1, None), height="50dp")
        button.on_press = self.add_quarter
        self.add_widget(button)

        global currQuarter
        # add initial quarters by default
        for number in range(0, 8):
            self.add_quarter()

    def add_quarter(self):
        global currQuarter
        quarter_label = QuarterLabel(text='Quarter ' + str(currQuarter), font_size=24, size_hint=(1, None))
        quarter_label.texture_size = quarter_label.size
        quarter_label.size = quarter_label.texture_size
        currQuarter += 1
        self.add_widget(quarter_label, 1)
        self.add_widget(ClassesLayout(), 1)


class QuarterLabel(Label):
    pass


class ClassesLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # the add class button
        button = Button(text="Add class", size_hint=(1, None))
        button.height = 26
        button.on_press = self.add_class
        self.add_widget(button)

        for number in range(0, 3):
            self.add_class()

    def add_class(self):
        classNum = int((len(self.children) + 2) / 3)
        class_label = ClassLabel(text='Class ' + str(classNum))
        self.add_widget(class_label, 1)

        sns_checkbox = SNSCheck()
        classesSNS.append(sns_checkbox)
        self.add_widget(sns_checkbox, 1)

        gpa_input = GPAInput()
        classesGPA.append(gpa_input)
        classNum += 1
        self.add_widget(gpa_input, 1)


class ClassLabel(Label):
    pass


class SNSCheck(CheckBox):
    pass


class GPAInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(GPAInput, self).insert_text(s, from_undo=from_undo)


GPACalc().run()
