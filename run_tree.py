from scripts.family_tree_base import create_family_tree
from scripts.gui_creation import FamilyTreeUI
from scripts.tree_visualizer import add_visualization_to_ui


def main():
    # Create a family tree
    family = create_family_tree("./data/members.json", "./data/relationships.json")
    # family.print_family_tree()

    # Create UI
    app = FamilyTreeUI(family)
    add_visualization_to_ui(app)
    app.run()


if __name__ == "__main__":
    main()
