import json
import os
from datetime import datetime

from django.conf import settings
from celery import shared_task
from django.db import transaction

from .models import Animal, AnimalIdentity, AnimalCharacteristics, Parentage, AnimalState, \
    AnimalRecord, ManagementGroup, Enterprise, Farm, Address, GeoPoint, MapFeature, GeoFeature, \
    CapacityAlert, Capacity, Field, \
    ExternalIdentifier
from .agriwebb import AgriWebb


@shared_task
def fetch_and_store_animals_data_to_json(
        token_id,
        farm_id,
        filter=None,
        sort=None,
        limit=None,
        skip=None,
        observation_date=None,
        capabilities=None
):
    """
    Fetches the animal data from AgriWebb API and stores it in a JSON file for observation.
    """
    try:
        agriwebb = AgriWebb()

        animals_data = agriwebb.animals(
            token_id,
            farm_id,
            filter=filter,
            sort=sort,
            limit=limit,
            skip=skip,
            observation_date=observation_date,
            capabilities=capabilities
        )

        animals_json_data = animals_data['animals']

        filename = f"animals_observation_{farm_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        folder_path = os.path.join(settings.BASE_DIR, "agriwebb", "data")

        os.makedirs(folder_path, exist_ok=True)

        path = os.path.join(folder_path, filename)

        with open(path, 'w') as json_file:
            json.dump(animals_json_data, json_file, indent=4)

        return f"Successfully fetched and stored animal data for farm {farm_id} in a JSON file."

    except Exception as e:
        return f"An error occurred while fetching and storing animals data: {e}"


@shared_task
def fetch_and_store_animals_data(
        token_id,
        farm_id,
        filter=None,
        sort=None,
        limit=None,
        skip=None,
        observation_date=None,
        capabilities=None
):
    """
    Fetches the animal data from AgriWebb API and stores it in the Django model.
    """
    try:
        agriwebb = AgriWebb()

        animals_data = agriwebb.animals(
            token_id,
            farm_id,
            filter=filter,
            sort=sort,
            limit=limit,
            skip=skip,
            observation_date=observation_date,
            capabilities=capabilities
        )
        with transaction.atomic():
            for animal in animals_data['animals']:

                ## Reminder: check what is the result of tags and make them before creating animal identity to set them
                # Fetch or create the AnimalIdentity
                animal_identity = animal['identity']
                tags = animal_identity['tags']
                identity, _ = AnimalIdentity.objects.get_or_create(
                    eid=animal_identity['eid'],
                    defaults={
                        'name': animal_identity['name'],
                        'vid': animal_identity.get('vid', ''),
                        'management_tag': animal_identity.get('managementTag', ''),
                        'brand': animal_identity.get('brand', ''),
                        'tattoo': animal_identity.get('tattoo', ''),
                        'tag_color_catalogue_id': animal_identity.get('tagColorCatalogueId', ''),
                    }
                )

                ## Reminder: check what is the result of birth_date_confidence and make it before creating the characteristics
                # Fetch or create the AnimalCharacteristics
                animal_characteristics = animal['characteristics']
                birth_date_confidence = animal_characteristics['birthDateConfidence']
                characteristics, _ = AnimalCharacteristics.objects.get_or_create(
                    birth_date=animal_characteristics['birthDate'],
                    defaults={
                        'age_class': animal_characteristics.get('ageClass', ''),
                        'birth_date_confidence': '',
                        'birth_date_accuracy': animal_characteristics.get('birthDateAccuracy', ''),
                        'birth_location_id': animal_characteristics.get('birthLocationId', ''),
                        'birth_year': animal_characteristics.get('birthYear', ''),
                        'breed_assessed': animal_characteristics.get('breedAssessed', ''),
                        'visual_color': animal_characteristics.get('visualColor', ''),
                        'sex': animal_characteristics.get('sex', ''),
                        'species_common_name': animal_characteristics.get('speciesCommonName', ''),

                    }
                )

                # Fetch or create the Parentage
                animal_parentage = animal['parentage']
                ## Reminder: fill this section when get the data example

                # Fetch or create the AnimalState
                ## Reminder: this three field are foreignkey, have to be populated before (weights,body_condition_score,animal_units)
                animal_state = animal['state']
                state, _ = AnimalState.objects.get_or_create(
                    defaults={
                        'current_location_id': animal_state.get('currentLocationId', ''),
                        'on_farm': animal_state.get('onFarm', ''),
                        'on_farm_date': animal_state.get('onFarmDate', ''),
                        'Last_seen': animal_state.get('LastSeen', ''),
                        'days_reared': animal_state.get('daysReared', ''),
                        'off_farm_date': animal_state.get('offFarmDate', ''),
                        'disposal_method': animal_state.get('disposalMethod', ''),
                        'fate': animal_state.get('fate', ''),
                        'fertility_status': animal_state.get('fertilityStatus', ''),
                        'rearing_rank': animal_state.get('rearingRank', ''),
                        'reproductive_status': animal_state.get('reproductiveStatus', ''),
                        'status_date': animal_state.get('statusDate', ''),
                        'withholding_date_meat': animal_state.get('withholdingDateMeat', ''),
                        'withholding_date_export': animal_state.get('withholdingDateExport', ''),
                        'withholding_date_organic': animal_state.get('withholdingDateOrganic', ''),
                        'weaned': animal_state.get('weaned', ''),
                        'offspring_count': animal_state.get('offspringCount', ''),
                        # 'weights': animal_state.get('weights', ''),
                        # 'body_condition_score': animal_state.get('bodyConditionScore', ''),
                        'body_condition_score_date': animal_state.get('bodyConditionScoreDate', ''),
                        # 'animal_units': animal_state.get('animalUnits', ''),
                        'has_had_offspring': animal_state.get('hasHadOffspring', ''),
                    }
                )

                # Fetch or create the Enterprise
                animal_enterprise = animal['enterprise']
                enterprise, _ = Enterprise.objects.get_or_create(
                    enterprise_id=animal['enterpriseId'],
                    defaults={
                        'name': animal_enterprise.get('name', ''),
                        'farm_id': animal_enterprise.get('farmId', ''),
                    }
                )

                # Fetch or create the ManagementGroup
                ## Reminder: have to make the enterprise before and set the id here
                animal_management_group = animal['managementGroup']
                management_group, _ = ManagementGroup.objects.get_or_create(
                    management_group_id=animal_management_group.get('managementGroupId', ''),
                    defaults={
                        'enterprise_id': animal_management_group.get('enterpriseId', ''),
                        'farm_id': animal_management_group.get('farmId', ''),
                        'name': animal_management_group.get('name', ''),
                        'species': animal_management_group.get('species', ''),
                        'type': animal_management_group.get('type', ''),
                        'enterprise': enterprise.id,
                    }
                )

                # Create or update the Animal model
                animal_obj, created = Animal.objects.update_or_create(
                    animal_id=animal['animalId'],
                    defaults={
                        'identity': identity,
                        'age_class': animal.get('ageClass', ''),
                        'characteristics': characteristics,
                        # 'parentage': parentage,
                        'management_group': management_group,
                        'enterprise': enterprise,
                        'farm_id': farm_id,
                        'state': state,
                        'purchased_from': animal.get('purchasedFrom', ''),
                        'purchase_location_id': animal.get('purchaseLocationId', ''),
                        'creation_record_group_id': animal.get('creationRecordGroupId', ''),
                        'creation_record_id': animal.get('creationRecordId', ''),
                        'birthing_record_id': animal.get('birthingRecordId', ''),
                        'purchase_record_id': animal.get('purchaseRecordId', ''),
                        'sale_record_id': animal.get('saleRecordId', ''),
                        'observation_date': animal.get('_observationDate', ''),
                    }
                )

                if 'records' in animal:
                    for record in animal['records']:
                        record_obj, _ = AnimalRecord.objects.get_or_create(
                            record_id=record['recordId'],
                            defaults={
                                'record_type': record.get('recordType', ''),
                                'observation_date': record.get('observationDate', ''),
                                'session_id': record.get('sessionId', ''),
                            }
                        )
                        animal_obj.records.add(record_obj)

        return f"Successfully fetched and stored animal data for farm {farm_id}"
    except Exception as e:
        return f"An error occurred while fetching and storing animals data: {e}"


@shared_task
def fetch_and_store_farm_data_to_json(token_id, farm_ids=None):
    """
    Fetches farm data from the AgriWebb API and stores it in a JSON file.
    """
    try:
        agriwebb = AgriWebb()

        farms_data = agriwebb.farms(token_id, farm_ids=farm_ids)

        farms_json_data = farms_data['farms']

        filename = f"farms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        folder_path = os.path.join(settings.BASE_DIR, "agriwebb", "data")

        os.makedirs(folder_path, exist_ok=True)

        path = os.path.join(folder_path, filename)

        with open(path, 'w') as json_file:
            json.dump(farms_json_data, json_file, indent=4)

        return f"Successfully fetched and stored farm data for farm(s): {farm_ids} in a JSON file."

    except Exception as e:
        return f"An error occurred while fetching and storing farm data: {e}"


@shared_task
def fetch_and_store_farm_data(token_id, farm_ids=None):
    """
    Fetches farm data from the AgriWebb API and stores it in the Django models.
    """
    try:
        agriwebb = AgriWebb()

        farms_data = agriwebb.farms(token_id, farm_ids=farm_ids)

        with transaction.atomic():
            for farm in farms_data['farms']:
                if farm.get('address'):
                    address_data = farm['address']
                    geo_point = address_data.get('location', {})
                    geo_point_obj, _ = GeoPoint.objects.update_or_create(
                        lat=geo_point.get('lat', None),
                        long=geo_point.get('long', None)
                    )

                    address_obj, _ = Address.objects.update_or_create(
                        country=address_data.get('country', ''),
                        postcode=address_data.get('postcode', ''),
                        town=address_data.get('town', ''),
                        state=address_data.get('state', ''),
                        address1=address_data.get('address1', ''),
                        address2=address_data.get('address2', ''),
                        location=geo_point_obj,
                    )
                else:
                    address_obj = None

                farm_obj, created = Farm.objects.update_or_create(
                    agri_id=farm['id'],
                    defaults={
                        'name': farm.get('name', ''),
                        'time_zone': farm.get('timeZone', ''),
                        'address': address_obj,
                        'fields': farm.get('fields', []),
                    }
                )

                map_features_data = farm.get('mapFeatures', [])
                for map_feature in map_features_data:
                    geometry_data = map_feature.get('geometry', {})

                    geometry_obj, _ = GeoFeature.objects.update_or_create(
                        type=geometry_data.get('type', ''),
                        coordinates=geometry_data.get('coordinates', ''),
                    )

                    alert_data = map_feature.get('alert', {})

                    alert_obj, _ = CapacityAlert.objects.update_or_create(
                        critical=alert_data.get('critical', ''),
                        warning=alert_data.get('warning', ''),
                    )

                    capacity_data = map_feature.get('capacity', {})

                    capacity_obj, _ = Capacity.objects.update_or_create(
                        mode=capacity_data.get('mode', ''),
                        value=capacity_data.get('value', ''),
                        unit=capacity_data.get('unit', ''),
                    )

                    map_feature_obj, _ = MapFeature.objects.update_or_create(
                        uu_id=map_feature.get('id', ''),
                        defaults={
                            "name": map_feature.get('name', ''),
                            "description": map_feature.get('description', ''),
                            "farm_id": map_feature.get('farmId', ''),
                            "type": map_feature.get('type', ''),
                            "identifier": map_feature.get('identifier', ''),
                            "geometry": geometry_obj,
                            "alert": alert_obj,
                            "capacity": capacity_obj,
                        }
                    )
                    farm_obj.map_features.add(map_feature_obj)

                fields_data = farm.get('fields', [])

                for field in fields_data:
                    location_data = field.get('location', {})
                    location_obj, _ = GeoPoint.objects.update_or_create(
                        lat=location_data.get('lat', ''),
                        long=location_data.get('long', ''),
                    )

                    geometry_data = field.get('geometry', {})

                    geometry_obj, _ = GeoFeature.objects.update_or_create(
                        type=geometry_data.get('type', ''),
                        coordinates=geometry_data.get('coordinates', ''),
                    )

                    field_obj, _ = Field.objects.update_or_create(
                        agri_id=field.get('agriId'),
                        defaults={
                            'farm_id': field.get('farmId', ''),
                            'name': field.get('name', ''),
                            'total_area': field.get('totalArea', 0),
                            'grazable_area': field.get('grazableArea', 0),
                            'unit': field.get('unit', 'hectare'),
                            'land_use': field.get('landUse', ''),
                            'crop_type': field.get('cropType', ''),
                            'creation_date': field.get('creationDate', ''),
                            'last_modified_date': field.get('lastModifiedDate', ''),
                            'location': location_obj,
                            'geometry': geometry_obj,
                        }
                    )

                    identifiers_data = field.get('identifiers', [])

                    for identifier in identifiers_data:
                        identifier_obj, _ = ExternalIdentifier.objects.update_or_create(
                            type=identifier.get('type', ''),
                            value=identifier.get('value', []),
                        )
                        field_obj.identifiers.add(identifier_obj)

                    farm_obj.fields.add(field_obj)

                identifier_data = farm.get('identifiers', [])

                for identifier in identifier_data:
                    external_identifier_obj, _ = ExternalIdentifier.objects.update_or_create(
                        type=identifier.get('type', ''),
                        value=identifier.get('value', []),
                    )
                    farm_obj.identifiers.add(external_identifier_obj)

        return f"Successfully fetched and stored farm data for farm(s): {farm_ids}"

    except Exception as e:
        return f"An error occurred while fetching and storing farm data: {e}"
