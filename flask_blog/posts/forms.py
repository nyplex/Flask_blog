from email import message
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, SubmitField, ValidationError, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length
from flask_blog import mongo


class NewTopicForm(FlaskForm):
    # get the categories to populate the catgeries field
    categories = mongo.db.categories.find().sort("category_name")
    choices = []
    for category in categories:
        cat_name = category["category_name"]
        choices.append((cat_name, cat_name.capitalize()))

    topicTitle = StringField("Topic Title",
                             validators=[DataRequired(),
                                         Length(min=5, max=50)],
                             render_kw={"placeholder": "Subject of your topic"})

    topicBody = TextAreaField("Topic Body",
                              validators=[DataRequired(),
                                          Length(min=10, max=10000)],
                              render_kw={"placeholder": "Let's get started"})

    topicMedia = FileField("Topic Media", validators=[
                           FileAllowed(["jpg", "jpeg", "png", "avi", "mp4",
                                       "gif", "m4v", "mkv", "mov", "mpeg", "mpg", "wmv"]),
                           FileSize(max_size=536870912,
                                    message="File too large! Maximum 512MB")])

    categoryField = SelectField(
        u"Category", choices=choices, validators=[DataRequired()])

    # Visible field , for user to input tags
    topicTags = StringField(
        "Tags", render_kw={"placeholder": "Use comma to separate tags"})
    # Hidden field that store the tags
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
