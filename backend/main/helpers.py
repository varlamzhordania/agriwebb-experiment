from .models import Animal, AnimalIdentity, AnimalCharacteristics, Parentage, AnimalState, \
    AnimalRecord, ManagementGroup, Enterprise, AnimalTag, DateConfidence, AnimalWeightSummary, \
    WeightGain, Weight, ConditionScore, AnimalUnit, GeneticParent, ParentAnimalIdentity, Surrogate, \
    AnimalParent


def populate_animal(animal, farm_id):
    """
    Populates the Animal model from the given animal data.
    """

    animal_id = animal.get('animalId', '')
    animal_identity = animal.get('identity', {})
    tags_data = animal_identity.get('tags', [])
    identity, _ = AnimalIdentity.objects.update_or_create(
        animal_id=animal_id,
        defaults={
            'name': animal_identity.get('name', ''),
            'eid': animal_identity.get('eid', ''),
            'vid': animal_identity.get('vid', ''),
            'management_tag': animal_identity.get('managementTag', ''),
            'brand': animal_identity.get('brand', ''),
            'tattoo': animal_identity.get('tattoo', ''),
            'tag_color_catalogue_id': animal_identity.get(
                'tagColorCatalogueId',
                ''
            ),
        }
    )
    for tag in tags_data:
        tag_obj, _ = AnimalTag.objects.update_or_create(
            agri_id=tag.get('id'),
            defaults={
                "eid": tag.get('eid', ''),
                "vid": tag.get('vid', ''),
                "management_tag": tag.get('managementTag', ''),
                "uhf_eid": tag.get('uhfEid', ''),
                "dna_id": tag.get('dnaId', ''),
                "registration_number": tag.get('registrationNumber', ''),
                "breed_society_id": tag.get('breedSocietyId', ''),
                "health_id": tag.get('healthId', ''),
                "tag_id": tag.get('tagId', ''),
                "tag_color_catalogue_id": tag.get('tagColorCatalogueId', ''),
                "type": tag.get('type', ''),
                "state": tag.get('state', ''),
                "removal_date": tag.get('removalDate', ''),
                "replacement_date": tag.get('replacementDate', ''),
            }
        )
        identity.tags.add(tag_obj)

    animal_characteristics = animal.get('characteristics', {})
    birth_date_confidence_data = animal_characteristics.get('birthDateConfidence', {})

    birth_date_confidence_obj, _ = DateConfidence.objects.get_or_create(
        year=birth_date_confidence_data.get('year', ''),
        month=birth_date_confidence_data.get('month', ''),
        day=birth_date_confidence_data.get('day', ''),
    )

    characteristics, _ = AnimalCharacteristics.objects.update_or_create(
        animal_id=animal_id,
        defaults={
            'age_class': animal_characteristics.get('ageClass', ''),
            'birth_date': animal_characteristics.get('birthDate'),
            'birth_date_confidence': birth_date_confidence_obj,
            'birth_date_accuracy': animal_characteristics.get(
                'birthDateAccuracy',
                ''
            ),
            'birth_location_id': animal_characteristics.get('birthLocationId', ''),
            'birth_year': animal_characteristics.get('birthYear', ''),
            'breed_assessed': animal_characteristics.get('breedAssessed', ''),
            'visual_color': animal_characteristics.get('visualColor', ''),
            'sex': animal_characteristics.get('sex', ''),
            'species_common_name': animal_characteristics.get(
                'speciesCommonName',
                ''
            ),

        }
    )

    animal_parentage = animal.get('parentage', {})
    sires_data = animal_parentage.get('sires', [])
    dams_data = animal_parentage.get('dams', [])
    parentage = Parentage()

    for dam in dams_data:
        parent_animal_identity_data = dam.get('parentAnimalIdentity', {})
        parent_animal_id = dam.get('parentAnimalId')
        parent_animal_identity_obj, _ = ParentAnimalIdentity.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'eid': parent_animal_identity_data.get('eid', ''),
                'vid': parent_animal_identity_data.get('vid', ''),
                'name': parent_animal_identity_data.get('name', ''),
            }
        )

        dam_obj, _ = GeneticParent.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'parent_animal_identity': parent_animal_identity_obj,
                'parent_type': dam.get('parentType', AnimalParent.AnimalParentType.DAM),
            }
        )
        parentage.dams.add(dam_obj)

    for sire in sires_data:
        parent_animal_identity_data = sire.get('parentAnimalIdentity', {})
        parent_animal_id = sire.get('parentAnimalId')
        parent_animal_identity_obj, _ = ParentAnimalIdentity.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'eid': parent_animal_identity_data.get('eid', ''),
                'vid': parent_animal_identity_data.get('vid', ''),
                'name': parent_animal_identity_data.get('name', ''),
            }
        )

        sire_obj, _ = GeneticParent.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'parent_animal_identity': parent_animal_identity_obj,
                'parent_type': sire.get('parentType', AnimalParent.AnimalParentType.SIRE),
            }
        )
        parentage.sires.add(sire_obj)

    surrogate_data = animal_parentage.get('surrogate', {})
    if surrogate_data:
        parent_animal_identity_data = surrogate_data.get('parentAnimalIdentity', {})
        parent_animal_id = surrogate_data.get('parentAnimalId')

        parent_animal_identity_obj, _ = ParentAnimalIdentity.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'eid': parent_animal_identity_data.get('eid', ''),
                'vid': parent_animal_identity_data.get('vid', ''),
                'name': parent_animal_identity_data.get('name', ''),
            }
        )

        surrogate_obj, _ = Surrogate.objects.update_or_create(
            parent_animal_id=parent_animal_id,
            defaults={
                'parent_animal_identity': parent_animal_identity_obj,
                'parent_type': surrogate_data.get('parentType', AnimalParent.AnimalParentType.UNKNOWN),
            }
        )
        parentage.surrogate = surrogate_obj

    parentage.save()

    animal_state = animal.get('state', {})
    weights_data = animal_state.get('weights', {})
    weights_live_average_daily_gain_data = weights_data.get('liveAverageDailyGain', {})

    weights_live_average_daily_gain_obj = WeightGain.objects.create(
        unit=weights_live_average_daily_gain_data.get('unit', ''),
        value=weights_live_average_daily_gain_data.get('value', ''),
    )

    weights_overall_average_daily_gain = weights_data.get('overallAverageDailyGain', {})

    weights_overall_average_daily_gain_obj = WeightGain.objects.create(
        unit=weights_overall_average_daily_gain.get('unit', ''),
        value=weights_overall_average_daily_gain.get('value', ''),
    )

    weights_assumed_average_daily_gain_gain = weights_data.get(
        'assumedAverageDailyGain',
        {}
    )

    weights_assumed_average_daily_gain_gain_obj = WeightGain.objects.create(
        unit=weights_assumed_average_daily_gain_gain.get('unit', ''),
        value=weights_assumed_average_daily_gain_gain.get('value', ''),
    )

    weights_live_weight = weights_data.get('liveWeight', {})

    weights_live_weight_obj = Weight.objects.create(
        unit=weights_live_weight.get('unit', ''),
        value=weights_live_weight.get('value', ''),
    )

    weights_estimated_weight = weights_data.get('estimatedWeight', {})

    weights_estimated_weight_obj = Weight.objects.create(
        unit=weights_estimated_weight.get('unit', ''),
        value=weights_estimated_weight.get('value', ''),
    )

    weights_obj, create = AnimalWeightSummary.objects.update_or_create(
        live_average_daily_gain=weights_live_average_daily_gain_obj,
        overall_average_daily_gain=weights_overall_average_daily_gain_obj,
        assumed_average_daily_gain=weights_assumed_average_daily_gain_gain_obj,
        live_weight_date=weights_data.get('liveWeightDate', ''),
        live_weight=weights_live_weight_obj,
        estimated_weight=weights_estimated_weight_obj,
    )

    body_condition_score_data = animal_state.get('bodyConditionScore', {})

    body_condition_score_obj = ConditionScore.objects.create(
        unit=body_condition_score_data.get('unit', ''),
        value=body_condition_score_data.get('value', ''),
    )

    animal_units_data = animal_state.get('animalUnits', {})

    animal_units_obj = AnimalUnit.objects.create(
        unit=animal_units_data.get('unit', ''),
        value=animal_units_data.get('value', ''),
    )

    state, _ = AnimalState.objects.update_or_create(
        animal_id=animal_id,
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
            'withholding_date_export': animal_state.get(
                'withholdingDateExport',
                ''
            ),
            'withholding_date_organic': animal_state.get(
                'withholdingDateOrganic',
                ''
            ),
            'weaned': animal_state.get('weaned', ''),
            'offspring_count': animal_state.get('offspringCount', ''),
            'weights': weights_obj,
            'body_condition_score': body_condition_score_obj,
            'body_condition_score_date': animal_state.get(
                'bodyConditionScoreDate',
                ''
            ),
            'animal_units': animal_units_obj,
            'has_had_offspring': animal_state.get('hasHadOffspring', ''),
        }
    )

    animal_enterprise = animal.get('enterprise')
    enterprise, _ = Enterprise.objects.update_or_create(
        enterprise_id=animal_enterprise.get('enterpriseId'),
        defaults={
            'name': animal_enterprise.get('name', ''),
            'farm_id': animal_enterprise.get('farmId', farm_id),
        }
    )

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

    animal_obj, created = Animal.objects.update_or_create(
        animal_id=animal['animalId'],
        defaults={
            'identity': identity,
            'age_class': animal.get('ageClass', ''),
            'characteristics': characteristics,
            'parentage': parentage,
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

    return animal_obj
