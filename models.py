from djongo import models

class Lawyer(models.Model):
    # Add choices for specialties
    SPECIALTY_CHOICES = [
        ('Family Law', 'Family Law'),
        ('Criminal Law', 'Criminal Law'), 
        ('Employment Law', 'Employment Law'),
        ('Immigration Law', 'Immigration Law'),
        ('Personal Injury', 'Personal Injury'),
        ('Real Estate', 'Real Estate'),
        ('Bankruptcy', 'Bankruptcy')
    ]

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Nepali', 'Nepali'),
        ('Tamil', 'Tamil'),
    ]
    
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)  # Add choices here
    languages = models.JSONField(default=list)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    experience = models.CharField(max_length=20)
    rating = models.FloatField()
    bio = models.TextField()
    image = models.URLField()

    class Meta:
        db_table = 'lawyers'

    def __str__(self):
        return self.name

class LegalRight(models.Model):
    CATEGORY_CHOICES = [
        ('employment', 'Employment Rights'),
        ('housing', 'Housing Rights'),
        ('consumer', 'Consumer Rights'),
        ('criminal', 'Criminal Rights'),
        ('family', 'Family Rights'),
        ('immigration', 'Immigration Rights'),
        ('disability', 'Disability Rights'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    detailed_info = models.TextField()
    tags = models.JSONField(default=list)  # For search functionality
    
    class Meta:
        ordering = ['category', 'title']
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"
    

class LegalDocument(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('family', 'Family'),
        ('housing', 'Housing'),
        ('employment', 'Employment'),
        ('estate', 'Estate'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    last_updated = models.DateField(auto_now=True)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_category_icon(self):
        icons = {
            'business': '📄',
            'family': '👨‍👩‍👧‍👦',
            'housing': '🏠',
            'employment': '💼',
            'estate': '✍️'
        }
        return icons.get(self.category, '📑')


class DocumentField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('select', 'Select'),
        ('checkbox', 'Checkbox'),
    ]
    
    document = models.ForeignKey(LegalDocument, related_name='fields', on_delete=models.CASCADE)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    required = models.BooleanField(default=False)
    options = models.TextField(blank=True, help_text="For select fields, enter options separated by commas")

    def get_options_list(self):
        if self.field_type == 'select' and self.options:
            return [opt.strip() for opt in self.options.split(',')]
        return []

