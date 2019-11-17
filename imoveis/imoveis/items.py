import scrapy


class PropertyItem(scrapy.Item):
    url = scrapy.Field()
    code = scrapy.Field("")
    property_type = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    neighborhood = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    rent_price = scrapy.Field()
    sale_price = scrapy.Field()
    built_area = scrapy.Field()
    total_area = scrapy.Field()
    real_estate = scrapy.Field()
    for_rent = scrapy.Field()
    for_sale = scrapy.Field()
    date = scrapy.Field()
    proposals = scrapy.Field()  # It exists ... not sure if I can trust it
    properties = scrapy.Field()
    rooms = scrapy.Field()
