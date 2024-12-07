from scripts.family_tree_base import create_family_tree
from scripts.gui_creation import FamilyTreeUI

def main():
    # Create a family tree
    family = create_family_tree()
    family.print_family_tree()
    
    # Create UI
    app = FamilyTreeUI(family)
    app.run()


if __name__ == "__main__":
    main()