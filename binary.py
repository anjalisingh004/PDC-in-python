'''number = 42
binary_representation = "{:016b}".format(number)
print(binary_representation)'''

value = 10
formatted_string = "{0:0>2X}".format(value)
print(formatted_string)


hex_list1 = ['65', 'F1', '45', 'F0']
binary_list1 = [bin(int(hex_str, 16))[2:].zfill(8) for hex_str in hex_list1]
print(binary_list1)

hex_list2 = ['00', '02']
binary_list2 = [bin(int(hex_str, 16))[2:].zfill(8) for hex_str in hex_list2]
print(binary_list2)

