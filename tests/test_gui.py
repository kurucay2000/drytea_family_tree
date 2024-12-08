import pytest
from unittest.mock import Mock, patch, mock_open
from gui.main_window import FamilyTreeUI
from gui.add_member_dialog import AddMemberDialog
from gui.member_details_frame import MemberDetailsFrame


@pytest.fixture
def sample_family_tree():
    """Create a mock family tree with sample data"""
    return {
        "1": {
            "id": 1,
            "name": "Test Person",
            "age": 30,
            "gender": "Male",
            "location": "Test City",
            "occupation": "Tester",
            "aspiration": "Write tests",
            "extra_information": "Loves testing",
            "father": None,
            "mother": None,
            "spouses": [],
        }
    }


@pytest.fixture
def mock_tk():
    """Create a mock Tkinter environment"""
    with patch("tkinter.Tk") as mock_tk, patch(
        "tkinter.StringVar"
    ) as mock_stringvar, patch("tkinter.Text") as mock_text, patch(
        "tkinter.Toplevel"
    ) as mock_toplevel:
        # Configure StringVar mock to store and return values
        class MockStringVar:
            def __init__(self):
                self._value = ""

            def get(self):
                return self._value

            def set(self, value):
                self._value = value

        mock_stringvar.side_effect = MockStringVar

        # Configure Text widget mock
        mock_text_instance = Mock()
        mock_text_instance.get.return_value = ""
        mock_text_instance.delete = Mock()
        mock_text_instance.insert = Mock()
        mock_text.return_value = mock_text_instance

        # Configure Toplevel mock
        mock_toplevel_instance = Mock()
        mock_toplevel_instance.transient = Mock()
        mock_toplevel_instance.grab_set = Mock()
        mock_toplevel_instance.destroy = Mock()
        mock_toplevel.return_value = mock_toplevel_instance

        yield mock_tk.return_value


class TestMemberDetailsFrame:
    @pytest.fixture
    def details_frame(self, mock_tk, sample_family_tree):
        """Create a MemberDetailsFrame instance with mocked Tkinter"""
        mock_save_callback = Mock()
        mock_family_tree = Mock()
        mock_family_tree.members = sample_family_tree

        with patch("tkinter.ttk.Entry"), patch("tkinter.ttk.Combobox"), patch(
            "tkinter.ttk.Button"
        ), patch("tkinter.ttk.Label"), patch("tkinter.ttk.Frame"), patch(
            "tkinter.ttk.LabelFrame"
        ):
            frame = MemberDetailsFrame(mock_tk, mock_family_tree, mock_save_callback)
            return frame

    def test_update_details(self, details_frame):
        """Test updating member details"""
        test_member = {
            "id": "1",
            "name": "Test Person",
            "age": 30,
            "gender": "Male",
            "location": "Test City",
            "occupation": "Tester",
            "extra_information": "Test info",
        }

        details_frame.update_details(test_member)

        # Check if values were set correctly using the actual values stored in StringVar
        assert details_frame.detail_vars["id"].get() == "1"
        assert details_frame.detail_vars["name"].get() == "Test Person"
        assert details_frame.detail_vars["age"].get() == "30"
        assert details_frame.detail_vars["gender"].get() == "Male"
        details_frame.extra_info_text.insert.assert_called_with("1.0", "Test info")


class TestAddMemberDialog:
    @pytest.fixture
    def dialog(self, mock_tk, sample_family_tree):
        """Create an AddMemberDialog instance with mocked Tkinter"""
        with patch("tkinter.ttk.Entry"), patch("tkinter.ttk.Combobox"), patch(
            "tkinter.ttk.Button"
        ), patch("tkinter.ttk.Label"), patch("tkinter.ttk.Frame"), patch(
            "tkinter.ttk.LabelFrame"
        ):
            mock_family_tree = Mock()
            mock_family_tree.members = sample_family_tree
            mock_callback = Mock()

            dialog = AddMemberDialog(mock_tk, mock_family_tree, mock_callback)

            # Mock the family tree's add_member method
            dialog.family_tree.add_member = Mock()

            yield dialog

            if hasattr(dialog, "dialog"):
                dialog.dialog.destroy()

    @patch("tkinter.messagebox.showerror")
    def test_invalid_age_validation(self, mock_error, dialog):
        """Test validation of invalid age input"""
        # Set up the mock values
        dialog.detail_vars["name"].set("Test Person")
        dialog.detail_vars["age"].set("invalid")

        # Mock the open() function to prevent actual file operations
        with patch("builtins.open", mock_open()) as mock_file:
            dialog._add_member()

        # Verify error message was shown
        mock_error.assert_called_with("Error", "Age must be a valid number")

        # Verify add_member was not called
        assert not dialog.family_tree.add_member.called


class TestFamilyTreeUI:
    @pytest.fixture
    def ui(self, mock_tk, sample_family_tree):
        """Create a FamilyTreeUI instance with mocked Tkinter"""
        mock_family_tree = Mock()
        mock_family_tree.members = sample_family_tree

        # Mock the Listbox
        mock_listbox = Mock()
        mock_listbox.size.return_value = 1
        mock_listbox.get.return_value = "Test Person"
        mock_listbox.curselection.return_value = [0]

        with patch("tkinter.Listbox", return_value=mock_listbox), patch(
            "tkinter.ttk.Entry"
        ), patch("tkinter.ttk.Combobox"), patch("tkinter.ttk.Button"), patch(
            "tkinter.ttk.Label"
        ), patch("tkinter.ttk.Frame"), patch("tkinter.ttk.LabelFrame"):
            ui = FamilyTreeUI(mock_family_tree)
            ui.member_listbox = mock_listbox
            return ui

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_member_changes(self, mock_file, mock_json_dump, ui):
        """Test saving member changes"""
        ui.current_member_id = "1"
        ui.details_frame.detail_vars["name"].set("Updated Name")

        # Mock the message box to return True (user clicks "Yes")
        with patch("tkinter.messagebox.askyesno", return_value=True):
            ui._save_member_changes()

            # Verify json.dump was called
            assert mock_json_dump.call_count == 1
            # Verify file was opened
            mock_file.assert_called_once_with("./data/members.json", "w")


if __name__ == "__main__":
    pytest.main(["-v"])
