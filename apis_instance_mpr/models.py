from apis_core.generic.abc import GenericModel
from apis_core.apis_entities.models import AbstractEntity
from apis_core.relations.models import Relation
from django_json_editor_field.fields import JSONEditorField
from django_interval.fields import FuzzyDateParserField
from django.db import models
from django.utils.translation import gettext_lazy as _
from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group

# generic models
# labels such as mpr_reference to be imported in the collections


class Funktion(GenericModel):
    ...


# Entities


class LabelAlternativeLabelsEntity(AbstractEntity):
    label = models.CharField(max_length=255, blank=True)
    alternative_labels = JSONEditorField()

    class Meta:
        abstract = True


class Delegation(LabelAlternativeLabelsEntity):
    ...


class Nobility(LabelAlternativeLabelsEntity):
    ...


class Denomination(LabelAlternativeLabelsEntity):
    ...


class OrderOfDistinction(LabelAlternativeLabelsEntity):
    kind = models.CharField(choices=['military', 'civil', 'religious'])  # TODO: use choices from collection


class Person(E21_Person, LabelAlternativeLabelsEntity):
    ...


class Place(E53_Place, LabelAlternativeLabelsEntity):
    ...


class Institution(E74_Group, LabelAlternativeLabelsEntity):
    ...


class Event(LabelAlternativeLabelsEntity):
    begin = FuzzyDateParserField(
        max_length=255, blank=True, null=True, verbose_name=_("Begin")
    )
    end = FuzzyDateParserField(
        max_length=255, blank=True, null=True, verbose_name=_("End")
    )


# Relations


class BeginEndRelation(Relation):
    begin = FuzzyDateParserField(
        max_length=255, blank=True, null=True, verbose_name=_("Begin")
    )
    end = FuzzyDateParserField(
        max_length=255, blank=True, null=True, verbose_name=_("End")
    )

    class Meta:
        abstract = True


class NotesReferencesRelation(Relation):
    notes = models.TextField(null=True)
    references = models.TextField(null=True)  # use Zotero

    class Meta:
        abstract = True


class PersonHasFunctionInInstitution(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = Institution
    funktion = models.ForeignKey(Funktion)


class PersonIsPartOfDelegation(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = Delegation


class PersonInstructsInstitution(Relation):
    subj = Person
    obj = Institution
    date = FuzzyDateParserField(
        max_length=255, blank=True, null=True, verbose_name=_("Date")
    )


class InstitutionIsChildInstitutionOf(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Institution
    obj = Institution


class PersonIsChildOf(Relation):
    subj = Person
    obj = Person


class PersonIsSiblingOf(Relation):
    subj = Person
    obj = Person


class PersonIsSpouseOf(Relation):
    subj = Person
    obj = Person


class PersonIsInSocialRelationWith(Relation):
    subj = Person
    obj = Person
    comment = models.TextField()


class PersonHasChangeInNobility(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = Nobility


class PersonHasDenomination(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = Denomination


class PersonHasOrderOfDistinction(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = OrderOfDistinction


class PersonDiesIn(Relation):
    subj = Person
    obj = Place


class PersonIsBornIn(Relation):
    subj = Person
    obj = Place


class PlaceIsLocatedInPlace(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Place
    obj = Place


class PlaceIsCloseToPlace:
    # to be used with places that cant be located with long/lat exactly
    # only used with one place so far, maybe skip for now and go with comments
    subj = Place
    obj = Place


class PlaceIsSuccessorPlaceOf(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Place
    obj = Place


class InstitutionGovernsPlace(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Institution
    obj = Place


class InstitutionIsLocatedIn(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Institution
    obj = Place


class PersonIsCommanderOfPlace(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Person
    obj = Place
    kind = models.CharField(choices=[])  # TODO: use choices from collection


class PersonWorksInPlace(BeginEndRelation, NotesReferencesRelation, Relation):
    # to be used if someone works only for a short time in a place
    # maybe add FK to Delegation that person was member of
    subj = Person
    obj = Place
    comment = models.TextField()


class EventTakesPlaceIn(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Event
    obj = Place


class InstitutionIsSuccessorInstitutionOf(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Institution
    obj = Institution
    kind = models.CharField(choices=[])  # TODO: use choices from collection


class InstitutionHasRelationToInstitution(BeginEndRelation, NotesReferencesRelation, Relation):
    subj = Institution
    obj = Institution
    kind = models.CharField(choices=[])  # TODO: use choices from collection
