# In typical LRU Cache design, we use a doubly linked list to maintain the order of the items and a hash map to store the items.
# both get and put must be thread-safe because both mutate state (LRU order)

# What causes race conditions in LRU?

# Typical LRU:
# HashMap → key → node
# Doubly Linked List → maintain order

# Operations:
# get() → move node to front
# put() → insert / update / evict

# Problem
# Concurrent threads can:
# corrupt linked list pointers
# evict wrong node
# lose updates

# Solution we will use a global lock for the entire cache operations