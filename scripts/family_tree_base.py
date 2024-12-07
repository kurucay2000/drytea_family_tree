class FamilyTree:
    def __init__(self):
        """
        Initialize an empty family tree.
        The tree will be stored as a dictionary of people, 
        with each person having a unique identifier.
        """
        self.members = {}
        self.relationships = {}

    def add_member(self, name, birth_date, gender, additional_info=None):
        """
        Add a new member to the family tree.
        
        :param name: Full name of the person
        :param birth_date: Date of birth (string)
        :param gender: Gender of the person
        :param additional_info: Optional dictionary of extra details
        :return: Unique identifier for the new member
        """
        # Generate a unique identifier (you could use a more sophisticated method)
        member_id = len(self.members) + 1
        
        # Create member dictionary
        member = {
            'id': member_id,
            'name': name,
            'birth_date': birth_date,
            'gender': gender,
            'additional_info': additional_info or {}
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
        self.relationships[person1_id].append({
            'person_id': person2_id,
            'relationship_type': relationship_type
        })

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
            print(f"Name: {member['name']}")
            print(f"Birth Date: {member['birth_date']}")
            print(f"Gender: {member['gender']}")
            
            # Print additional info if exists
            if member['additional_info']:
                print("Additional Information:")
                for key, value in member['additional_info'].items():
                    print(f"  {key}: {value}")
            
            # Print relationships
            relationships = self.get_relationships(member_id)
            if relationships:
                print("Relationships:")
                for rel in relationships:
                    related_member = self.get_member(rel['person_id'])
                    print(f"  {rel['relationship_type']}: {related_member['name']}")

# Example usage
def create_family_tree():
    # Create a family tree
    family = FamilyTree()
    
    # Add some family members
    grandpa_id = family.add_member(
        name="John Smith", 
        birth_date="1940-05-15", 
        gender="male", 
        additional_info={"occupation": "Retired Teacher"}
    )
    
    grandma_id = family.add_member(
        name="Mary Smith", 
        birth_date="1942-08-20", 
        gender="female", 
        additional_info={"occupation": "Homemaker"}
    )
    
    dad_id = family.add_member(
        name="Robert Smith", 
        birth_date="1970-03-10", 
        gender="male", 
        additional_info={"job": "Software Engineer"}
    )
    
    mom_id = family.add_member(
        name="Sarah Smith", 
        birth_date="1972-11-25", 
        gender="female", 
        additional_info={"job": "Doctor"}
    )
    
    child1_id = family.add_member(
        name="Emma Smith", 
        birth_date="2000-07-30", 
        gender="female", 
        additional_info={"education": "College Student"}
    )
    
    child2_id = family.add_member(
        name="Jack Smith", 
        birth_date="2003-12-05", 
        gender="male", 
        additional_info={"education": "High School"}
    )
    
    # Add relationships
    family.add_relationship(grandpa_id, grandma_id, "spouse")
    family.add_relationship(grandpa_id, dad_id, "parent")
    family.add_relationship(grandma_id, dad_id, "parent")
    
    family.add_relationship(dad_id, mom_id, "spouse")
    family.add_relationship(dad_id, child1_id, "parent")
    family.add_relationship(dad_id, child2_id, "parent")
    family.add_relationship(mom_id, child1_id, "parent")
    family.add_relationship(mom_id, child2_id, "parent")
    
    family.add_relationship(child1_id, child2_id, "sibling")
    
    # Print the entire family tree
    family.print_family_tree()

if __name__ == "__main__":
    create_family_tree()