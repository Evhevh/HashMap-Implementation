# Name: Ethan Van Hao
# OSU Email: vanhaoe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap (Portfolio Assignment)
# Due Date: 3/13/2025
# Description: A Separate Chain HashMap implementation of the HashMap class. This class has the ability to
#              add new values to the hashmap, resize its capacity, calculate table load using a function and
#              count the amount of empty buckets. It can also retrieve a value from the HashMap using a key,
#              check if a key is present HashMap, remove a key/value pair, return a tuple of all the key/value
#              pairs and clear the key/value pairs from the HashMap. Lastly, a find_mode function was created
#              to be able to go through a DynamicArray and use a HashMap to find the mode/modes and frequency
#              of the mode and return it as a tuple.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. Replaces the associated value with the new value if the
        given key already exists in the hash map. If not in the hash map, a new pair must be added. Double the
        capacity if current load factor is greater than or equal to 1.0.
        """
        #adjust capacity based on table_load
        if self.table_load() >= 1.0:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        #Retrieve a linkedlist based on the key given
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        bucket = self._buckets.get_at_index(index)

        #check if key already exists and update value associated with key if so
        node = bucket.contains(key)
        if node:
            node.value = value
        else:
            #insert new key/value pair into bucket
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table and rehashes all the existing key/value pairs.
        """
        #check for new_capacity being less than 1
        if new_capacity < 1:
            return

        #check if new_capacity is prime and changes it to the next prime number if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        #initialize new buckets with empty linked lists
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        #store old capacity and update current capacity
        old_capacity = self._capacity
        self._capacity = new_capacity

        new_node = LinkedList()

        #iterate through each bucket in the old buckets array
        for num in range(old_capacity):
            old_bucket = self._buckets.get_at_index(num)
            #iterate through each node in old bucket's linked list
            if old_bucket is not None:
                for node in old_bucket:
                    #insert key/value into new_node
                    new_node.insert(node.key, node.value)

        #update data members
        self._buckets = new_buckets
        self._size = 0

        #use the put method to add key/value pairs into the HashMap
        for node in new_node:
            self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns the calculated load factor of the hash table.
        """
        #calculates using the equation for calculating load factor
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        #initialize a counter
        count = 0

        #iterate through buckets and increment count based on the length of the linked lists
        for pos in range(self._capacity):
            if self._buckets.get_at_index(pos).length() == 0:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Return None if key is not in hash map.
        """
        #calculate index of key
        index = self._hash_function(key) % self._capacity

        #retrieve linked list at index
        bucket = self._buckets.get_at_index(index)

        #search for node containing key
        node = bucket.contains(key)

        #if node is not empty, return the value associated with the node
        if node:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Return true if given key is in the hash map, else return false.
        """
        #calculate index of bucket using given key
        index = self._hash_function(key) % self._capacity

        #get linked list at index
        bucket = self._buckets.get_at_index(index)

        #return true or false if key is empty or not
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. Does nothing if the key is not in the
        hash map.
        """
        #look for the bucket that holds the key
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)

        #if key is removed, decrement size by 1
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        """
        #initialize a new DynamicArray to return
        hashmap_tuple = DynamicArray()

        #iterate through hash map
        for pos in range(self._capacity):
            bucket = self._buckets.get_at_index(pos)
            #iterate through each linked list and append a tuple to the result array
            for node in bucket:
                hashmap_tuple.append((node.key, node.value))

        return hashmap_tuple

    def clear(self) -> None:
        """
        Clears the content of the hash map
        """
        #initialize the private data member to a new DynamicArray
        self._buckets = DynamicArray()

        #fill the DynamicArray with empty LinkedLists with the original capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        #reset size of the HashMap to 0
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Return a tuple containing an array with the modes and the frequency of the mode.
    O(N) time complexity.
    """
    #initialize HashMap and maximum frequency to 0
    map = HashMap()
    max_freq = 0

    #iterate through the given DynamicArray to count the frequency of each element
    for pos in range(da.length()):
        #get element at current position
        key = da.get_at_index(pos)

        #get current frequency of the element
        current = map.get(key)
        if current is None:
            current = 0

        #increment frequency of the element
        new_freq = current + 1

        #update frequency in the HashMap
        map.put(key, new_freq)

        #check and update the maximum frequency if current frequency is greater
        if new_freq > max_freq:
            max_freq = new_freq

    #initialize a DynamicArray for modes
    mode_da = DynamicArray()

    #get all the key/value pairs from the HashMap
    entries = map.get_keys_and_values()

    #iterate through the key/value pairs to find the modes
    for pos in range(entries.length()):
        key, freq = entries.get_at_index(pos)
        if freq == max_freq:
            mode_da.append(key)

    #return tuple of modes array and maximum frequency
    return mode_da, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
