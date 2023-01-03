# Importing Libraries
import serial
import time
import json

# Opening JSON file
instructions = {}

with open('python/instructions.json') as json_file:
    instructions = json.load(json_file)

print(instructions)

def find_instruction_code(x):
    commands = x.split('/')
    # go through each command inside of instructions 
    prev_instruct = instructions[commands[0]]
    for command in commands[1:]:
        if type(prev_instruct) is not dict:
            break
        else:
            prev_instruct = prev_instruct[command]
    return prev_instruct

# create arduino at serial port COM5 
arduino = serial.Serial('COM5', 9600)

def write_read(x):
    # if x is not a number, then return
    
    instruction_code = find_instruction_code(x)
    
    # write instruction code to Arduino as bytes
    arduino.write(bytes(instruction_code, 'utf-8'))
    # wait for Arduino to send back a response
    time.sleep(0.5)
    # read the response from Arduino
    data = arduino.readline()
    # print the response from Arduino
    print(data)
    return


while True:
    num = input("Enter the command: ")  # Taking input from user
    value = write_read(num)
    print(value)  # printing the value