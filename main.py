from scripts.family_tree import create_family_tree
from gui.main_window import FamilyTreeUI
from gui.tree_visualizer import add_visualization_to_ui


def main():
    family = create_family_tree("./data/members.json")
    app = FamilyTreeUI(family)
    add_visualization_to_ui(app)
    app.run()


if __name__ == "__main__":
    main()
