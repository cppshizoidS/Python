from barcode import EAN13
number = '25061256883547'
my_code = EAN13(number)
my_code.save("new_code")