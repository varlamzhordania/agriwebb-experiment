from django.db import models


class PastureLivestockData(models.Model):
    defaults_template = models.OneToOneField(
        "DefaultsTemplate",
        related_name="pasture_livestock_data",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    # data = JSONField(default=list)
    user_updated = models.BooleanField(blank=True, default=False)
    ## new fields
    year = models.IntegerField(
        verbose_name="Year",
        blank=True,
        null=True,
        help_text="The year the data belongs to."
    )
    crop_id = models.IntegerField(
        verbose_name="Crop ID",
        blank=True,
        null=True,
        help_text="The ID of crop,the data belongs to."
    )
    species = models.CharField(
        verbose_name="Species",
        max_length=255,
        null=True,
        blank=True,
        help_text="The list of animal species."
    )
    weight_unit = models.CharField(
        verbose_name="Weight Unit",
        max_length=10,
        null=True,
        blank=True,
        help_text="The weight unit (lbs...etc)."
    )
    animal_details = models.CharField(
        verbose_name="Animal Details",
        max_length=255,
        null=True,
        blank=True,
        help_text="The list of animal details."
    )
    average_weight = models.FloatField(
        verbose_name="Average Weight",
        null=True,
        blank=True,
        help_text="The average weight of all animals."
    )


class PastureFeedData(models.Model):
    defaults_template = models.OneToOneField(
        "DefaultsTemplate",
        related_name="pasture_feed_data",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    # data = JSONField(default=list)
    user_updated = models.BooleanField(blank=True, default=False)
    ## new fields
    year = models.IntegerField(
        verbose_name="Year",
        blank=True,
        null=True,
        help_text="The year the data belongs to."
    )
    unit = models.CharField(
        verbose_name="Unit",
        max_length=255,
        null=True,
        blank=True,
        help_text="The unit of feeding."
    )
    amount = models.FloatField(
        verbose_name="Amount",
        null=True,
        blank=True,
        help_text="The amount of feeding."
    )
    method = models.CharField(
        verbose_name="Method",
        max_length=255,
        null=True,
        blank=True,
        help_text="The method of feeding."
    )
    crop_id = models.IntegerField(
        verbose_name="Crop ID",
        blank=True,
        null=True,
        help_text="The ID of crop,the data belongs to."
    )
    additive = models.CharField(
        verbose_name="Additive",
        max_length=255,
        null=True,
        blank=True,
        help_text="The additive feed."
    )
    dmi_unit = models.CharField(
        verbose_name="DMI Unit",
        max_length=255,
        null=True,
        blank=True,
    )
    days_on_additive = models.IntegerField(
        verbose_name="Days On Additive",
        null=True,
        blank=True,
        help_text="The number of days on additive feed."
    )
    expected_daily_dmi = models.FloatField(
        verbose_name="Expected Daily DMI",
        null=True,
        blank=True,
        help_text="The expected daily DMI feed."
    )


class PastureStockingData(models.Model):
    defaults_template = models.OneToOneField(
        "DefaultsTemplate",
        related_name="pasture_stocking_data",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    # data = JSONField(default=list)
    user_updated = models.BooleanField(blank=True, default=False)
    ## new fields
    year = models.IntegerField(
        verbose_name="Year",
        blank=True,
        null=True,
        help_text="The year the data belongs to."
    )
    crop_id = models.IntegerField(
        verbose_name="Crop ID",
        blank=True,
        null=True,
        help_text="The ID of crop,the data belongs to."
    )
    count_animals = models.IntegerField(
        verbose_name="Animals Count",
        null=True,
        blank=True,
        help_text="The number of animals."
    )
