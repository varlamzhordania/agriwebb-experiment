import json
import os
from datetime import datetime

from django.conf import settings
from django.db import transaction
from celery import shared_task

from .helpers import populate_animal
from .models import Farm, Address, GeoPoint, MapFeature, GeoFeature, CapacityAlert, Capacity, Field, \
    ExternalIdentifier, AnimalCount

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
                populate_animal(animal, farm_id)

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


@shared_task
def fetch_and_store_animals_with_count_data(
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
    Fetches the animal data with count from AgriWebb API and stores it in the Django model.
    """
    try:
        agriwebb = AgriWebb()

        animals_data = agriwebb.animals_with_count(
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

            animals_with_count = animals_data['animalsWithCount']
            animals_list = animals_with_count['animals']
            non_paged_count = animals_with_count.get('nonPagedCount', 0)

            animal_count = AnimalCount.objects.create(
                farm_id=farm_id,
                non_paged_count=non_paged_count,
            )

            for animal_data in animals_list:
                animal_obj = populate_animal(animal_data, farm_id)
                animal_count.animals.add(animal_obj)

        return f"Successfully fetched and stored animals with count data for farm {farm_id} in the AnimalCount model."

    except Exception as e:
        return f"An error occurred while fetching and storing animals with count data: {e}"
