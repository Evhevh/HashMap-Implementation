# HashMap

This project implements two types of hash maps in Python:

- **Separate Chaining Hash Map** ([hash_map_sc.py](hash_map_sc.py)): Uses linked lists to handle collisions.
- **Open Addressing Hash Map** ([hash_map_oa.py](hash_map_oa.py)): Uses quadratic probing and tombstones for collision resolution.

## Features

- Custom dynamic array implementation ([`DynamicArray`](a6_include.py))
- Two hash functions: [`hash_function_1`](a6_include.py), [`hash_function_2`](a6_include.py)
- Separate chaining with singly linked lists ([`LinkedList`](a6_include.py))
- Open addressing with quadratic probing ([`HashEntry`](a6_include.py))
- Methods for insertion, deletion, resizing, and key/value retrieval
- Utility function [`find_mode`](hash_map_sc.py) to find the mode(s) in a dynamic array

## Usage

Each hash map file contains a `HashMap` class with the following methods:

- `put(key, value)`: Insert or update a key-value pair
- `get(key)`: Retrieve the value for a key
- `remove(key)`: Remove a key-value pair
- `contains_key(key)`: Check if a key exists
- `resize_table(new_capacity)`: Resize the hash table
- `get_keys_and_values()`: Get all key-value pairs as a dynamic array
- `clear()`: Remove all entries
- `table_load()`: Get the current load factor
- `empty_buckets()`: Count empty buckets

See the bottom of [hash_map_sc.py](hash_map_sc.py) and [hash_map_oa.py](hash_map_oa.py) for example usage and test cases.

## Requirements

- Python 3.6+
- No external dependencies

## File Overview

- [`a6_include.py`](a6_include.py): Shared data structures and hash functions
- [`hash_map_sc.py`](hash_map_sc.py): Separate chaining hash map implementation
- [`hash_map_oa.py`](hash_map_oa.py): Open addressing hash map implementation
- `README.md`: Project documentation

## Running Tests

You can run either hash map file directly to execute the included test cases:

```sh
python hash_map_sc.py
python hash_map_oa.py
```

## License

This project is for educational purposes.

