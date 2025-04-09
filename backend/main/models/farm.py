from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Farm(models.Model):
    agri_id = models.CharField(
        verbose_name=_('AgriWebb Farm ID'),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        help_text=_('AgriWebb unique Farm ID, named farm_id to avoid conflict with the django id'),
    )
    name = models.CharField(
        verbose_name=_('Farm Name'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("AgriWebb Farm Name,"),
    )
    address = models.ForeignKey(
        "Address",
        verbose_name=_('Farm Address'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("AgriWebb Farm Address,"),
    )
    time_zone = models.CharField(
        verbose_name=_('Farm TimeZone'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Farm TimeZone, All dates are returned as UTC unix epoch in milliseconds, this timezone can be used to convert to the farm local time. The field will contain a timezone name from the list: https://timezonedb.com/time-zones"
        ),
    )
    map_features = models.ManyToManyField(
        "MapFeature",
        verbose_name=_('Farm Map Features'),
        blank=True,
        help_text=_(
            "AgriWebb Farm Map Features, it will return as array of map featues. since it have a farm_id, it can be set to use reverse relationship via a foreignkey"
        ),
    )
    fields = models.ManyToManyField(
        "Field",
        verbose_name=_('Farm Fields'),
        blank=True,
        help_text=_(
            "AgriWebb Farm fields , it will return as array of fields. since it have a farm_id, it can be set to use reverse relationship via a foreignkey"
        ),
    )
    identifiers = models.ManyToManyField(
        "ExternalIdentifier",
        verbose_name=_('External Identifiers'),
        blank=True,
        help_text=_("AgriWebb Farm Identifiers, List of external identifers of the farm")
    )


class Address(models.Model):
    address1 = models.CharField(
        verbose_name=_('Address 1'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Address 1'),
    )
    address2 = models.CharField(
        verbose_name=_('Address 2'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Address 2'),
    )
    country = models.CharField(
        verbose_name=_('Country'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Country'),
    )
    postcode = models.CharField(
        verbose_name=_('Postcode'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Postcode'),
    )
    town = models.CharField(
        verbose_name=_('Town'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Town'),
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb State'),
    )
    location = models.ForeignKey(
        "GeoPoint",
        verbose_name=_('Location'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            'AgriWebb Location, on the query it wont return array of locations so assumed its 1 single geoPoint per address'
        ),
    )


class GeoPoint(models.Model):
    lat = models.FloatField(
        verbose_name=_('Latitude'),
        null=True,
        blank=True,
        help_text=_('AgriWebb Latitude on GeoPoint'),
    )
    long = models.FloatField(
        verbose_name=_('Longitude'),
        null=True,
        blank=True,
        help_text=_('AgriWebb Longitude on GeoPoint'),
    )


class MapFeature(models.Model):
    class TypeChoices(models.TextChoices):
        RAINGAUGE = "RAIN_GAUGE", _("Rain Gauge")
        WATERTANK = "WATER_TANK", _("Water Tank")
        TROUGH = "TROUGH", _("Trough")

    uu_id = models.UUIDField(
        verbose_name=_('Agri ID'),
        unique=True,
        null=True,
        blank=True,
        help_text=_('AgriWebb uuid unique identifier of the map feature'),
    )
    name = models.CharField(
        verbose_name=_('Map Name'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('AgriWebb Map Name, Human friendly name of the feature, shown to the farmer'),
    )
    description = models.TextField(
        verbose_name=_('Map Description'),
        null=True,
        blank=True,
        help_text=_(
            'AgriWebb Map Description, Longer description associated with the feature, shown to the farmer'
        ),
    )
    geometry = models.ForeignKey(
        "GeoFeature",
        verbose_name=_('Map Geometry'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_('AgriWebb Location of the map feature')
    )
    farm_id = models.UUIDField(
        verbose_name=_('Farm ID'),
        null=True,
        blank=True,
        help_text=_(
            'AgriWebb Farm ID, its a many to many relations ships so not using a foreignkey since a middle table will be created'
        ),
    )

    type = models.CharField(
        verbose_name=_('Map Type'),
        choices=TypeChoices.choices,
        max_length=16,
        null=True,
        blank=True,
        help_text=_("AgriWebb Map Type"),
    )
    alert = models.ForeignKey(
        "CapacityAlert",
        verbose_name=_('Alert'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Alert, Level reading alerts. Only applicable for features with level readings such as water tanks."
        )
    )
    capacity = models.ForeignKey(
        "Capacity",
        verbose_name=_('Capacity'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Capacity of the feature. Only applicable for features with level readings such as water tanks."
        ),
    )
    identifier = models.CharField(
        verbose_name=_('Identifier'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Identifier of the feature,     External identifier of the feature such as the sensor serial number, used to allow cross system mapping"
        ),
    )


class GeoFeature(models.Model):
    class TypeChoices(models.TextChoices):
        POLYGON = "Polygon", _("Polygon")
        MULTIPOLYGON = "MultiPolygon", _("MultiPolygon")
        POINT = "Point", _("Point")
        MULTIPOINT = "MultiPoint", _("MultiPoint")
        LINESTRING = "LineString", _("LineString")
        MULTILINESTRING = "MultiLineString", _("MultiLineString")
        GEOMETRYCOLLECTION = "GeometryCollection", _("GeometryCollection")

    type = models.CharField(
        verbose_name=_('Type'),
        choices=TypeChoices.choices,
        max_length=32,
        null=True,
        blank=True,
        help_text=_("AgriWebb Type of feature"),
    )
    coordinates = gis_models.GeometryField(
        verbose_name=_("Coordinates"),
        null=True,
        blank=True,
        help_text=_("Geometry field storing coordinates, maybe need to change the field later"),
    )


class CapacityAlert(models.Model):
    critical = models.FloatField(
        verbose_name=_('Critical Alert'),
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Critical Alert,Percentage of the capacity at which the tank is considered at critical level. Users will be notified when the tank's water level goes below this percentage. max: 500 min: 0"
        ),
    )
    warning = models.FloatField(
        verbose_name=_('Warning Alert'),
        null=True,
        blank=True,
        help_text=_(
            "AgriWebb Warning Alert, Percentage of the capacity at which the tank is considered at warning level. Users will be notified when the tank's water level goes below this percentage. max: 500 min: 0"
        )
    )


class Capacity(models.Model):
    class ModeChoices(models.TextChoices):
        DEPTH = "depth", _("Depth")

    class UnitChoices(models.TextChoices):
        MM = "mm", _("mm")
        CM = "cm", _("cm")
        METER = "meter", _("meter")
        INCH = "inch", _("inch")
        FOOT = "foot", _("foot")
        YARD = "yard", _("yard")

    mode = models.CharField(
        verbose_name=_('Mode'),
        blank=True,
        null=True,
        help_text=_("AgriWebb Capacity Mode"),
    )
    value = models.FloatField(
        verbose_name=_('Value'),
        blank=True,
        null=True,
        help_text=_("AgriWebb Capacity Value"),
    )
    unit = models.CharField(
        verbose_name=_('Unit'),
        choices=UnitChoices.choices,
        blank=True,
        null=True,
        help_text=_("AgriWebb Capacity Unit"),
    )


class Field(models.Model):
    class UnitChoices(models.TextChoices):
        ACRE = "acre", _("Acre")
        SQFT = "sqft", _("SQFT")
        SQYD = "sqyd", _("SQYD")
        M2 = "m2", _("M2")
        HECTARE = "hectare", _("Hectare")

    class LandUseChoices(models.TextChoices):
        GRAZING = "Grazing", _("Grazing")
        CROPPING = "Cropping", _("Cropping")
        HAY = "Hay", _("Hay")
        YARD = "Yard", _("Yard")
        FEEDLOT = "Feedlot", _("Feedlot")
        PEN = "Pen", _("Pen")
        LANEWAY = "Laneway", _("Laneway")
        VEGETATION = "Vegetation", _("Vegetation")
        SILVOPASTURE = "Silvopasture", _("Silvopasture")
        RANGELAND = "Rangeland", _("Rangeland")
        BADLAND = "Badland", _("Badland")
        WETLAND = "Wetland", _("Wetland")
        EROSIONZONE = "ErosionZone", _("Erosion Zone")
        RESTORATIONZONE = "RestorationZone", _("Restoration Zone")
        CONVERSIONZONE = "ConversionZone", _("Conversion Zone")
        NONAGRICULTURE = "NonAgriculture", _("NonAgriculture")

    agri_id = models.CharField(
        verbose_name=_('Agri ID'),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text=_("AgriWebb Internal ID, didnt specify it couldn't be null in documentation"),
    )
    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        blank=True,
        null=True,
        help_text=_("AgriWebb Creation Date, didnt specify if its unix timestamp"),
    )
    last_modified_date = models.DateTimeField(
        verbose_name=_('Last modified date'),
        blank=True,
        null=True,
        help_text=_(
            "AgriWebb Last modified Date, didnt specify if its unix timestamp, Can be used to monitor for changes in particular geometry resizes and usage changes"
        ),
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("AgriWebb Name"),
    )
    location = models.ForeignKey(
        GeoPoint,
        verbose_name=_('Location'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("AgriWebb field Location,"),
    )
    geometry = models.ForeignKey(
        GeoFeature,
        verbose_name=_('Geometry'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("AgriWebb field Geometry,"),
    )
    farm_id = models.CharField(
        verbose_name=_('Farm ID'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("AgriWebb Farm ID"),
    )
    total_area = models.FloatField(
        verbose_name=_('Total Area'),
        blank=True,
        null=True,
        help_text=_("AgriWebb Total Area, The total area of the field in hectares"),
    )
    grazable_area = models.FloatField(
        verbose_name=_('Grazable Area'),
        blank=True,
        null=True,
        help_text=_("AgriWebb Grazable Area, The grazable area of the field in hectares"),
    )
    unit = models.CharField(
        verbose_name=_('Unit'),
        max_length=8,
        choices=UnitChoices.choices,
        blank=True,
        null=True,
        help_text=_(
            "AgriWebb Unit, This represents the type of unit used to measure the field area"
        ),
    )
    land_use = models.CharField(
        verbose_name=_('Land Use'),
        max_length=32,
        choices=LandUseChoices.choices,
        blank=True,
        null=True,
        help_text=_("AgriWebb Land Use, Describes the land use for the given area"),
    )
    crop_type = models.CharField(
        verbose_name=_('Crop Type'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "AgriWebb Crop Type, The free form name of the type of crop growing in the field"
        ),

    )
    identifiers = models.ManyToManyField(
        'ExternalIdentifier',
        verbose_name=_('Identifiers'),
        blank=True,
        help_text=_("AgriWebb Identifier, List of external identifers of the field"),
    )


class ExternalIdentifier(models.Model):
    type = models.CharField(
        verbose_name=_('Type'),
        max_length=255,
        blank=True,
        null=True,
    )
    value = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_('Value'),
        blank=True,
        default=list,
        help_text=_("List of values")
    )
