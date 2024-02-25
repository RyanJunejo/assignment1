"""Assignment 1 - Tests for class PriorityQueue  (Task 3a)

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module will contain tests for class PriorityQueue.
"""
import pytest
from container import PriorityQueue


# TODO: Put your pytest test functions for class PriorityQueue here
class TestPriorityQueue:
    @pytest.fixture
    def test_empty_priority_queue_is_empty(self):
        """Test that an empty priority queue is indeed empty."""
        empty_priority_queue = PriorityQueue()
        assert empty_priority_queue.is_empty()

    def test_add_to_priority_queue(self):
        """Test adding an item to a priority queue."""
        empty_priority_queue = PriorityQueue()
        empty_priority_queue.add('item')
        assert not empty_priority_queue.is_empty()

    def test_remove_from_priority_queue(self):
        """Test removing an item from a priority queue."""
        empty_priority_queue = PriorityQueue()
        empty_priority_queue.add('item')
        empty_priority_queue.remove()
        assert empty_priority_queue.is_empty()

    def test_priority_order(self):
        """Test that items are removed from the priority queue in the correct order."""
        empty_priority_queue = PriorityQueue()
        empty_priority_queue.add('item1')
        empty_priority_queue.add('item2')
        assert empty_priority_queue.remove() == 'item1'
        assert empty_priority_queue.remove() == 'item2'

    def test_maintain_priority_order(self):
        """Test that priority order is maintained after adding new items."""
        empty_priority_queue = PriorityQueue()
        empty_priority_queue.add('item1')
        empty_priority_queue.add('item2')
        empty_priority_queue.add('item3')
        assert empty_priority_queue.remove() == 'item1'
        empty_priority_queue.add('item4')
        assert empty_priority_queue.remove() == 'item2'
        assert empty_priority_queue.remove() == 'item3'
        assert empty_priority_queue.remove() == 'item4'

    def test_add_maintains_priority_order(self):
        """Test that adding items maintains the correct priority order."""
        priority_queue = PriorityQueue()
        priority_queue.add('apple')
        priority_queue.add('banana')
        priority_queue.add('orange')
        assert priority_queue.remove() == 'apple'
        assert priority_queue.remove() == 'banana'
        assert priority_queue.remove() == 'orange'

    def test_add_with_duplicates(self):
        """Test that adding duplicate items preserves their order."""
        priority_queue = PriorityQueue()
        priority_queue.add('apple')
        priority_queue.add('banana')
        priority_queue.add('banana')
        assert priority_queue.remove() == 'apple'
        assert priority_queue.remove() == 'banana'
        assert priority_queue.remove() == 'banana'

    def test_add_with_numbers(self):
        """Test that adding numbers maintains their correct order."""
        priority_queue = PriorityQueue()
        priority_queue.add(5)
        priority_queue.add(3)
        priority_queue.add(8)
        assert priority_queue.remove() == 3
        assert priority_queue.remove() == 5
        assert priority_queue.remove() == 8

    def test_priority_queue_item_not_inside(self):
        """Test PriorityQueue() knows that an item is not inside of it"""
        pq = PriorityQueue()
        pq.add('Bob')
        pq.add('Rob')
        pq.add('Hob')
        assert pq.remove() != 'Aob'


if __name__ == '__main__':
    import pytest

    pytest.main(['test_priority_queue.py'])
