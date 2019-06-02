# quizz
# Simple Quiz Django project

This is a simple quiz web applications It allows to upload the quizs from csv files and execute them in the browser.
The web will show the test avaiables filtered by categories and the option to add new test. Once a test is selected it would be possible to select the number of questions desired. The order of the questions will be randomized each time a test is launched.

The **CSV** file must follow this structure:
- First row will contain the category name in the first column , the name of the test in the second and in the third an optional description of the test.
- The following rows will contain the questions in the first column. Then in the even rows will be the answers and in the odd columns a "1" or "0" indicating if the answer in the previous column is the correct answer or not.
- At the moment, only one answer can be the right answer but there is no limit for the number of possible answers although 4 is recommended.

The web has a basic authentication system and new users can register(Although the option is hidden for now, it can be acceded on "/account_app/register". The only information attached to the user will be the number of hits/fails on the test. Every test added will be accessible by any member.
