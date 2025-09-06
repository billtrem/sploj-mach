from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    LINK_LABEL_CHOICES = [
        ('book', 'Book Now'),
        ('signup', 'Sign Up'),
        ('learn', 'Learn More'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # Images
    poster = models.ImageField(
        upload_to='projects/posters/',
        blank=True,
        null=True,
        help_text="Vertical poster used on the What's On page."
    )
    horizontal_image = models.ImageField(
        upload_to='projects/horizontal/',
        blank=True,
        null=True,
        help_text="Horizontal image or banner used in the modal."
    )

    # Optional embedded video
    video_embed_code = models.TextField(blank=True, help_text="Embed code for a video/trailer.")

    # Link
    link = models.URLField(blank=True, help_text="External link for booking, signup, etc.")
    link_label = models.CharField(
        max_length=20,
        choices=LINK_LABEL_CHOICES,
        default='learn',  # 👈 Always defaults to Learn More
        blank=True
    )

    # Styling
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
    """General info section for a project or for Sploj overall."""
    project = models.ForeignKey(
        Project,
        related_name='info_sections',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        if self.project:
            return f"{self.title} – {self.project.title}"
        return self.title
