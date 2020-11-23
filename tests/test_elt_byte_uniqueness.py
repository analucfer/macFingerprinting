import macfingerprinting.elt_byte_uniqueness as elt


def test_EltBitFrequencyTable():
    # Preliminary stuff
    bit_table = elt.EltBitFrequencyTable([])
    bit_table.clear()
    bit_table.maximum_bits_per_elt[b'\x00'] = 3 * 8
    bit_table.maximum_bits_per_elt[b'\x01'] = 2 * 8
    test_data = [
        "\x00\x80",
        "\x00\x00",
        "\x00\x00",
        "\x00\x01",
        "\x00\x01",
        "\x00\x01",
        "\x01\x01",
        "\x00\x00\x03",
    ]
    control = {
        b'\x00': [
            # Byte 0
            "0000000",  # 0
            "0000000",  # 1
            "0000000",  # 2
            "0000000",  # 3
            "0000000",  # 4
            "0000000",  # 5
            "0000000",  # 6
            "0000000",  # 7
            # Byte 1
            "1000000",  # 0
            "0000000",  # 1
            "0000000",  # 2
            "0000000",  # 3
            "0000000",  # 4
            "0000000",  # 5
            "0000000",  # 6
            "0001110",  # 7
            # Byte 3
            "0",  # 0
            "0",  # 1
            "0",  # 2
            "0",  # 3
            "0",  # 4
            "0",  # 5
            "1",  # 6
            "1",  # 7
        ],
        b'\x01': [
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "1",
            #
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "1",
        ]
    }
    control_tristate = {
        b'\x00': [
            # Byte 0
            "0000000",  # 0
            "0000000",  # 1
            "0000000",  # 2
            "0000000",  # 3
            "0000000",  # 4
            "0000000",  # 5
            "0000000",  # 6
            "0000000",  # 7
            # Byte 1
            "1000000",  # 0
            "0000000",  # 1
            "0000000",  # 2
            "0000000",  # 3
            "0000000",  # 4
            "0000000",  # 5
            "0000000",  # 6
            "0001110",  # 7
            # Byte 3
            "xxxxxx0",  # 0
            "xxxxxx0",  # 1
            "xxxxxx0",  # 2
            "xxxxxx0",  # 3
            "xxxxxx0",  # 4
            "xxxxxx0",  # 5
            "xxxxxx1",  # 6
            "xxxxxx1",  # 7
        ],
        b'\x01': [
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "1",
            #
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "1",
        ]
    }

    if elt.USE_TRISTATE:
        control = control_tristate

    for elem in test_data:
        elemZeroBytes = list(map(bit_table.unicode_to_byte, elem[0]))[0]
        elemBytes = list(map(bit_table.unicode_to_byte, elem))
        bit_table.add_field(elemZeroBytes, elemBytes)
    errors = 0

    # Check values
    for key in control:
        # keyBytes = bytes(key, 'utf-8')
        byte_array = control[key]
        for byte_idx in range(0, len(byte_array)):
            bit_array = byte_array[byte_idx]
            for bit_idx in range(0, len(bit_array)):
                assert bit_array[bit_idx] == bit_table.data[key][byte_idx][bit_idx]

    bit_table.clear()


def test_hamming_distance_bits():
    assert elt.hamming_distance_bits("101", "1") == 2
    assert elt.hamming_distance_bits("1010", "1010") == 0
    assert elt.hamming_distance_bits("1010", "1011") == 1
    assert elt.hamming_distance_bits("1011", "1010") == 1
    assert elt.hamming_distance_bits("0", "1010") == 4
    assert elt.hamming_distance_bits("1", "1010") == 3


def test_hamming_distance_bytes():
    assert elt.hamming_distance_bytes(b"\x01", b"\x00") == 1
