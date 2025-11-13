import re

class ImmovlanPipeline:
    def process_item(self, item, spider):
        # Normalise strings
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip() or None
            elif value is None or (isinstance(value, str) and not value.strip()):
                item[key] = None
        
        # Convert numeric fields
        numeric_fields = ['number_rooms','living_surface','number_garage','number_baths','facade','floor','price']
        for field in numeric_fields:
            try:
                if item.get(field):
                    item[field] = int(re.sub(r'[^\d]', '', str(item[field])))
            except Exception:
                item[field] = None
        
        # Boolean fields
        boolean_fields = ['furnished','garage','floor_heating','elevator','accessibility','garden','terrace','swimming_pool']
        for field in boolean_fields:
            val = item.get(field)
            if val is not None:
                item[field] = 1 if str(val).lower() in ['yes','y','1'] else 0
            else:
                item[field] = 0
        
        return item
