class FamilyTree:
    def __init__(self):
        """
        Initialize an empty family tree.
        The tree will be stored as a dictionary of people,
        with each person having a unique identifier.
        """
        self.members = {}
        self.relationships = {}

    def add_member(
        self,
        name=None,
        age=None,
        gender=None,
        location=None,
        occupation=None,
        aspiration=None,
        cause_of_death=None,
        extra_information=None,
    ):
        """
        Add a new member to the family tree.

        :param name: Full name of the person (optional)
        :param age: Age of the person as integer (optional)
        :param gender: Gender of the person (one of "Male", "Female", "Alien", "Other") (optional)
        :param location: Location of the person (optional)
        :param occupation: Occupation of the person (optional)
        :param aspiration: Life aspiration of the person (optional)
        :param cause_of_death: Cause of death if applicable (optional)
        :param extra_information: Any additional information (optional)
        :return: Unique identifier for the new member
        """
        # Generate a unique identifier
        member_id = len(self.members) + 1

        # Validate and convert gender to title case if provided
        valid_genders = ["Male", "Female", "Alien", "Other"]
        if gender:
            gender = gender.title()
            if gender not in valid_genders:
                raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")

        # Convert age to integer if provided
        if age is not None:
            try:
                age = int(float(age))  # Handle both string and float inputs
                if age < 0:
                    raise ValueError("Age cannot be negative")
            except ValueError as e:
                if str(e) == "Age cannot be negative":
                    raise
                raise ValueError("Age must be a valid integer")

        # Create member dictionary
        member = {
            "id": member_id,
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "occupation": occupation,
            "aspiration": aspiration,
            "cause_of_death": cause_of_death,
            "extra_information": extra_information,
        }

        # Store the member
        self.members[member_id] = member

        return member_id

    def add_relationship(self, person1_id, person2_id, relationship_type):
        """
        Add a relationship between two family members.

        :param person1_id: ID of the first person
        :param person2_id: ID of the second person
        :param relationship_type: Type of relationship (e.g., 'parent', 'spouse', 'sibling')
        """
        if person1_id not in self.members or person2_id not in self.members:
            raise ValueError("One or both persons not found in the family tree")

        # Initialize relationships list if not exists
        if person1_id not in self.relationships:
            self.relationships[person1_id] = []

        # Add relationship
        self.relationships[person1_id].append(
            {"person_id": person2_id, "relationship_type": relationship_type}
        )

    def get_member(self, member_id):
        """
        Retrieve a member's details by their ID.

        :param member_id: ID of the member
        :return: Dictionary with member details
        """
        return self.members.get(member_id)

    def get_relationships(self, member_id):
        """
        Get all relationships for a specific member.

        :param member_id: ID of the member
        :return: List of relationships
        """
        return self.relationships.get(member_id, [])

    def print_family_tree(self):
        """
        Print out the entire family tree in a readable format.
        """
        print("Family Tree:")
        for member_id, member in self.members.items():
            print(f"\nMember ID {member_id}:")

            # Print member details
            fields = [
                ("Name", "name"),
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
            relationships = self.get_relationships(member_id)
            if relationships:
                print("Relationships:")
                for rel in relationships:
                    related_member = self.get_member(rel["person_id"])
                    related_name = (
                        related_member["name"]
                        if related_member["name"]
                        else f"Member {rel['person_id']}"
                    )
                    print(f"  {rel['relationship_type']}: {related_name}")


def load_member_data_from_json(family_tree, members_file):
    """
    Load member data from a JSON file into an existing FamilyTree instance.

    :param family_tree: FamilyTree instance to load data into
    :param members_file: Path to JSON file containing family member data
    :raises FileNotFoundError: If members file is not found
    :raises ValueError: If JSON format is invalid or data structure is incorrect
    """
    import json

    try:
        with open(members_file, "r") as f:
            members_data = json.load(f)

        # Validate members data structure
        if not isinstance(members_data, list):
            raise ValueError("Members JSON file must contain a list of members")

        # Add each member to the tree
        for member_data in members_data:
            try:
                family_tree.add_member(
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

    except FileNotFoundError:
        raise FileNotFoundError(f"Members file not found: {members_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in members file: {members_file}")


def load_relationship_data_from_json(family_tree, relationships_file):
    """
    Load relationship data from a JSON file into an existing FamilyTree instance.
    Supports using names instead of IDs to specify relationships.

    :param family_tree: FamilyTree instance to load data into
    :param relationships_file: Path to JSON file containing relationship data
    :raises FileNotFoundError: If relationships file is not found
    :raises ValueError: If JSON format is invalid or data structure is incorrect
    """
    import json

    def find_member_id_by_name(name):
        """Helper function to find a member's ID by their name"""
        for member_id, member in family_tree.members.items():
            if member.get("name") == name:
                return member_id
        raise ValueError(f"Member with name '{name}' not found")

    try:
        with open(relationships_file, "r") as f:
            relationships_data = json.load(f)

        # Validate relationships data structure
        if not isinstance(relationships_data, list):
            raise ValueError(
                "Relationships JSON file must contain a list of relationships"
            )

        # Add each relationship to the tree
        for rel_data in relationships_data:
            try:
                person1_name = rel_data.get("person1")
                person2_name = rel_data.get("person2")
                relationship_type = rel_data.get("relationship")

                if not all([person1_name, person2_name, relationship_type]):
                    raise ValueError("Missing required relationship data")

                # Convert names to IDs
                try:
                    person1_id = find_member_id_by_name(person1_name)
                    person2_id = find_member_id_by_name(person2_name)
                except ValueError as e:
                    print(f"Warning: Skipping relationship - {str(e)}")
                    continue

                family_tree.add_relationship(person1_id, person2_id, relationship_type)
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping invalid relationship data: {str(e)}")
                continue

    except FileNotFoundError:
        raise FileNotFoundError(f"Relationships file not found: {relationships_file}")
    except json.JSONDecodeError:
        raise ValueError(
            f"Invalid JSON format in relationships file: {relationships_file}"
        )


def create_family_tree(members_file, relationships_file):
    """
    Create a new family tree and load data from JSON files.

    :param members_file: Path to JSON file containing family member data
    :param relationships_file: Path to JSON file containing relationship data
    :return: FamilyTree instance with loaded data
    """
    # Create new family tree
    family_tree = FamilyTree()

    # Load member data
    load_member_data_from_json(family_tree, members_file)

    # Load relationship data
    load_relationship_data_from_json(family_tree, relationships_file)

    return family_tree
