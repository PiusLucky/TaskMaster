from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired

TASK_PRIORITY_CHOICE = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
TASK_CATEGORY_CHOICE = [
    ('fun', 'Fun'), ('studies', 'Studies'), ('work', 'Work'), ('other', 'Other')]


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField(
        'Category', choices=TASK_CATEGORY_CHOICE, validators=[DataRequired()])
    priority = SelectField(
        'Priority', choices=TASK_PRIORITY_CHOICE, validators=[DataRequired()])
    dueDate = DateField('Due Date', validators=[
                        DataRequired()], format='%Y-%m-%d')

