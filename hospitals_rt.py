NUM_OF_COLUMNS = 7

class hospital:
    def __init__(self, latitude, longitude, gaz_name, feature_id, county_name, state_alpha, gaz_featureclass):
        self.latitude = latitude
        self.longitude = longitude
        self.gaz_name = gaz_name
        self.feature_id = feature_id
        self.county_name = county_name
        self.state_alpha = state_alpha
        self.gaz_featureclass = gaz_featureclass
        
def put_into_list(file):
    temp_latitude = 0.0
    temp_longitude = 0.0
    temp_gaz_name = ''
    temp_feature_id = 0
    temp_county_name = ''
    temp_state_alpha = ''
    temp_gaz_featureclass = ''
    hospital_list = []

    for line in file: # For every line in the file
        j = 0 # character counter
        k = 0 # column counter
        for column in range(NUM_OF_COLUMNS): # and for every column from our records.
            content = "" # Firstly, we initialise a string.
            for character in line[j:len(line)]: # Then, we iterate through every string,
                j = j + 1 # we count the characters
                if character == ';': # and if we find a ;
                    k = k + 1 # we add 1 to our column counter, signaling that one column is finished
                    break # and we break from the character loop.
                content = content + character # We add each character to our string value
            # and we assign that string value to our temporary variables, based on the column counter.
            if k == 1: 
                temp_latitude = content
                temp_latitude = temp_latitude.replace ("," , ".")
                temp_latitude = float(temp_latitude)
            elif k == 2: 
                temp_longitude = content
                temp_longitude = temp_longitude.replace ("," , ".")
                temp_longitude = float(temp_longitude)
            elif k == 3: temp_gaz_name = content
            elif k == 4: temp_feature_id = int(content)
            elif k == 5: temp_county_name = content
            elif k == 6: 
                temp_state_alpha = content
                k = k + 1
            elif k == 7: temp_gaz_featureclass = content
        # After we are through with one line, we create the hospital object
        temp_hospital = hospital(temp_latitude, temp_longitude, temp_gaz_name,temp_feature_id, temp_county_name, temp_state_alpha , temp_gaz_featureclass )
        hospital_list.append(temp_hospital)# and we add that object to our list of hospitals

    return hospital_list
       