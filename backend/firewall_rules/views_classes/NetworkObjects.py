from django.forms import ModelForm
from firewall_rules.models import *

# Create the form class.
class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ['action', 'static_source', 'static_destination']

# Creating a form to add an article.
#form = ArticleForm()

# Creating a form to change an existing article.
#>>> article = Article.objects.get(pk=1)
#>>> form = ArticleForm(instance=article)