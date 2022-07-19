# budget-planner

## Project Objective

Hello, stranger

This passion project is focused on creating my own personal budget planner application for two purposes: to hone my python skills and manipulate my finance data more freely than Excel.

The following project is built upon dash and dash-bootstrap-components ~~with ramen too~~.

| library                   | versions  |
| ------------------------- |-----------|
| python                    | 3.9.12    |
| dash                      | 2.5.1     |
| dash-bootstrap-components | 1.1.0     |
| dash-core-components      | 2.0.0     |
| pandas                    | 1.4.2     |
| sqlite3                   | 3.38.3    |

## How To Use

Run

```python
python home.py
```

To add a gif for the loading screen, simply add a gif to the assets foulder named 'loading.gif'

## Pending updates

### Priority One List

1. EXPENSE implementation with code simplification
  - take notes out
  - date, place, price, PMT, expense
1. home [start by 7/14]

### Features to keep track/testing

- navigation bar to different pages
- printed initialization messages
- income page loads from database if exists
- otherwise can upload or start new data
- error msg with non CSV file
- income page loads with default page size every reload
- income page can change tbl page size
- tbl dropdown error msg when no income and pay type
- loads properly when type is saved in database or not
- can add a row
- only saves when saved is pressed
- save button has a message change: Saved!
- loads from db otherwise can add or delete, will update dropdown
- can export and delete

### Possibly bugs to remember

- persistence type and temporary storage for input and tbl data
- css px might need to be switched to rem
- income should sort data by date...
- sql doesnt read on different connections when using memory
- sql should commit!!

### helpful links

- "https://techblogs.azurewebsites.net/2020/11/23/why-sometimes-the-dropdown-list-does-not-show-up-in-a-dash-table/"
