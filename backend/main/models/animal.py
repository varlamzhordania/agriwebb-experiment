from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Record


class AnimalRecord(Record):
    pass


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


class SharedSpeciesChoices(models.TextChoices):
    CATTLE = "cattle", _("Cattle")
    SHEEP = "sheep", _("Sheep")
    GOATS = "goats", _("Goats")
    DEER = "deer", _("Deer")


class Animal(models.Model):
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
    management_group_id = models.CharField(
        max_length=255,
        verbose_name=_('Management Group ID'),
        blank=True,
        null=True,
        help_text=_('Management Group ID on the agriwebb'),
    )
    management_group = models.ForeignKey(
        "ManagementGroup",
        verbose_name=_('Management Group'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Management Group on the agriwebb'),
    )
    enterprise_id = models.CharField(
        max_length=255,
        verbose_name=_('Enterprise ID'),
        blank=True,
        null=True,
        help_text=_('Enterprise ID on the agriwebb'),
    )
    enterprise = models.ForeignKey(
        "Enterprise",
        verbose_name=_('Enterprise'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Enterprise ID on the agriwebb'),
    )
    state = models.ForeignKey(
        "AnimalState",
        verbose_name=_('State'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('State on the agriwebb'),
    )
    records = models.ManyToManyField(
        AnimalRecord,
        verbose_name=_('Records'),
        blank=True,
        help_text=_('Animal Record on the agriwebb, '),
    )
    farm_id = models.CharField(
        max_length=255,
        verbose_name=_('Farm ID'),
        blank=True,
        null=True,
        help_text=_('Farm ID on the agriwebb'),
    )
    purchased_from = models.CharField(
        max_length=255,
        verbose_name=_('Purchased From'),
        blank=True,
        null=True,
        help_text=_('Purchased From on the agriwebb'),
    )
    purchase_location_id = models.CharField(
        max_length=255,
        verbose_name=_('Purchase Location ID'),
        blank=True,
        null=True,
        help_text=_('Purchase Location ID on the agriwebb'),
    )
    creation_record_group_id = models.CharField(
        max_length=255,
        verbose_name=_('Creation Record Group ID'),
        blank=True,
        null=True,
        help_text=_('Creation Record Group ID on the agriwebb'),
    )
    creation_record_id = models.CharField(
        max_length=255,
        verbose_name=_('Creation Record ID'),
        blank=True,
        null=True,
        help_text=_('Creation Record ID on the agriwebb'),
    )
    birthing_record_id = models.CharField(
        max_length=255,
        verbose_name=_('Birth Record ID'),
        blank=True,
        null=True,
        help_text=_('Birth Record ID on the agriwebb'),
    )
    purchase_record_id = models.CharField(
        max_length=255,
        verbose_name=_('Purchase Record ID'),
        blank=True,
        null=True,
        help_text=_('Purchase Record ID on the agriwebb'),
    )
    sale_record_id = models.CharField(
        max_length=255,
        verbose_name=_('Sale Record ID'),
        blank=True,
        null=True,
        help_text=_('Sale Record ID on the agriwebb'),
    )
    _observation_date = models.DateTimeField(
        verbose_name=_('Observation Date'),
        blank=True,
        null=True,
        help_text=_('Observation Date on the agriwebb'),
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
        "AnimalTag",
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
        choices=SharedSpeciesChoices.choices,
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


class ManagementGroup(models.Model):
    management_group_id = models.CharField(
        max_length=255,
        verbose_name=_('Management Group ID'),
        null=False,
        blank=False,
        help_text=_('Management Group ID on the agriwebb,Internal ID in agriwebb'),
    )
    enterprise_id = models.CharField(
        max_length=255,
        verbose_name=_('Enterprise ID'),
        null=True,
        blank=True,
        help_text=_('Enterprise ID on the agriwebb'),
    )
    farm_id = models.CharField(
        max_length=255,
        verbose_name=_('Farm ID'),
        null=True,
        blank=True,
        help_text=_('Farm ID on the agriwebb'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        null=True,
        blank=True,
        help_text=_('Name of the management group on the agriwebb'),
    )
    species = models.CharField(
        max_length=20,
        choices=SharedSpeciesChoices.choices,
        verbose_name=_('Species'),
        null=True,
        blank=True,
        help_text=_('Species name on the agriwebb'),
    )
    type = models.CharField(
        max_length=255,
        verbose_name=_('Type'),
        null=True,
        blank=True,
        help_text=_('Type of the management group on the agriwebb'),
    )
    enterprise = models.ForeignKey(
        "Enterprise",
        verbose_name=_('Enterprise'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class Enterprise(models.Model):
    enterprise_id = models.CharField(
        max_length=255,
        verbose_name=_('Internal Enterprise ID'),
        null=False,
        blank=False,
        help_text=_('Enterprise ID on the agriwebb, Internal ID in agriwebb'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        null=True,
        blank=True,
        help_text=_('Name of the enterprise on the agriwebb'),
    )
    farm_id = models.CharField(
        max_length=255,
        verbose_name=_('Farm ID'),
        null=True,
        blank=True,
        help_text=_('Farm ID on the agriwebb'),
    )


class AnimalState(models.Model):
    class FateChoices(models.TextChoices):
        ALIVE = "Alive", _("Alive")
        DEAD = "Dead", _("Dead")
        SOLD = "Sold", _("Sold")
        INTRANSIT = "InTransit", _("InTransit")

    class FertilityStatusChoices(models.TextChoices):
        UNKNOWN = "Unknown", _("Unknown")
        FERTILE = "Fertile", _("Fertile")
        INFERTILE = "Infertile", _("Infertile")
        NEUTERED = "Neutered", _("Neutered")
        CRYPTORCHID = "Cryptorchid", _("Cryptorchid")
        NONBREEDING = "NonBreeding", _("NonBreeding")

    class ReproductiveStatusChoices(models.TextChoices):
        UNKNOWN = "Unknown", _("Unknown")
        NOTCYCLING = "NotCycling", _("NotCycling")
        PREGNANT = "Pregnant", _("Pregnant")
        EMPTY = "Empty", _("Empty")
        INVOLUTING = "Involuting", _("Involuting")

    current_location_id = models.CharField(
        max_length=255,
        verbose_name=_('Current Location ID'),
        null=True,
        blank=True,
        help_text=_(
            'Current location ID on the agriwebb,An internal AgriWebb ID representing the animals location, be that of a paddock, pen, yard, feedlot, vegetation, laneway etc'
        ),
    )
    on_farm = models.BooleanField(
        verbose_name=_('On Farm'),
        default=False,
        help_text=_("Indication of whether this animal is currently on or off-farm.")
    )
    on_farm_date = models.DateTimeField(
        verbose_name=_('On Farm Date'),
        null=True,
        blank=True,
        help_text=_('On Farm Date on the agriwebb'),
    )
    Last_seen = models.DateTimeField(
        verbose_name=_('Last Seen'),
        null=True,
        blank=True,
        help_text=_('Last Seen on the agriwebb'),
    )
    days_reared = models.IntegerField(
        verbose_name=_('Days Reared'),
        blank=True,
        null=True,
        help_text=_('Days Reared on the agriwebb,'),
    )
    off_farm_date = models.DateTimeField(
        verbose_name=_('Off Farm Date'),
        null=True,
        blank=True,
        help_text=_('Off Farm Date on the agriwebb'),
    )
    disposal_method = models.CharField(
        max_length=255,
        verbose_name=_('Disposal Method'),
        null=True,
        blank=True,
        help_text=_(
            'Disposal Method on the agriwebb,Indicates the disposal method for an animal that is dead. This may be Null if the animal is alive or disposal method is unknown.'
        ),
    )
    fate = models.CharField(
        max_length=16,
        verbose_name=_('Fate'),
        null=True,
        blank=True,
        choices=FateChoices.choices,
        help_text=_("Fate on the agriwebb"),
    )
    fertility_status = models.CharField(
        max_length=255,
        verbose_name=_('Fertility Status'),
        null=True,
        blank=True,
        choices=FertilityStatusChoices.choices,
        help_text=_('Fertility Status on the agriwebb'),
    )
    rearing_rank = models.FloatField(
        verbose_name=_('Rearing Rank'),
        null=True,
        blank=True,
        help_text=_('Rearing Rank on the agriwebb'),
    )
    reproductive_status = models.CharField(
        max_length=20,
        verbose_name=_('Reproductive Status'),
        null=True,
        blank=True,
        choices=ReproductiveStatusChoices.choices,
        help_text=_('Reproductive Status on the agriwebb'),
    )
    status_date = models.DateTimeField(
        verbose_name=_('Status Date'),
        null=True,
        blank=True,
        help_text=_('Status Date on the agriwebb'),
    )
    withholding_date_meat = models.DateTimeField(
        verbose_name=_('Withholding Date Meat'),
        null=True,
        blank=True,
        help_text=_('Withholding Date Meat on the agriwebb'),
    )
    withholding_date_export = models.DateTimeField(
        verbose_name=_('Withholding Date Export'),
        null=True,
        blank=True,
        help_text=_('Withholding Date Export on the agriwebb'),
    )
    withholding_date_organic = models.DateTimeField(
        verbose_name=_('Withholding Date Organic'),
        null=True,
        blank=True,
        help_text=_('Withholding Date Organic on the agriwebb'),
    )
    weaned = models.BooleanField(
        verbose_name=_('Weaned'),
        default=False,
        help_text=_('Weaned on the agriwebb'),
    )
    offspring_count = models.FloatField(
        verbose_name=_('Offspring Count'),
        null=True,
        blank=True,
        help_text=_('Offspring count on the agriwebb'),
    )
    weights = models.ForeignKey(
        "AnimalWeightSummary",
        verbose_name=_('Weights'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Weights on the agriwebb'),
    )
    body_condition_score = models.ForeignKey(
        "ConditionScore",
        verbose_name=_('Body Condition Score'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Body Condition Score on the agriwebb'),
    )
    body_condition_score_date = models.DateTimeField(
        verbose_name=_('Body Condition Score Date'),
        null=True,
        blank=True,
        help_text=_('Body Condition Score Date on the agriwebb'),
    )
    animal_units = models.ForeignKey(
        "AnimalUnit",
        verbose_name=_('Animal Units'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Animal Units on the agriwebb'),
    )
    has_had_offspring = models.BooleanField(
        verbose_name=_('Has Had Offspring'),
        default=False,
        help_text=_('Has Had Offspring on the agriwebb'),
    )


class ConditionScore(models.Model):
    class UnitChoices(models.TextChoices):
        BCS5 = "bcs5", _("BCS5")
        BCS9 = "bcs9", _("BCS9")

    unit = models.CharField(
        max_length=16,
        verbose_name=_('Unit'),
        choices=UnitChoices.choices,
        null=False,
        blank=False,
        help_text=_('Condition score Unit on the agriwebb'),
    )
    value = models.FloatField(
        verbose_name=_('Value'),
        null=False,
        blank=False,
        help_text=_('Condition score Value on the agriwebb'),
    )


class AnimalUnit(models.Model):
    class UnitChoices(models.TextChoices):
        DSE = "dse", _("DSE")
        AE = "ae", _("AE")
        LSU = "lsu", _("LSU")
        AU = "au", _("AU")
        MJPERDAY = "MJPerDay", _("MJ Per Day")

    unit = models.CharField(
        max_length=16,
        verbose_name=_('Unit'),
        choices=UnitChoices.choices,
        null=False,
        blank=False,
        help_text=_('Unit on the agriwebb'),
    )
    value = models.FloatField(
        verbose_name=_('Value'),
        null=False,
        blank=False,
        help_text=_('Value on the agriwebb'),
    )


class WeightGain(models.Model):
    class UnitChoices(models.TextChoices):
        KGPERDAY = "kgPerDay", _("Kg Per Day")
        GRAMPERDAY = "gramPerDay", _("Gram Per Day")
        OZPERDAY = "ozPerDay", _("Oz Per Day")
        LBPERDAY = "lbPerDay", _("Lb Per Day")

    unit = models.CharField(
        max_length=16,
        verbose_name=_('Unit'),
        choices=UnitChoices.choices,
        null=False,
        blank=False,
        help_text=_('Weight Unit on the agriwebb'),
    )
    value = models.FloatField(
        verbose_name=_('Weight Gain Value'),
        null=False,
        blank=False,
        help_text=_('Weight Gain Value on the agriwebb'),
    )


class Weight(models.Model):
    class UnitChoices(models.TextChoices):
        UG = "ug", _("Ug")
        MG = "mg", _("Mg")
        GRAM = "gram", _("Gram")
        KG = "kg", _("Kg")
        TONNE = "tonne", _("Tonne")
        OZ = "oz", _("Oz")
        LB = "lb", _("Lb")
        TON = "ton", _("Ton")
        STONE = "stone", _("Stone")
        LONGTON = "longton", _("Longton")

    unit = models.CharField(
        max_length=16,
        verbose_name=_('Unit'),
        choices=UnitChoices.choices,
        null=False,
        blank=False,
        help_text=_('Weight Unit on the agriwebb'),
    )
    value = models.FloatField(
        verbose_name=_('Weight Value'),
        null=False,
        blank=False,
        help_text=_('Weight Value on the agriwebb'),
    )


class AnimalWeightSummary(models.Model):
    live_average_daily_gain = models.ForeignKey(
        WeightGain,
        verbose_name=_('Live Average Daily Gain'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Live Average Daily Gain on the agriwebb"),
    )
    overall_average_daily_gain = models.ForeignKey(
        WeightGain,
        verbose_name=_('Overall Average Daily Gain'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Overall Average Daily Gain on the agriwebb"),
    )
    assumed_average_daily_gain = models.ForeignKey(
        WeightGain,
        verbose_name=_('Assumed Average Daily Gain'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Assumed Average Daily Gain on the agriwebb"),
    )
    live_weight_date = models.DateTimeField(
        verbose_name=_('Live Weight Date'),
        null=True,
        blank=True,
        help_text=_('Live Weight Date on the agriwebb'),
    )
    live_weight = models.ForeignKey(
        Weight,
        verbose_name=_('Live Weight'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Live Weight Date on the agriwebb'),
    )
    estimated_weight = models.ForeignKey(
        Weight,
        verbose_name=_('Estimated Weight'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Estimated Weight on the agriwebb'),
    )
