class FamilyTree:
    def __init__(self):
        """
        Initialize an empty family tree.
        The tree will be stored as a dictionary of people,
        with names as the keys.
        """
        self.members = {}
        self.member_ids = []

    def add_member(
        self,
        name=None,
        id=None,  # Add ID parameter
        age=None,  # Age is now a string
        gender=None,
        location=None,
        occupation=None,
        aspiration=None,
        cause_of_death=None,
        extra_information=None,
        father=None,
        mother=None,
        spouses=None,
    ):
        """
        Add a new member to the family tree.

        :param name: Full name of the person (required)
        :param id: Unique identifier for the person (optional)
        :param age: Age of the person as integer (optional)
        ...
        """
        if not name:
            raise ValueError("Name is required")

        # Validate and convert gender to title case if provided
        valid_genders = ["Male", "Female", "Alien", "Other"]
        if gender:
            gender = gender.title()
            if gender not in valid_genders:
                raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")

        # Validate age as a string
        valid_ages = [
            "Infant",
            "Toddler",
            "Child",
            "Teen",
            "Young Adult",
            "Adult",
            "Elder",
        ]
        if age:
            age = age.title()
            if age not in valid_ages:
                raise ValueError(f"Age must be one of: {', '.join(valid_ages)}")

        # Create member dictionary
        member = {
            "id": id,  # Include ID in member dictionary
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "occupation": occupation,
            "aspiration": aspiration,
            "cause_of_death": cause_of_death,
            "extra_information": extra_information,
            "father": father,
            "mother": mother,
            "spouses": [spouse for spouse in (spouses or []) if spouse is not None],
        }

        # Store the member using their name as the key
        self.members[name] = member

        # Remove code that adds member to parents' children lists
        # if father and father in self.members:
        #     self.members[father]["children"].append(name)
        # if mother and mother in self.members:
        #     self.members[mother]["children"].append(name)

        return name

    def get_member(self, name):
        """
        Retrieve a member's details by their name.

        :param name: Name of the member
        :return: Dictionary with member details
        """
        return self.members.get(name)

    def print_family_tree(self):
        """
        Print out the entire family tree in a readable format.
        """
        print("Family Tree:")
        for name, member in self.members.items():
            print(f"\nMember: {name}")

            # Print member details
            fields = [
                ("Age", "age"),
                ("Gender", "gender"),
                ("Location", "location"),
                ("Occupation", "occupation"),
                ("Aspiration", "aspiration"),
                ("Cause of Death", "cause_of_death"),
                ("Extra Information", "extra_information"),
            ]

            for label, field in fields:
                if member[field] is not None:
                    print(f"{label}: {member[field]}")

            # Print relationships
            relationships = []
            if member["father"]:
                relationships.append(("Father", member["father"]))
            if member["mother"]:
                relationships.append(("Mother", member["mother"]))
            for spouse in member["spouses"]:
                relationships.append(("Spouse", spouse))
            for child in member["children"]:
                relationships.append(("Child", child))

            if relationships:
                print("Relationships:")
                for rel_type, rel_name in relationships:
                    print(f"  {rel_type}: {rel_name}")


def load_member_data_from_json(family_tree, members_file):
    """
    Load member data from a JSON file into an existing FamilyTree instance.
    """
    import json

    try:
        with open(members_file, "r") as f:
            members_data = json.load(f)

        # Validate members data structure
        if not isinstance(members_data, list):
            raise ValueError("Members JSON file must contain a list of members")

        # First pass: Add all members without relationships
        for member_data in members_data:
            try:
                family_tree.add_member(
                    id=member_data.get("id"),  # Include ID when adding member
                    name=member_data.get("name"),
                    age=member_data.get("age"),
                    gender=member_data.get("gender"),
                    location=member_data.get("location"),
                    occupation=member_data.get("occupation"),
                    aspiration=member_data.get("aspiration"),
                    cause_of_death=member_data.get("cause_of_death"),
                    extra_information=member_data.get("extra_information"),
                )
            except ValueError as e:
                print(f"Warning: Skipping invalid member data: {str(e)}")
                continue

        # Second pass: Add relationships
        for member_data in members_data:
            name = member_data.get("name")
            if name and name in family_tree.members:
                member = family_tree.members[name]
                member["father"] = member_data.get("father")
                member["mother"] = member_data.get("mother")
                member["spouses"] = member_data.get("spouses", [])

    except FileNotFoundError:
        raise FileNotFoundError(f"Members file not found: {members_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in members file: {members_file}")


def create_family_tree(members_file):
    """
    Create a new family tree and load data from JSON files.

    :param members_file: Path to JSON file containing family member data
    :param relationships_file: Path to JSON file containing relationship data (not used)
    :return: FamilyTree instance with loaded data
    """
    # Create new family tree
    family_tree = FamilyTree()

    # Load member data
    load_member_data_from_json(family_tree, members_file)

    return family_tree
