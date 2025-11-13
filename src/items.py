import scrapy

class ImmovlanItem(scrapy.Item):
    project_url = scrapy.Field()
    property_url = scrapy.Field()
    
    # Principal information
    property_type = scrapy.Field()
    locality_name = scrapy.Field()
    property_id = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    price = scrapy.Field()
    
    # General information
    state = scrapy.Field()
    number_rooms = scrapy.Field()
    living_surface = scrapy.Field()
    furnished = scrapy.Field()
    garage = scrapy.Field()
    number_garage = scrapy.Field()
    number_baths = scrapy.Field()
    floor_heating = scrapy.Field()
    glazing = scrapy.Field()
    elevator = scrapy.Field()
    accessibility = scrapy.Field()
    facade = scrapy.Field()
    floor = scrapy.Field()
    garden = scrapy.Field()
    terrace = scrapy.Field()
    swimming_pool = scrapy.Field()
