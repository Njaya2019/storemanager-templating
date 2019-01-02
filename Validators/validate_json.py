

def validate_json_string_value(json_value):
    if type(json_value)==int:
        return False
    else:
        return True
    
    
   

def validate_json_numeric_value(json_value):
    if type(json_value)==int:
        if json_value < 0:
            return False
        return True
    else:
        return False
  

    

