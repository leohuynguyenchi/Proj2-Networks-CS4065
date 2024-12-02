# Huy Nguyen - Toan Ly - Toan Nham
# Proj2-Networks-CS4065
This is a project 2 for Computer Networks class - Fall 2024

**Project Overview**: This project implements a Bulletin Board System using a client-server architecture with sockets. It supports:

- A single public message board where users can join, post, and retrieve messages.
- Multiple private message groups where users can join specific groups, post, and interact with users within those groups.
- Both the client and server are written in Python.

**Compilation and Running Instructions**
_Prerequisites_: Ensure Python (version 3.6 or later) is installed.

**Steps to Run**
1. Start the Server:
   - Navigate to the directory containing the server.py file.
   - Run "_python server.py_" in the terminal

2. Start the client:
   - Navigate to the directory containing client.py file.
   - Run "_python client.py_" in the different terminal

**Usability Instructions**

_Part 1_:
- %connect localhost 8080: Connect to the server.
- %join: Join the public message board.
- %post <content>: Post a message to the public message board.
- %users: Retrieve a list of users in the public message board.
- %message <message_id>: Retrieve the content of a specific message by ID.
- %leave: Leave the public message board.
- %exit: Disconnect from the server and exit the client.

_Part 2_:
 - %groups: Retrieve a list of all available groups.
 - %groupjoin <group_name>: Join a specific group or multiple groups (separated by a comma). E.g: %groupjoin g1,g2,g3
 - %grouppost <group_name> <content>: Post a message to a private group's message board.
 - %groupusers <group_name>: Retrieve a list of users in the specified group.
 - %groupleave <group_name>: Leave a specific group.
 - %groupmessage <group_name> <message_id>: Retrieve the content of a specific message in a private group.

