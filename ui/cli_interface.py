def get_input_from_user(features, model):
    example_row = {}
    for feature in features:
        options = list(model.model[feature].keys())
        print(f"\nPossible values for '{feature}': {options}")
        while True:
            val = input(f"Enter {feature}: ").strip().capitalize()
            if val in options:
                example_row[feature] = val
                break
            else:
                print(f"❌ Invalid value. Please choose from: {options}")
    return example_row
