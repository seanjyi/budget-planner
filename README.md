# Budget Planner

## Project Objective

Hello Stranger, 

This passion project was focused on creating my own personal budget planner application for two purposes: to hone my python skills and manipulate my finance data more easily than on Google Sheets. While Google Sheets is well designed to input data and display graphs, I wanted to personalize it more to my needs. 

The following project is built upon dash and dash-bootstrap-components. ~~and ramen~~

| library                   | versions  |
| ------------------------- |-----------|
| python                    | 3.9.12    |
| dash                      | 2.5.1     |
| dash-bootstrap-components | 1.1.0     |
| dash-core-components      | 2.0.0     |
| pandas                    | 1.4.2     |
| sqlite3                   | 3.38.3    |

## How To Use

Run following code:

```
python home.py
```
The following project will open in a web browser of you choosing. 

*Note: To add a gif for the loading screen, simply add a gif to the assets foulder named 'loading.gif'*

### Home
Unfortunately, the Home page is still under construction. Eventually, I would have liked to added visual graphs here.

### Income & Expense
The Income page is a simple design of using a table to input data. Upon initial load, if there isn't any data saved from previous sessions, then the user is asked if they want to start from scratch or input a CSV file. Upon choosing or loading from the database, the user will be able to add data, save, increase row or change page size. If there isn't any values for the dropdown lists an error will appear. Upon saving, the data will be saved to a local SQL database.

The Expense page mimics the Income page. The only difference is the input categories.

### Settings
The Settings page handles the default page size, drowdown list values, and the exportation or deletion of data. To input data simply write in the value and click add. It will then appear under the respective category. If the user wants to export their data as a CSV file, they just to click on the respective button. It will create a save file, and if a save already exists it will create up to 5 backup files. If the user wants to delete their data from the database, all they need to do is click the respective button.


## Conclusion
Finishing the project, I am surprised to have used HTML, CSS, bootstrap and SQL. My intention was a simple Python program that uses Dash; however, feeling confident that the summer was long, I planned for more features than I could accomplish. Even though I am sad that I wasn't able to finish the project, I am glad I was able to add multiple features. As I said before, this is a passion project. It was fun to apply skills and good coding practices that I have picked up from my classes. While each feature took some time, I am proud of every one: from the color confirmation saving button to saving data on a SQL database.

Of course, looking back there are definitely some things I would change. For instance, I would have created multiple branches for each feature. Pushing directly to the main branch was okay for a small project like this, but having multiple branches would have helped me debug a little quicker. Additionally, I would have curbed my expectations for the Dash library. The Dash library isn't intended for extensive interactive use. It is a library made for visualization. If could have redo the project, I wouldn't have focused on the Income and Expense pages. Instead, I would have simply imported the data as a CSV file and focused on creating interesting graphs to analyze spending patterns.

Thank you for reading about my project! 
