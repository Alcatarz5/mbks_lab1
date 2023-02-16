from file_worker import read_file, write_to_file


def command_help() -> None:
    print(
        "To read files - read <filename> \n"
        + "To write in file - write <filename> <text> \n"
        + "To grand rights - grand <filename> <user> <rights in format <**> where 0-deny, 1-accept> \n"
        + "To exit app - exit"
    )


def split_command(command_line: str) -> list:
    return command_line.split(" ")


def is_exit(command: str) -> bool:
    if command == "exit":
        return True
    else:
        return False


def is_valid_command(command_line: str) -> bool:
    command = split_command(command_line)
    if len(command) == 2:
        if command[0] == "read" or command[0] == "delete":
            return True
    elif len(command) == 3:
        if command[0] == "create" or command[0] == "change":
            return True
    else:
        print("Такой команды нет")
        return False


def write_command(user: str) -> None:
    command_line = input()
    while not is_valid_command(command_line):
        command_line = input()
        if command_line == "exit":
            return
    command = split_command(command_line)
    match command[0]:
        case "read":
            read_file(user=user, object_name=command[1])
        case "write":
            write_to_file(user=user, object_name=command[1], data=command[2])
