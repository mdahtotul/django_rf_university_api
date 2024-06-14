To work with free tinymce and equation

### Step - 1: Copy the static folder of this project and paste on your project.

### Step - 2: Install tinymce exact version in your project

```
pip install django-tinymce==3.4.0
```

### Step - 3: Add tinymce to your installed app in settings.py

```
INSTALLED_APPS = [
    # .... other apps
    "tinymce",
]
```

### Step - 4: Check STATIC_URL && STATIC_ROOT is working

### Step - 5: Add this code to your project settings.py

```
TINYMCE_JS_URL = "tinymce/tinymce.min.js"

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount",
    "external_plugins": {
        "tiny_mce_wiris": "https://www.wiris.net/demo/plugins/tiny_mce/plugin.js"
    },
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft | tiny_mce_wiris_formulaEditor | tiny_mce_wiris_formulaEditorChemistry"
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
```

### Step - 6: (Final) Add changes to your modal

```
from django.db import models
from tinymce import models as tinymce_models

class Stem(models.Model):
    description = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stem"
        verbose_name_plural = "Stems"

    def __str__(self) -> str:
        return f"{self.id} -- {self.description[:50]}"
```

Everything is done. Now Register your modal to admin.py and check in the admin panel
