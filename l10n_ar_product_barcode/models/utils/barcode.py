import math


def ean_checksum(eancode):
    """
        returns the checksum of an ean string of length 12, returns -1 if
        the string has the wrong length
    """

    if len(eancode) != 12:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def generate_ean(product_code, settings):
    """Creates and returns a valid ean13 from product and company codes"""
    if not product_code:
        product_code = "00000"

    country_key = settings.get('COUNTRY_KEY')
    company_code = settings.get('COMPANY_KEY')
    ean = country_key + company_code + product_code.zfill(5)
    check = ean_checksum(ean)
    return ean + str(check)
