from django import forms

class baseForm(forms.Form):

    def as_html_field(self):
        return self._html_output(normal_row="<div class='field half'>%(label)s %(field)s</div>",
                                 error_row="<div class='error'></div>",
                                 row_ender='',
                                 help_text_html=' %s',
                                 errors_on_separate_row=False)
