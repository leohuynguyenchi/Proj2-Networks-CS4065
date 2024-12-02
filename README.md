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

**Issues Encountered and Solutions**
1. Bug: Users from one group could retrieve messages from other groups (#21)
   - Problem: A user in one group was able to access messages posted in other groups.
   -> Solution: Updated the message retrieval logic to filter messages based on the user’s current group(s). Make sure that group-specific message boards were accessed only by authorized users.

2. Bug: Users from one group could post messages to another group
   - Problem: Users were inadvertently able to post messages to groups they were not a part of.
   -> Solution: Added a validation layer in the server to check a user’s group membership before allowing message posts. Unauthorized attempts are rejected, and the user is notified that they're not members of that specific group.

3. Bug: Users in one group could view members of other groups
   - Problem: Users were able to see the usernames of members in groups they were not part of.
   -> Solution: Enhanced the %groupusers functionality to restrict the visibility of users to only those in the requesting user’s groups. Added a check for group membership during user list retrieval.

4. Bug: After a user left a group, other members couldn’t continue sending messages
   - Problem: Leaving a group disrupted the server's ability to manage messages for the group.
   -> Solution: Fixed the group leave functionality to properly update group membership records. Make sure that group message boards remained active for remaining members and broadcasted a notification about the user’s exit to all other group members.
