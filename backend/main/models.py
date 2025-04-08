from django.db import models
from django.utils.translation import gettext_lazy as _


class Record(models.Model):
    class RecordTypeChoices(models.TextChoices):
        AnimalTreatment = "animalTreatment", _("Animal Treatment")
        Feed = "feed", _("Feed")
        LocationChanged = "locationChanged", _("Location Changed")
        PregnancyScan = "pregnancyScan", _("Pregnancy Scan")
        Score = "score", _("Score")
        Weigh = "weigh", _("Weigh")

    record_id = models.IntegerField(
        verbose_name=_('Record ID'),
        primary_key=False,
        blank=True,
        null=True,
        help_text=_('Record ID on the agriwebb'),
    )
    record_type = models.CharField(
        max_length=20,
        verbose_name=_('Record Type'),
        choices=RecordTypeChoices.choices,
        blank=True,
        null=True,
        help_text=_('Record Type on the agriwebb'),
    )
    observation_date = models.DateTimeField(  # change to charField,it could be unix time
        verbose_name=_('Observation Date'),
        blank=True,
        null=True,
        help_text=_('Observation Date on the agriwebb'),
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name=_('Session ID'),
        blank=True,
        null=True,
        help_text=_('Session ID on the agriwebb'),
    )

    class Meta:
        abstract = True


class SharedAgeClassChoices(models.TextChoices):
    CALF = "calf", _("Calf")
    HEIFERCALF = "heifer_calf", _("Heifer Calf")
    STEERCALF = "steer_calf", _("Steer Calf")
    BULLCALF = "bull_calf", _("Bull Calf")
    NONBREEDINGBULLCALF = "non_breeding_bull_calf", _("Non-Breeding Bull Calf")
    WEANER = "weaner", _("Weaner")
    HEIFERWEANER = "heifer_weaner", _("Heifer Weaner")
    STEERWEANER = "steer_weaner", _("Steer Weaner")
    BULLWEANER = "bull_weaner", _("Bull Weaner")
    NONBREEDINGBULLWEANER = "non_breeding_bull_weaner", _("Non-Breeding Bull Weaner")
    YEARLING = "yearling", _("Yearling")
    HEIFER = "heifer", _("Heifer")
    SPAYEDHEIFER = "spayed_heifer", _("Spayed Heifer")
    COW = "cow", _("Cow")
    SPAYEDCOW = "spayed_cow", _("Spayed Cow")
    STEER = "steer", _("Steer")
    BULL = "bull", _("Bull")
    NONBREEDINGBULL = "non_breeding_bull", _("Non-Breeding Bull")
    NONBREEDINGMATUREBULL = "non_breeding_mature_bull", _("Non-Breeding Mature Bull")
    LAMB = "lamb", _("Lamb")
    EWELAMB = "ewe_lamb", _("Ewe Lamb")
    RAMLAMB = "ram_lamb", _("Ram Lamb")
    WETHERLAMB = "wether_lamb", _("Wether Lamb")
    EWEWEANER = "ewe_weaner", _("Ewe weaner")
    RAMWEANER = "ram_weaner", _("Ram Weaner")
    WETHERWEANER = "wether_weaner", _("Wether Weaner")
    HOGGET = "hogget", _("Hogget")
    EWEHOGGET = "ewe_hogget", _("Ewe Hogget")
    RAMHOGGET = "ram_hogget", _("Ram Hogget")
    WETHERHOGGET = "wether_hogget", _("Wether Hogget")
    MAIDENEWE = "maiden_ewe", _("Maiden Ewe")
    EWE = "ewe", _("Ewe")
    WETHER = "wether", _("Wether")
    RAM = "ram", _("Ram")
    UNKNOWN = "unknown", _("Unknown")


class Animal(Record):
    animal_id = models.IntegerField(
        verbose_name=_('Animal ID'),
        primary_key=False,
        blank=False,
        null=False,
        help_text=_('Animal ID on the agriwebb, specified non-null in documentaton'),
    )
    identity = models.ForeignKey(
        "AnimalIdentity",
        verbose_name=_('Identity'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Identity on the agriwebb, type of relationship unknown'),
    )
    age_class = models.IntegerField(
        verbose_name=_('Age Class'),
        choices=SharedAgeClassChoices.choices,
        blank=True,
        null=True,
        help_text=_('Age Class on the agriwebb'),
    )
    characteristics = models.ForeignKey(
        "AnimalCharacteristics",
        verbose_name=_('Characteristics'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Characteristics on the agriwebb'),
    )
    parentage = models.ForeignKey(
        "Parentage",
        verbose_name=_('Parentage'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Parentage on the agriwebb'),
    )


class AnimalIdentity(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        blank=False,
        null=False,
        help_text=_('Name on the agriwebb'),
    )
    eid = models.CharField(
        max_length=255,
        verbose_name=_('EID'),
        blank=True,
        null=True,
        help_text=_('EID on the agriwebb'),
    )
    vid = models.CharField(
        max_length=255,
        verbose_name=_('VID'),
        blank=True,
        null=True,
        help_text=_('VID on the agriwebb'),
    )
    management_tag = models.CharField(
        max_length=255,
        verbose_name=_('Management Tag'),
        blank=True,
        null=True,
        help_text=_('Management Tag on the agriwebb'),
    )
    brand = models.CharField(
        max_length=255,
        verbose_name=_('Brand'),
        blank=True,
        null=True,
        help_text=_('Brand on the agriwebb'),
    )
    tattoo = models.CharField(
        max_length=255,
        verbose_name=_('Tattoo'),
        blank=True,
        null=True,
        help_text=_('Tattoo on the agriwebb'),
    )
    tags = models.ManyToManyField(
        verbose_name=_('Tags'),
        blank=True,
        help_text=_(
            'Tags on the agriwebb, many to many relation ship cause on documentation its a list of tags'
        ),
    )
    tag_color_catalogue_id = models.CharField(
        max_length=255,
        verbose_name=_('Tag Color'),
        blank=True,
        null=True,
        help_text=_('Tag Color of the agriwebb'),
    )


class AnimalTag(models.Model):
    class TypeChoices(models.TextChoices):
        GENERIC = "generic", _("Generic")
        NLIS = "nlis", _("NLIS")
        APHIS = "aphis", _("APHIS")
        BCMS = "bcms", _("BCMS")
        SCOT_MOVES = "scot_moves", _("Scot Moves")
        UK_SHEEP = "uk_sheep", _("UK Sheep")
        EID = "eid", _("EID")
        VID = "vid", _("VID")
        EID_AND_VID = "eid_and_vid", _("EID AND VID")
        UHF = "uhf", _("UHF")
        BOLUS = "bolus", _("BOLUS")
        SLAUGHTER = "slaughter", _("Slaughter")
        BREED_SOCIETY = "breed_society", _("Breed Society")
        DNA = "dna", _("DNA")
        HEALTH = "health", _("Health")
        TRICH = "trich", _("Trich")
        GROUP = "group", _("Group")
        GROUP_MANAGEMENT = "group_management", _("Group Management")
        MANAGEMENT = "management", _("Management")

    class StateChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        REMOVED = " removed", _("Removed")
        REPLACED = " replaced", _("Replaced")

    agri_id = models.CharField(
        max_length=255,
        verbose_name=_('AgriWebb ID'),
        blank=True,
        null=True,
        help_text=_('AgriWebb Internal ID, changed named to agri_id to avoid conflict'),
    )
    eid = models.CharField(
        max_length=255,
        verbose_name=_('EID'),
        blank=True,
        null=True,
        help_text=_('EID on the agriwebb'),
    )
    vid = models.CharField(
        max_length=255,
        verbose_name=_('VID'),
        blank=True,
        null=True,
        help_text=_('VID on the agriwebb'),
    )
    management_tag = models.CharField(
        max_length=255,
        verbose_name=_('Management Tag'),
        blank=True,
        null=True,
        help_text=_(
            'Management Tag on the agriwebb, Visual label used for on farm management, which is not guaranteed to be unique.'
        ),
    )
    uhfEid = models.CharField(
        max_length=255,
        verbose_name=_('UHF EID'),
        blank=True,
        null=True,
        help_text=_('UHF EID on the agriwebb'),
    )
    dnaId = models.CharField(
        max_length=255,
        verbose_name=_('DNA ID'),
        blank=True,
        null=True,
        help_text=_('DNA ID on the agriwebb'),
    )
    registration_number = models.CharField(
        max_length=255,
        verbose_name=_('Registration Number'),
        blank=True,
        null=True,
        help_text=_('Registration Number on the agriwebb'),
    )
    breedSocietyId = models.CharField(
        max_length=255,
        verbose_name=_('Breed Society ID'),
        blank=True,
        null=True,
        help_text=_('Breed Society ID on the agriwebb'),
    )
    healthId = models.CharField(
        max_length=255,
        verbose_name=_('Health ID'),
        blank=True,
        null=True,
        help_text=_('Health ID on the agriwebb'),
    )
    tag_id = models.CharField(
        max_length=255,
        verbose_name=_('Tag ID'),
        blank=True,
        null=True,
        help_text=_('Tag ID on the agriwebb'),
    )
    tag_color_catalogue_id = models.CharField(
        max_length=255,
        verbose_name=_('Tag Color'),
        blank=True,
        null=True,
        help_text=_('Tag Color of the agriwebb'),
    )
    type = models.CharField(
        max_length=25,
        choices=TypeChoices.choices,
        verbose_name=_('Type'),
        blank=True,
        null=True,
        help_text=_('Tag Type on the agriwebb'),
    )
    state = models.CharField(
        max_length=10,
        choices=StateChoices.choices,
        verbose_name=_('State'),
        blank=True,
        null=True,
        help_text=_('Tag State on the agriwebb'),
    )
    removal_date = models.FloatField(
        verbose_name=_('Removal Date'),
        blank=True,
        null=True,
        help_text=_('Removal Date on the agriwebb, set float base on documentation'),
    )
    replacement_date = models.FloatField(
        verbose_name=_('Replacement Date'),
        blank=True,
        null=True,
        help_text=_('Replacement Date on the agriwebb, set float base on documentation'),
    )


class AnimalCharacteristics(models.Model):
    class DateAccuracyChoices(models.TextChoices):
        DAY = "day", _("Day")
        MONTH = "month", _("Month")
        YEAR = "year", _("Year")
        BEFOREYEAR = "before_year", _("Before Year")

    class SexChoices(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        UNSPECIFIED = "unspecified", _("Unspecified")

    class SpeciesChoices(models.TextChoices):
        CATTLE = "cattle", _("Cattle")
        SHEEP = "sheep", _("Sheep")
        GOATS = "goats", _("Goats")
        DEER = "deer", _("Deer")

    age_class = models.CharField(
        max_length=255,
        choices=SharedAgeClassChoices.choices,
        verbose_name=_('Age Class'),
        blank=True,
        null=True,
        help_text=_('Age Class on the agriwebb, Deprecated, use age class on animal'),
    )
    birth_date = models.FloatField(
        verbose_name=_('Birth Date'),
        blank=True,
        null=True,
        help_text=_('Birth Date on the agriwebb, set float base on documentation'),
    )
    birth_date_confidence = models.ForeignKey(
        "DateConfidence",
        on_delete=models.PROTECT,
        verbose_name=_('Birth Date Confidence'),
        blank=True,
        null=True,
        help_text=_('Birth Date Confidence on the agriwebb'),
    )
    birth_date_accuracy = models.CharField(
        max_length=20,
        verbose_name=_('Birth Date Accuracy'),
        choices=DateAccuracyChoices.choices,
        blank=True,
        null=True,
        help_text=_('Birth Date Accuracy on the agriwebb'),
    )
    birth_location_id = models.CharField(
        max_length=255,
        verbose_name=_('Birth Location ID'),
        blank=True,
        null=True,
        help_text=_('Birth Location ID of the agriwebb'),
    )
    birth_year = models.IntegerField(
        verbose_name=_('Birth Year'),
        blank=True,
        null=True,
        help_text=_('Birth Year on the agriwebb, set IntegerField base on documentation'),
    )
    breed_assessed = models.CharField(
        max_length=255,
        verbose_name=_('Breed Assessed'),
        blank=True,
        null=True,
        help_text=_('Breed Assessed on the agriwebb'),
    )
    visual_color = models.CharField(
        max_length=255,
        verbose_name=_('Visual Color'),
        blank=True,
        null=True,
        help_text=_('Visual Color on the agriwebb'),
    )
    sex = models.CharField(
        max_length=20,
        verbose_name=_("Sex"),
        blank=True,
        null=True,
        choices=SexChoices.choices,
        default=SexChoices.UNSPECIFIED,
    )
    species_common_name = models.CharField(
        max_length=20,
        verbose_name=_('Species Common Name'),
        blank=True,
        null=True,
        choices=SpeciesChoices.choices,
    )


class DateConfidence(models.Model):
    class Confidence(models.TextChoices):
        ACCURATE = "Accurate", "Accurate"
        ESTIMATE = "Estimate", "Estimate"
        UNKNOWN = "Unknown", "Unknown"

    year = models.CharField(
        max_length=16,
        verbose_name=_('Year'),
        choices=Confidence.choices,
        default=Confidence.UNKNOWN,
        help_text=_('Year Confidence on the agriwebb'),
    )
    month = models.CharField(
        max_length=16,
        verbose_name=_('Month'),
        choices=Confidence.choices,
        default=Confidence.UNKNOWN,
        help_text=_('Month Confidence on the agriwebb'),
    )
    day = models.CharField(
        max_length=16,
        verbose_name=_('Day'),
        choices=Confidence.choices,
        default=Confidence.UNKNOWN,
        help_text=_('Day Confidence on the agriwebb'),
    )


class ParentAnimalIdentity(models.Model):
    eid = models.CharField(
        max_length=255,
        verbose_name=_('EID'),
        null=True,
        blank=True,
        help_text=_('EID on the agriwebb'),
    )
    vid = models.CharField(
        max_length=255,
        verbose_name=_('Vid'),
        null=True,
        blank=True,
        help_text=_('Vid on the agriwebb'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        null=True,
        blank=True,
        help_text=_('Name on the agriwebb'),
    )


class AnimalParent(models.Model):
    class AnimalParentType(models.TextChoices):
        DAM = "dam", _("Dam")
        SIRE = "sire", _("Sire")
        UNKNOWN = "unknown", _("Unknown")

    parent_animal_id = models.CharField(
        max_length=255,
        verbose_name=_('Parent Animal ID'),
        null=True,
        blank=True,
        help_text=_('Parent Animal ID on the agriwebb'),
    )
    parent_animal_identity = models.ForeignKey(
        ParentAnimalIdentity,
        verbose_name=_('Parent Animal Identity'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    parent_type = models.CharField(
        max_length=10,
        verbose_name=_('Parent Type'),
        choices=AnimalParentType.choices,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class GeneticParent(AnimalParent):
    pass


class Surrogate(AnimalParent):
    pass


class Parentage(models.Model):
    dams = models.ManyToManyField(
        GeneticParent,
        verbose_name=_('Dams'),
        blank=True,
    )
    sires = models.ManyToManyField(
        GeneticParent,
        verbose_name=_('Sires'),
        blank=True
    )
    surrogate = models.ForeignKey(
        Surrogate,
        verbose_name=_('Surrogate'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
