from app.models.enums import TaskTag


class Tag:
    def __init__(self, name: TaskTag):
        self.name: TaskTag = name

    def get_name(self) -> TaskTag:
        return self.name

    # Default Behavior: By default, Python classes inherit __eq__ from the object class,
    # which compares objects by their identity (memory address, like the is operator).
    # Two different instances are never equal, even if their attributes are identical.
    # Customization: You override __eq__ to compare objects based on their values
    # or attributes rather than their identity. This allows two separate instances with the same data to be considered equal.
    def __eq__(self, other) -> bool:
        if not isinstance(other, Tag):
            return False
        return self.name == other.name

    # Purpose: This hash value is used internally by hash tables (dictionaries and sets)
    # to quickly find and store items (average O(1) time complexity). Objects with the same hash
    # are placed in the same "bucket," followed by an equality check to confirm the exact match.
    # Default Behavior: By default, custom classes also inherit __hash__ from object, which returns a hash based on the object's identity.
    # Requirement: The hash value of an object must not change during its lifetime (immutability).
    # This is why mutable types (like lists and dictionaries) are unhashable, while immutable types (like tuples and frozensets) are.
    def __hash__(self) -> int:
        return hash(self.name)

    # The main rule governing their interaction is: If two objects are equal (according to __eq__),
    # they must have the same hash value (according to __hash__). The reverse is not required (different objects can have the same hash value
    # due to collisions). Quality of life: You don't need to implement both methods if you don't need custom comparison logic or hash values.

    # If you implement __eq__ but not __hash__:
    # Python 3 automatically sets the __hash__ method to None, making instances of that class unhashable. Attempting to use them as dictionary
    # keys or in a set will raise a TypeError. This safety feature prevents breaking the hash contract because the default identity-based hash
    # is no longer consistent with value-based equality.
    #
    # If you implement both:
    # You must ensure the implementation follows the contract. The attributes used to determine equality in __eq__ must be a subset of (or the same as)
    # the attributes used in __hash__. The hashed attributes should be immutable.
