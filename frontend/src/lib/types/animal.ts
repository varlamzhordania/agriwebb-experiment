import {Record,RecordType} from "./record";
import {ID, Int, Timestamp} from "./scalers";
import {
    AgeClass,
    AnimalFate, AnimalParentType,
    AnimalTagState, AnimalUnitType, ConditionScoreType,
    Confidence,
    DateAccuracy,
    FertilityStatus, ReproductiveStatus,
    Sex,
    Species,
    TagType, WeightGainUnit, WeightUnit
} from "./enums";

interface Animal {
    animalId: ID;
    identity?: AnimalIdentity;
    ageClass?: AgeClass;
    characteristics?: AnimalCharacteristics;
    parentage?: Parentage;
    managementGroupId?: string;
    managementGroup?: ManagementGroup;
    enterpriseId?: string;
    enterprise?: Enterprise;
    state?: AnimalState;
    records?: AnimalRecord[];
    farmId?: string;
    purchasedFrom?: string;
    purchaseLocationId?: string;
    creationRecordGroupId?: string;
    creationRecordId?: string;
    birthingRecordId?: string;
    purchaseRecordId?: string;
    saleRecordId?: string;
    _observationDate?: Timestamp;
}

interface AnimalsWithCount {
  nonPagedCount: Int
  animals: [Animal]
}

interface AnimalIdentity {
    name?: string;
    eid?: string;
    vid?: string;
    managementTag?: string;
    brand?: string;
    tattoo?: string;
    tags?: AnimalTag[];
    tagColorCatalogueId?: string;
}

interface AnimalTag {
    id?: string;
    eid?: string;
    vid?: string;
    managementTag?: string;
    uhfEid?: string;
    dnaId?: string;
    registrationNumber?: string;
    breedSocietyId?: string;
    healthId?: string;
    tagId?: string;
    tagColorCatalogueId?: string;
    type?: TagType;
    state?: AnimalTagState;
    removalDate?: number;
    replacementDate?: number;
}

interface AnimalCharacteristics {
    ageClass?: AgeClass;
    birthDate?: number;
    birthDateConfidence?: DateConfidence;
    birthDateAccuracy?: DateAccuracy;
    birthLocationId?: string;
    birthYear?: number;
    breedAssessed?: string;
    visualColor?: string;
    sex?: Sex;
    speciesCommonName?: Species;
}

interface DateConfidence {
    year: Confidence
    month: Confidence
    day: Confidence
}

interface Parent {
    parentAnimalId?: string;
    parentAnimalIdentity?: ParentAnimalIdentity;
    parentType?: AnimalParentType;
}

interface ParentAnimalIdentity {
    eid?: string;
    vid?: string;
    name?: string;
}

class GeneticParent implements Parent {
    parentAnimalId?: string;
    parentAnimalIdentity?: ParentAnimalIdentity;
    parentType?: AnimalParentType;
}

class Surrogate implements Parent {
    parentAnimalId?: string;
    parentAnimalIdentity?: ParentAnimalIdentity;
    parentType?: AnimalParentType;
}

interface Parentage {
    dams?: GeneticParent[];
    sires?: GeneticParent[];
    surrogate?: Surrogate;
}

interface ManagementGroup {
    managementGroupId: string;
    enterpriseId?: string;
    farmId?: string;
    name?: string;
    species?: Species;
    type?: string;
    enterprise?: Enterprise;
}

interface Enterprise {
    enterpriseId: string;
    name?: string;
    farmId?: string;
}

interface AnimalState {
    currentLocationId?: string;
    onFarm?: boolean;
    onFarmDate?: Timestamp;
    lastSeen?: Timestamp;
    daysReared?: number;
    offFarmDate?: Timestamp;
    disposalMethod?: string;
    fate?: AnimalFate;
    fertilityStatus?: FertilityStatus;
    rearingRank?: number;
    reproductiveStatus?: ReproductiveStatus;
    statusDate?: Timestamp;
    withholdingDateMeat?: Timestamp;
    withholdingDateExport?: Timestamp;
    withholdingDateOrganic?: Timestamp;
    weaned?: boolean;
    offspringCount?: number;
    weights?: AnimalWeightSummary;
    bodyConditionScore?: ConditionScore;
    bodyConditionScoreDate?: Timestamp;
    animalUnits?: AnimalUnit;
    hasHadOffspring?: boolean;
}

interface AnimalWeightSummary {
    liveAverageDailyGain?: WeightGain;
    overallAverageDailyGain?: WeightGain;
    assumedAverageDailyGain?: WeightGain;
    liveWeightDate?: Timestamp;
    liveWeight?: Weight;
    estimatedWeight?: Weight;
}

interface WeightGain {
    unit: WeightGainUnit;
    value: number;
}

interface Weight {
    unit: WeightUnit;
    value: number;
}

interface ConditionScore {
    unit: ConditionScoreType;
    value: number;
}

interface AnimalUnit {
    unit: AnimalUnitType;
    value: number;
}

class AnimalRecord implements Record {
    observationDate: string;
    recordId: string;
    recordType: RecordType;
    sessionId: string;
}


