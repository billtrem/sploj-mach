from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage


class Project(models.Model):
    LINK_LABEL_CHOICES = [
        ('book', 'Book Now'),
        ('signup', 'Sign Up'),
        ('learn', 'Learn More'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # Images - Force Cloudinary storage
    poster = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='projects/posters/',
        blank=True,
        null=True,
        help_text="Vertical poster used on the What's On page."
    )
    horizontal_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='projects/horizontal/',
        blank=True,
        null=True,
        help_text="Horizontal image or banner used in the modal."
    )

    video_embed_code = models.TextField(blank=True, help_text="Embed code for a video/trailer.")

    link = models.URLField(blank=True, help_text="External link for booking, signup, etc.")
    link_label = models.CharField(
        max_length=20,
        choices=LINK_LABEL_CHOICES,
        default='learn',
        blank=True
    )

    color = models.CharField(max_length=7, default='#000000', help_text="Hex color for modal accents.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class InfoSection(models.Model):
    """Info section for a project or Sploj overall."""
    project = models.ForeignKey(
        Project,
        related_name='info_sections',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='info/sections/',
        blank=True,
        null=True,
        help_text="Optional image for this section (e.g., header photo)"
    )
    is_links_section = models.BooleanField(
        default=False,
        help_text="Check if this section should display as a list of links"
    )

    # Optional links if this is a link section
    link_1_label = models.CharField(max_length=200, blank=True)
    link_1_url = models.URLField(blank=True)
    link_2_label = models.CharField(max_length=200, blank=True)
    link_2_url = models.URLField(blank=True)
    link_3_label = models.CharField(max_length=200, blank=True)
    link_3_url = models.URLField(blank=True)
    link_4_label = models.CharField(max_length=200, blank=True)
    link_4_url = models.URLField(blank=True)

    # Funders logos inside the same section
    funder_logo_1 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_2 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_3 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_4 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)

    def __str__(self):
        if self.project:
            return f"{self.title} – {self.project.title}"
        return self.title
