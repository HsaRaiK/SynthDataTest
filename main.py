from validator import load_profile, validate_measurements
import json


if __name__ == "__main__":
	profile = load_profile("profile_v1.json")

	# Sample valid payload
	valid_sample = {
		"cartridge_status": "OK",
		"measurements": {"IL-6": 12.5, "neutrophil_marker": 85.0},
	}

	# Sample invalid payload (missing IL-6, out-of-range neutrophil)
	invalid_sample = {
		"cartridge_status": "OK",
		"measurements": {"neutrophil_marker": 1500.0},
	}

	# 3. Print Payload 1 & Validation Result
	print("--- SAMPLE 1: VALID PAYLOAD ---")
	print("Input Data:")
	print(json.dumps(valid_sample, indent=2))
	is_valid, errors = validate_measurements(valid_sample, profile)
	print(f"Validation Result: is_valid = {is_valid}")
	print(f"Errors: {errors}\\n")

	# 4. Print Payload 2 & Validation Result
	print("--- SAMPLE 2: INVALID PAYLOAD ---")
	print("Input Data:")
	print(json.dumps(invalid_sample, indent=2))
	is_valid, errors = validate_measurements(invalid_sample, profile)
	print(f"Validation Result: is_valid = {is_valid}")
	print(f"Errors: {errors}\\n")