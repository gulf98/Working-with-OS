# Working-with-OS
Course: Python QA Engineer - 2022 (OTUS).\
Homework 9: Working with OS.

Script action:
- reads the result of a command 'ps aux'
- translates the received data into a dictionary
- generates a report of the specified format
- prints the report to the console
- saves the report to a file '%d-%m-%Y-%H:%M-scan.txt'

Report Format:\
System status:\
System users: 'root', 'user1', ...\
Processes running: 833\
User processes:\
root: 533\
user1: 231\
...\
Total memory used: 45.7%\
Total CPU used: 33.2%\
Uses the most memory: (%process name, first 20 characters if longer)\
Most CPU used: (%process name, first 20 characters if longer)