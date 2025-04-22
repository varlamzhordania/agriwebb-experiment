import json
import os
from datetime import datetime

from django.conf import settings
from celery import shared_task

from .models import Animal, AnimalIdentity, AnimalCharacteristics, Parentage, AnimalState, \
    AnimalRecord, ManagementGroup, Enterprise
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
                    'management_tag': animal_identity.get('management_tag', ''),
                    'brand': animal_identity.get('brand', ''),
                    'tattoo': animal_identity.get('tattoo', ''),
                    'tag_color_catalogue_id': animal_identity.get('tag_color_catalogue_id', ''),
                }
            )

            ## Reminder: check what is the result of birth_date_confidence and make it before creating the characteristics
            # Fetch or create the AnimalCharacteristics
            animal_characteristics = animal['characteristics']
            birth_date_confidence = animal_characteristics['birth_date_confidence']
            characteristics, _ = AnimalCharacteristics.objects.get_or_create(
                birth_date=animal_characteristics['birth_date'],
                defaults={
                    'age_class': animal_characteristics.get('age_class', ''),
                    'birth_date_confidence': '',
                    'birth_date_accuracy': animal_characteristics.get('birth_date_accuracy', ''),
                    'birth_location_id': animal_characteristics.get('birth_location_id', ''),
                    'birth_year': animal_characteristics.get('birth_year', ''),
                    'breed_assessed': animal_characteristics.get('breed_assessed', ''),
                    'visual_color': animal_characteristics.get('visual_color', ''),
                    'sex': animal_characteristics.get('sex', ''),
                    'species_common_name': animal_characteristics.get('species_common_name', ''),

                }
            )

            # Fetch or create the Parentage
            animal_parentage = animal['parentage']
            ## Reminder: fill this section when get the data example

            # Fetch or create the AnimalState
            ## Reminder: this three field are foreignkey, have to be populated before (weights,body_condition_score,animal_units)
            animal_state = animal['state']
            state, _ = AnimalState.objects.get_or_create(
                fate=animal['state']['fate'],
                defaults={
                    'current_location_id': animal_state.get('current_location_id', ''),
                    'on_farm': animal_state.get('on_farm', ''),
                    'on_farm_date': animal_state.get('on_farm_date', ''),
                    'Last_seen': animal_state.get('Last_seen', ''),
                    'days_reared': animal_state.get('days_reared', ''),
                    'off_farm_date': animal_state.get('off_farm_date', ''),
                    'disposal_method': animal_state.get('disposal_method', ''),
                    'fate': animal_state.get('fate', ''),
                    'fertility_status': animal_state.get('fertility_status', ''),
                    'rearing_rank': animal_state.get('rearing_rank', ''),
                    'reproductive_status': animal_state.get('reproductive_status', ''),
                    'status_date': animal_state.get('status_date', ''),
                    'withholding_date_meat': animal_state.get('withholding_date_meat', ''),
                    'withholding_date_export': animal_state.get('withholding_date_export', ''),
                    'withholding_date_organic': animal_state.get('withholding_date_organic', ''),
                    'weaned': animal_state.get('weaned', ''),
                    'offspring_count': animal_state.get('offspring_count', ''),
                    # 'weights': animal_state.get('weights', ''),
                    # 'body_condition_score': animal_state.get('body_condition_score', ''),
                    'body_condition_score_date': animal_state.get('body_condition_score_date', ''),
                    # 'animal_units': animal_state.get('animal_units', ''),
                    'has_had_offspring': animal_state.get('has_had_offspring', ''),
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
