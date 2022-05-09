from sepal_ui import sepalwidgets as sw


class StepperStep(sw.StepperStep):
    """wrapper for the stepper used in the parameter tile"""

    def __init__(self, i, name):

        super().__init__(key=i, step=i, complete=False, editable=True, children=[name])


class StepperContent(sw.StepperContent):
    """wrapper for the stepper content used in the parameter tile"""

    def __init__(self, i, content):

        super().__init__(key=i, step=i, children=[content])
