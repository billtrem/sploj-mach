from django.db import models
from django.utils.text import slugify


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    signup_link = models.URLField(blank=True, null=True)
    video_embed_code = models.TextField(blank=True)
    photo = models.ImageField(upload_to='project_photos/', blank=True, null=True)
    color = models.CharField(max_length=7, default='#000000', help_text='Hex color code for this category, e.g. #FF5733')

    def __str__(self):
        return self.name


class Post(models.Model):
    LINK_LABEL_CHOICES = [
        ('book', 'Book Now'),
        ('signup', 'Sign Up'),
        ('learn', 'Learn More'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('ProjectCategory', related_name='posts')
    link = models.URLField(blank=True, help_text="External link (e.g., SumUp, Eventbrite, Google Form)")
    link_label = models.CharField(max_length=20, choices=LINK_LABEL_CHOICES, blank=True, help_text="Button label for the link")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class InfoPage(models.Model):
    welcome_message = models.TextField()
    contact_description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    opening_hours = models.TextField(help_text="Use line breaks to separate days.")
    mission_text = models.TextField(blank=True)
    support_text = models.TextField(blank=True)

    def __str__(self):
        return "Info Page"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    description = models.TextField(blank=True)

    info_page = models.ForeignKey(
        'InfoPage',
        related_name='team_members',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Leave blank if this team member is for a specific category only."
    )

    project_category = models.ForeignKey(
        'ProjectCategory',
        related_name='team_members',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Assign this team member to a specific category (e.g. Radio Dyfi). Leave blank if general staff."
    )

    def __str__(self):
        return self.name


class Funder(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='funders/', blank=True, null=True)
    project_categories = models.ManyToManyField(
        'ProjectCategory',
        blank=True,
        related_name='funders'
    )
    show_on_info_page = models.BooleanField(default=False)

    def __str__(self):
        return self.name
