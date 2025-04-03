from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates the key/value pair in the hash map. Resizes the current capacity to double if the load factor
        is greater than or equal to 0.5.
        """
        #check if calculated table_load is greater than or equal to 0.5 and resize accordingly
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        #calculate index of given key
        index = self._hash_function(key) % self._capacity

        #initialize trackers
        first_tombstone = -1
        found = False
        current_index = 0

        #iterate through table using quadratic probing
        for pos in range(self._capacity):
            #calculate probe index and get the entry at the current index
            current_index = (index + pos * pos) % self._capacity
            current_entry = self._buckets.get_at_index(current_index)

            #if the slot is empty, the key is not in the table
            if current_entry is None:
                break
            #update key/value pair if key exists
            elif current_entry.key == key:
                current_entry.value = value
                #update tombstone logic if current entry is a tombstone
                if current_entry.is_tombstone:
                    current_entry.is_tombstone = False
                    self._size += 1
                #entry found and end loop
                found = True
                break
            #store tombstone index if this is the first tombstone found
            elif current_entry.is_tombstone and first_tombstone == -1:
                first_tombstone = current_index

        #if not key found, insert new key/value pair
        if not found:
            #insert at first tombstone found, if any
            if first_tombstone != -1:
                insert_index = first_tombstone
            else:
                #else, insert at current probe index
                insert_index = current_index

            #create new HashEntry and insert into table and increment size
            self._buckets.set_at_index(insert_index, HashEntry(key, value))
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table and all active key/value pairs are rehashed into the
        new table. The capacity will change to a prime number.
        """
        #check if new_capacity is less than the current number of elements
        if new_capacity < self._size:
            return

        #check if new_capacity is prime and choose the next prime number if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        old_buckets = self._buckets
        old_capacity = self._capacity

        #create new bucket and append None to it
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0

        #iterate through the old HashMap and rehash the old entries into the new HashMap
        for pos in range(old_capacity):
            entry = old_buckets.get_at_index(pos)
            if entry is not None and not entry.is_tombstone:
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        #equation to calculate the table load factor
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        #initialize a counter
        count = 0

        #iterate through the HashMap and increment count if an index is empty
        for pos in range(self._capacity):
            if self._buckets.get_at_index(pos) is None:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Returns None if key is not located in the HashMap.
        """
        #calculate index of given key
        index = self._hash_function(key) % self._capacity

        #iterate through HashMap using quadratic probing
        for pos in range(self._capacity):
            #calculate probe index and get entry at the index
            current_index = (index + pos * pos) % self._capacity
            entry = self._buckets.get_at_index(current_index)
            #if entry is None, the key is not located in the table
            if entry is None:
                return None
            #if entry is tombstone, move to the next entry
            if entry.is_tombstone:
                continue
            #if the keys match, return the value
            if entry.key == key:
                return entry.value

        #return None if key is not found after probing the entire HashMap
        return None


    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is located in the HashMap, otherwise return False.
        """
        #calculate index of given key
        index = self._hash_function(key) % self._capacity

        #iterate through the HashMap using quadratic probing
        for pos in range(self._capacity):
            #calculate probe index and get entry at the index
            current_index = (index + pos * pos) % self._capacity
            entry = self._buckets.get_at_index(current_index)
            #key is not located in the table so return false
            if entry is None:
                return False
            #skip the tombstone and continue with the loop
            if entry.is_tombstone:
                continue
            #key is located and found so return true
            if entry.key == key:
                return True

        #key was not found after probing through the entire HashMap so return false
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key/pair value associated with the given key from the HashMap
        """
        #calculate index of given key
        index = self._hash_function(key) % self._capacity

        #iterate through HashMap using quadratic probing
        for pos in range(self._capacity):
            #calculate probe index and get entry at index
            current_index = (index + pos * pos) % self._capacity
            entry = self._buckets.get_at_index(current_index)
            #key not found
            if entry is None:
                return
            #skip tombstone
            if entry.is_tombstone:
                continue
            #remove entry by turning it into a tombstone and decrementing size
            if entry.key == key:
                entry.is_tombstone = True
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray where each index is a tuple of a key/value pair from the HashMap.
        """
        #initialize a new DynamicArray for the tuple of key/value pairs
        hashmap_tuple = DynamicArray()

        #iterate through the HashMap
        for pos in range(self._capacity):
            entry = self._buckets.get_at_index(pos)
            #append to new DynamicArray if entry is not None or a tombstone
            if entry is not None and not entry.is_tombstone:
                hashmap_tuple.append((entry.key, entry.value))

        #return DynamicArray of tuples
        return hashmap_tuple

    def clear(self) -> None:
        """
        Clear the contents of the HashMap. HashTable capacity if not affected.
        """
        #initialize the Hashmap to a new DynamicArray
        self._buckets = DynamicArray()

        #append None to the DynamicArray with the old capacity
        for _ in range(self._capacity):
            self._buckets.append(None)

        #reset the size
        self._size = 0

    def __iter__(self):
        """
        Enables iteration across the HashMap.
        """
        #start iteration at the beginning and return iterator object
        self._index = 0

        return self

    def __next__(self):
        """
        Return the next item in the HashMap based on the location of the iterator.
        """
        try:
            #retrieve entry at current index
            entry = self._buckets.get_at_index(self._index)

            #loop until valid entry is found
            while entry is None or entry.is_tombstone:
                self._index += 1
                entry = self._buckets.get_at_index(self._index)

        #if out of bounds, raise StopIteration
        except DynamicArrayException:
            raise StopIteration

        #increment index and return valid entry found
        self._index += 1
        return entry


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
