from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AgriWebbToken(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("User's this agriwebb token belong"),
    )
    organization = models.CharField(
        max_length=255,
        verbose_name=_("Organization"),
        null=True,
        blank=True,
        help_text=_("Organization's this agriwebb token belong"),
    )
    access_token = models.CharField(
        max_length=1024,
        verbose_name=_("Access Token"),
        null=True,
        blank=True,
        help_text=_("AgriWebb Access Token that retrieved in exchange."),
    )
    refresh_token = models.CharField(
        max_length=1024,
        verbose_name=_("Refresh Token"),
        null=True,
        blank=True,
        help_text=_("AgriWebb Refresh Token that retrieved in exchange."),
    )
    token_type = models.CharField(
        max_length=50,
        verbose_name=_("Token Type"),
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Token type that will be used on header, example: Bearer, Token...etc."
        ),
    )
    expires_in_seconds = models.IntegerField(
        verbose_name=_("Expiration Time in seconds"),
        null=True,
        blank=True,
        help_text=_("AgriWebb Token expiration time in seconds."),
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expiration Time"),
        null=True,
        blank=True,
        help_text=_("AgriWebb Token expiration date time."),
    )
    is_expired = models.BooleanField(verbose_name=_("Is Expired"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("AgriWebb Token")
        verbose_name_plural = _("AgriWebb Tokens")
        ordering = ("-created_at",)

    def __str__(self):
        return f"AgriWebb Token for {self.user or self.organization}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timezone.timedelta(seconds=self.expires_in_seconds)

        super().save(*args, **kwargs)

    def set_organization(self, organization):
        self.organization = organization
        self.save(update_fields=["organization"])

    def check_is_expired(self):
        expiration_time = self.created_at + timezone.timedelta(seconds=self.expires_in_seconds)
        if timezone.now() > expiration_time:
            self.is_expired = True
            self.save(update_fields=["is_expired"])
            return True
        return False

    def refresh(self, new_access_token, new_refresh_token, expires_in_seconds):
        self.access_token = new_access_token
        self.refresh_token = new_refresh_token
        self.expires_in_seconds = expires_in_seconds
        self.expires_at = timezone.now() + timezone.timedelta(seconds=self.expires_in_seconds)
        self.is_expired = False
        self.save()
