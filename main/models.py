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

    # Main public button
    link = models.URLField(blank=True, help_text="External link for booking, signup, etc.")
    link_label = models.CharField(
        max_length=20,
        choices=LINK_LABEL_CHOICES,
        default='learn',
        blank=True
    )

    # Volunteer sign-up button
    volunteer_link = models.URLField(
        blank=True,
        help_text="Link to volunteer sign-up form (Google Form or internal page)"
    )
    volunteer_label = models.CharField(
        max_length=50,
        default='Sign Up',
        blank=True,
        help_text="Label for the volunteer button (default: 'Sign Up')"
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

    # Main image
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='info/sections/',
        blank=True,
        null=True,
        help_text="Optional main image for this section"
    )

    # Carousel images (up to 20)
    for i in range(1, 21):
        locals()[f'carousel_image_{i}'] = models.ImageField(
            storage=MediaCloudinaryStorage(),
            upload_to='info/sections/',
            blank=True,
            null=True
        )
    del i

    is_links_section = models.BooleanField(
        default=False,
        help_text="Check if this section should display as a list of links"
    )

    # Optional links (up to 10)
    for i in range(1, 11):
        locals()[f'link_{i}_label'] = models.CharField(max_length=200, blank=True)
        locals()[f'link_{i}_url'] = models.URLField(blank=True)
    del i

    # Funders logos
    funder_logo_1 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_2 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_3 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)
    funder_logo_4 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='info/funders/', blank=True, null=True)

    def get_carousel_images(self):
        """Return all non-empty carousel images as a list."""
        return [getattr(self, f'carousel_image_{i}') for i in range(1, 21) if getattr(self, f'carousel_image_{i}')]

    def get_links(self):
        """Return all non-empty link labels/URLs as a list of dicts."""
        return [
            {'label': getattr(self, f'link_{i}_label'), 'url': getattr(self, f'link_{i}_url')}
            for i in range(1, 11)
            if getattr(self, f'link_{i}_label') and getattr(self, f'link_{i}_url')
        ]

    def __str__(self):
        return f"{self.title} – {self.project.title}" if self.project else self.title
