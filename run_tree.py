from scripts.family_tree_base import create_family_tree
from scripts.family_tree_ui import FamilyTreeUI
from scripts.tree_visualizer import add_visualization_to_ui


def main():
    family = create_family_tree("./data/members.json", None)
    app = FamilyTreeUI(family)
    add_visualization_to_ui(app)
    app.run()


if __name__ == "__main__":
    main()
