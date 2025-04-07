export interface Record {
    recordId: string;
    recordType: RecordType;
    observationDate: string;
    sessionId?: string;
}

export enum RecordType {
    AnimalTreatment = "animalTreatment",
    Feed = "feed",
    LocationChanged = "locationChanged",
    PregnancyScan = "pregnancyScan",
    Score = "score",
    Weigh = "weigh",
}
