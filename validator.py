import json

def load_profile (profile_path="profile_v1.json"):
                """Loads the active Risk Profile configuration."""
                with open(profile_path, "r") as f:
                    return json.load(f) 

def validate_measurements (raw_data, profile):
    """
     Validates incoming raw biomarker readings against the active Risk Profile. 
     Returns: (is_valid: bool, errors: list) 
    """ 
    errors = [] 
    # 1. Check hardware cartridge status flag
    if raw_data.get("cartridge_status") != "OK":
        errors.append(f"Cartridge error: {raw_data.get('cartridge_status', 'FAULTY')}")
        return False, errors 
    # 2. Iterate over required biomarkers defined in the profile
    biomarker_rules = profile.get("biomarkers", {})
    measurements = raw_data.get("measurements", {})
    for marker_name, rules in biomarker_rules.items():
        # Check for missing biomarker readings
        if marker_name not in measurements or measurements[marker_name] is None:
            errors.append(f"Missing measurement for required biomarker: {marker_name}")
            continue
        value = measurements[marker_name] 
        # Check for non-numeric data types
        if not isinstance(value, (int, float)):
            errors.append(f"Invalid data type for {marker_name}: expected number, got {type(value).__name__}")
            continue 
        
        
        # Check measurement against physical valid range bounds 
        min_valid, max_valid = rules["valid_range"]
        if value < min_valid or value > max_valid:
            errors.append(f"Value for {marker_name} ({value} {rules['unit']}) is outside valid range [{min_valid}, {max_valid}]")
    is_valid = len(errors) == 0
    return is_valid, errors