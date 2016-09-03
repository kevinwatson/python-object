# -*- coding: utf-8 -*-

import unittest

from steenzout.object import Object


class ObjectTestCase(unittest.TestCase):
    """Test case for the Object class."""

    def test_hash(self):
        """Test for the __hash__ function."""

        o1 = Object()
        o2 = Object()
        a = object()

        self.assertEqual(hash(o1), hash(o2))
        self.assertNotEqual(hash(o1), hash(a))

    def test_eq(self):
        """Test for the __eq__ function."""

        o1 = Object()
        o2 = Object()
        a = object()

        self.assertTrue(o1 == o1)
        self.assertTrue(o1 == o2)

        self.assertFalse(id(o1) == id(o2))
        self.assertFalse(o1 == a)

    def test_neq(self):
        """Test for the __neq__ function."""

        o1 = Object()
        o2 = Object()
        a = object()

        self.assertFalse(o1 != o1)
        self.assertFalse(o1 != o2)

        self.assertTrue(o1 != a)

    def test_repr(self):
        """Test for the __repr__ function."""
        o1 = Object()

        self.assertEqual("<class 'steenzout.object.Object'>({})", repr(o1))
