## v1.3.0 (2024-12-09)

## v1.1.1 (2024-12-09)

### Feat

- fix bug in the member details pop-ups for whether or not info changed
- add sorting by first/last name to the family member list UI
- sort names alphabetically in UI by last name. Fix UI tests
- update UI colors to be purple. less eye sore now!!
- add nox for running pre-commit/pytest
- adjust age to be a string rather than a number; add validation
- validation checks on mother/fathers being added

### Fix

- clearing details was not working correct during removal. added test for it
- correctly removes information now
- fix bugs in updating member details, especially with id field
- fixed validation on father/mother and age inputs
- json data error
- master not main on ci
- unused import
- bug that was adding new member IDs as a string instead of int

### Refactor

- create gui folders and fix some silly file names

## v1.1.0 (2024-12-07)

### Fix

- fixed some bugs with children data

### Refactor

- a number of UI fixes and a refactor of the GUI elements

## v1.0.2 (2024-12-07)

### Feat

- improve GUI and refactor out relationships for tracking parents
- improve add family member function/UI
- create ability to edit member information in UI
- add ability to remove a member from the UI
- adjust input to take JSON files rather than hard-coded

## v0.1.0 (2024-12-07)

### Feat

- add uv export and more formatting
- add new family member metadata
- add tree visualization and some depencencies
- add a GUI for visualizing all of the member data
- add base family tree
- inital uv commit
