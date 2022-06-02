# budget-planner

## Project Objective

Hello, stranger

This passion project is focused on creating my own personal budget planner application for two purposes: to hone my python skills and manipulate my finance data more freely than Excel.

The following project is built upon dash and dash-bootstrap-components ~~with ramen too~~.

| library                   | versions  |
| ------------------------- |-----------|
| python                    | 3.9.12    |
| dash                      | 2.4.1     |
| dash-bootstrap-components | 1.1.0     |
| dash-core-components      | 2.0.0     |
| pandas                    | 1.4.2     |

## How To Use

Run
```
python home.py
```
To add a gif for the loading screen, simply add a gif to the assets foulder named 'loading.gif'

### Income

To use prexisiting data:

- save data as 'data/income.csv'
- IT IS ~~FUCKING~~ IMPORTANT TO HAVE THE FOLLOWING CSV HEADERS

>date,category,amount,mop,notes

When saving, the current income.csv will be saved to a backup file until they are 5. Then it will delete the oldest one.

Additionally, when manipulating data and switching pages, it will not save. This is so when creating a mistake, one can easily revisit the page to undo it.

## Pending updates

### Priority One List

1. sql implementation
1. drop down vs improve reading in csv possibly
1. settings
1. expense
1. home

### Priority Two List

1. table width
