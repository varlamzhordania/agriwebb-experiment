import {CoordinatesScalar, ID, Timestamp} from "./scalers";
import {AreaUnit, CapacityMode, DepthUnit, GeoType, LandUse, MapFeatureType} from "./enums";


interface Farm {
    id: ID;
    name: string;
    address: Address;
    timeZone: string;
    mapFeatures: MapFeature[];
    fields: Field[];
    identifiers: ExternalIdentifier[];
}

type Address = {
    address1: string;
    address2: string;
    country: string;
    postcode: string;
    town: string;
    state: string;
    location: GeoPoint;
};

interface MapFeature {
    id: ID;
    name: string;
    description: string;
    geometry: GeoFeature;
    farmId: ID;
    type: MapFeatureType;
    alert: CapacityAlert;
    capacity: Capacity;
    identifier: string;
}

type GeoPoint = {
    lat: number;  // Latitude in decimal degrees
    long: number; // Longitude in decimal degrees
};

interface GeoFeature {
    type: GeoType;
    coordinates: CoordinatesScalar;
}

interface CapacityAlert {
    critical: number;
    warning: number;
}

interface Capacity {
    mode: CapacityMode;
    value: number;
    unit: DepthUnit;
}

interface Field {
    id: ID;
    creationDate: Timestamp;
    lastModifiedDate: Timestamp;
    name: string;
    location: GeoPoint;
    geometry: GeoFeature;
    farmId: ID;
    totalArea: number;
    grazableArea: number;
    unit: AreaUnit;
    landUse: LandUse;
    cropType: string;
    identifiers: ExternalIdentifier[];
}

interface ExternalIdentifier {
    type: string;
    value: string[];
}
