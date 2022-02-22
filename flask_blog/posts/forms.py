from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, ValidationError, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class NewTopicForm(FlaskForm):
    topicTitle = StringField("Topic Title",
                             validators=[DataRequired(),
                                         Length(min=5, max=50)],
                             render_kw={"placeholder": "Subject of your topic"})

    topicBody = TextAreaField("Topic Body",
                              validators=[DataRequired(),
                                          Length(min=10, max=10000)],
                              render_kw={"placeholder": "Let's get started"})

    topicMedia = FileField("Topic Media", validators=[
                           FileAllowed(["jpg", "jpeg", "png"])])

    topicTags = StringField(
        "Tags", render_kw={"placeholder": "Use comma to separate tags"})

    newTopicTags = HiddenField(label=None)

    newPostSubmit = SubmitField("Create Post")

    def validate_topicTags(self, topicTags):
        tags = self.newTopicTags.data
        tagsList = tags.split(",")
        if len(tagsList) > 5:
            self.newTopicTags.data = ""
            topicTags.data = ""
            raise ValidationError(
                'You can not have more than 5 tags')
