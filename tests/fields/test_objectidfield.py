"""
test_objectidfield
------------------

Tests DRF serialization for Djongo ObjectID type fields
"""

from bson import ObjectId
from bson.errors import InvalidId

from django.test import TestCase
from rest_framework.exceptions import ValidationError
import pytest

from rest_meets_djongo.fields import ObjectIdField


class TestObjectIDField(TestCase):

    field = ObjectIdField()

    def test_to_internal_value(self):
        """
        For object ID fields, the internal value should be an ObjectID
        object, appropriately formatted w/ MongoDB's setup.

        We use an ObjectID key generated by Djongo previously, utilizing its
        ObjectIDField (for models) to do so
        """
        obj_key = "5d08078b1f7eb051eafe2390"

        ref_obj = ObjectId(obj_key)
        new_obj = self.field.to_internal_value(obj_key)

        assert new_obj.__eq__(ref_obj)

    def test_to_representation(self):
        """
        Confirm that object ID objects can still be reconstructed once
        serialized. This allows for them to be used as primary key queries
        by DRF (I.E. '/students/5d08078b1f7eb051eafe2390')
        """
        ref_obj = ObjectId()

        ref_id = ref_obj.__str__()
        obj_id = self.field.to_representation(ref_obj)

        assert ref_id == obj_id

    def test_conversion_equivalence(self):
        """
        Confirm that serialization and de-serialization of ObjectIDs is a
        lossless operation (and thus its use won't create unexpected
        behaviours) by default.
        """
        obj = ObjectId()

        obj_repr = self.field.to_representation(obj)
        new_obj = self.field.to_internal_value(obj_repr)

        assert obj.__eq__(new_obj)

    def test_invalid_rejection(self):
        """
        Confirm that invalid ObjectID tags are rejected when attempting to
        serialize them
        """
        bad_key = "tooshort"

        with pytest.raises(ValidationError):
            self.field.to_internal_value(bad_key)

        not_a_key = dict()

        with pytest.raises(InvalidId):
            self.field.to_representation(not_a_key)

