export enum GeoType {
    Polygon = "Polygon",
    MultiPolygon = "MultiPolygon",
    Point = "Point",
    MultiPoint = "MultiPoint",
    LineString = "LineString",
    MultiLineString = "MultiLineString",
    GeometryCollection = "GeometryCollection",
}

export enum CapacityMode {
    Depth = "depth",
}

export enum DepthUnit {
    mm = "mm",
    cm = "cm",
    meter = "meter",
    inch = "inch",
    foot = "foot",
    yard = "yard",
}

export enum MapFeatureType {
    RAIN_GAUGE = "RAIN_GAUGE",
    WATER_TANK = "WATER_TANK",
    TROUGH = "TROUGH",
}

export enum AreaUnit {
    Acre = "acre",
    Sqft = "sqft",
    Sqyd = "sqyd",
    M2 = "m2",
    Hectare = "hectare",
}

export enum LandUse {
    Grazing = "Grazing",
    Cropping = "Cropping",
    Hay = "Hay",
    Yard = "Yard",
    Feedlot = "Feedlot",
    Pen = "Pen",
    Laneway = "Laneway",
    Vegetation = "Vegetation",
    Silvopasture = "Silvopasture",
    Rangeland = "Rangeland",
    Badland = "Badland",
    Wetland = "Wetland",
    ErosionZone = "ErosionZone",
    RestorationZone = "RestorationZone",
    ConversionZone = "ConversionZone",
    NonAgriculture = "NonAgriculture",
}

export enum TagType {
    VisualTag = "VisualTag",
    ElectronicTag = "ElectronicTag",
    CombinedTag = "CombinedTag",
    ManagementTag = "ManagementTag",
    UHFTag = "UHFTag",
    BreedSocietyID = "BreedSocietyID",
    TSUSampleID = "TSUSampleID",
    HerdFlockTag = "HerdFlockTag",
    TrichTag = "TrichTag",
    RegistrationNumber = "RegistrationNumber",
    HealthTag = "HealthTag",
    DNAID = "DNAID"
}

export enum AnimalTagType {
    generic = "generic",
    nlis = "nlis",
    aphis = "aphis",
    bcms = "bcms",
    scot_moves = "scot_moves",
    uk_sheep = "uk_sheep",
    eid = "eid",
    vid = "vid",
    eid_and_vid = "eid_and_vid",
    uhf = "uhf",
    bolus = "bolus",
    slaughter = "slaughter",
    breed_society = "breed_society",
    dna = "dna",
    health = "health",
    trich = "trich",
    group = "group",
    group_management = "group_management",
    management = "management",
}


export enum AnimalTagState {
    Active = "active",
    Removed = " removed",
    Replaced = " replaced"
}

export enum AgeClass {
    Calf = "calf",
    HeiferCalf = "heifer_calf",
    SteerCalf = "steer_calf",
    BullCalf = "bull_calf",
    NonBreedingBullCalf = "non_breeding_bull_calf",
    Weaner = "weaner",
    HeiferWeaner = "heifer_weaner",
    SteerWeaner = "steer_weaner",
    BullWeaner = "bull_weaner",
    NonBreedingBullWeaner = "non_breeding_bull_weaner",
    Yearling = "yearling",
    Heifer = "heifer",
    SpayedHeifer = "spayed_heifer",
    Cow = "cow",
    SpayedCow = "spayed_cow",
    Steer = "steer",
    Bull = "bull",
    NonBreedingBull = "non_breeding_bull",
    NonBreedingMatureBull = "non_breeding_mature_bull",
    Lamb = "lamb",
    EweLamb = "ewe_lamb",
    RamLamb = "ram_lamb",
    WetherLamb = "wether_lamb",
    EweWeaner = "ewe_weaner",
    RamWeaner = "ram_weaner",
    WetherWeaner = "wether_weaner",
    Hogget = "hogget",
    EweHogget = "ewe_hogget",
    RamHogget = "ram_hogget",
    WetherHogget = "wether_hogget",
    MaidenEwe = "maiden_ewe",
    Ewe = "ewe",
    Wether = "wether",
    Ram = "ram",
    Unknown = "unknown"
}

export enum Confidence {
    Accurate = "Accurate",
    Estimate = "Estimate",
    Unknown = "Unknown"
}

export enum DateAccuracy {
    Day = "day",
    Month = "month",
    Year = "year",
    BeforeYear = "before_year"
}

export enum Species {
    Cattle = "cattle",
    Sheep = "sheep",
    Goats = "goats",
    Deer = "deer"
}

export enum Sex {
    Male = "male",
    Female = "female",
    Unspecified = "unspecified",
}

export enum AnimalParentType {
    Dam = "Dam",
    Sire = "Sire",
    Surrogate = "Surrogate",
}

export enum AnimalFate {
    Alive = "Alive",
    Dead = "Dead",
    Sold = "Sold",
    InTransit = "InTransit"
}

export enum FertilityStatus {
    Unknown = "Unknown",
    Fertile = "Fertile",
    Infertile = "Infertile",
    Neutered = "Neutered",
    Cryptorchid = "Cryptorchid",
    NonBreeding = "NonBreeding"
}

export enum ReproductiveStatus {
    Unknown = "Unknown",
    NotCycling = "NotCycling",
    Pregnant = "Pregnant",
    Empty = "Empty",
    Involuting = "Involuting"
}

export enum WeightGainUnit {
    kgPerDay = "kgPerDay",
    gramPerDay = "gramPerDay",
    ozPerDay = "ozPerDay",
    lbPerDay = "lbPerDay"
}

export enum WeightUnit {
    ug = "ug",
    mg = "mg",
    gram = "gram",
    kg = "kg",
    tonne = "tonne",
    oz = "oz",
    lb = "lb",
    ton = "ton",
    stone = "stone",
    longton = "longton"
}

export enum ConditionScoreType {
    bcs5 = "bcs5",
    bcs9 = "bcs9"
}

export enum AnimalUnitType {
    dse = "dse",
    ae = "ae",
    lsu = "lsu",
    au = "au",
    MJPerDay = "MJPerDay"
}
