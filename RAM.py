import sys
from RAMParser import parser


def executeFile(file, debug=False):
    with open(file, 'r') as f:
        if f.read(1):
            f.seek(0)
            data = f.read()
            try:
                instructions = parser.parse(data)
                # print(instructions)
            except Exception as inst:
                print(inst.args[0])
            try:
                print("Inputs:")
                for key in instructions[0]:
                    print("{} ==> {}".format(key, instructions[0][key]))
                registers = findRegs(instructions)
                # print("Registers: {}".format(registers))
                labels = findLabels(instructions[1])
                # print("Labels: {}".format(labels))
                print("")
                if (debug == True):
                    f.seek(0)
                    linesNoReg = grabLines(f)
                    answer = executeDebug(instructions[1], labels, registers,
                                          linesNoReg)
                    print("")
                answer = execute(instructions[1], labels, registers)
                if answer == 'ERROR':
                    print("Evaluation error.")
                else:
                    print("Output:\nR1 = {}".format(answer))
            except:
                return
        else:
            print("Empty file.")
    return


def grabLines(filePointer):
    lines = []
    for line in filePointer:
        li = line.strip()
        if not li.startswith("#"):
            lines.append(li.upper())
    linesNoReg = []
    for line in lines:
        if line.startswith("R"):
            continue
        linesNoReg.append(line)
    # print(linesNoReg)
    return linesNoReg


def execute(instructions, labels, registers):
    instructionPointer = 0
    while instructionPointer < len(instructions):
        ins = instructions[instructionPointer]
        if ins["opCode"] == "inc":
            #find register in dictionary and increment
            registers[ins["op1"]] += 1
        elif ins["opCode"] == "dec":
            #check if 0 and if so, don't decriment
            if registers[ins["op1"]] > 0:
                registers[ins["op1"]] -= 1
        elif ins["opCode"] == "clear":
            # find the register and set to 0
            registers[ins["op1"]] = 0
        elif ins["opCode"] == "continue":
            break
        elif ins["opCode"] == "jump":
            whereToJump = ins["labelInfo"][:-1]

            instructionPointer = labels[whereToJump]
            continue
        elif ins["opCode"] == "mov":
            # take value in op2 and set value of op1 to op2 value
            op2Val = registers[ins["op2"]]
            registers[ins["op1"]] = op2Val
        elif ins["opCode"] == "conJump":
            # check if op1 is 0
            if registers[ins["op1"]] == 0:
                # when it's 0, jump to the label
                whereToJump = ins["labelInfo"][:-1]
                instructionPointer = labels[whereToJump]
                continue
        else:
            return "ERROR"
        instructionPointer += 1
    return registers["R1"]


def executeDebug(instructions, labels, registers, lines):
    instructionPointer = 0
    while instructionPointer < len(instructions):
        print("Executing: {}".format(lines[instructionPointer]))
        ins = instructions[instructionPointer]
        if ins["opCode"] == "inc":
            #find register in dictionary and increment
            registers[ins["op1"]] += 1
        elif ins["opCode"] == "dec":
            #check if 0 and if so, don't decriment
            if registers[ins["op1"]] > 0:
                registers[ins["op1"]] -= 1
        elif ins["opCode"] == "clear":
            # find the register and set to 0
            registers[ins["op1"]] = 0
        elif ins["opCode"] == "continue":
            break
        elif ins["opCode"] == "jump":
            whereToJump = ins["labelInfo"][:-1]
            instructionPointer = labels[whereToJump]
            continue
        elif ins["opCode"] == "mov":
            # take value in op2 and set value of op1 to op2 value
            op2Val = registers[ins["op2"]]
            registers[ins["op1"]] = op2Val
        elif ins["opCode"] == "conJump":
            # check if op1 is 0
            if registers[ins["op1"]] == 0:
                # when it's 0, jump to the label
                whereToJump = ins["labelInfo"][:-1]
                instructionPointer = labels[whereToJump]
                continue
        else:
            return "ERROR"
        instructionPointer += 1
    return registers["R1"]


def findRegs(instructions):
    registers = {}
    keys = list(instructions[0].keys())
    for ins in instructions[1]:
        insKeys = list(ins.keys())
        if "op1" in insKeys:
            if ins["op1"] in keys:
                continue
            else:
                keys.append(ins["op1"])
                registers.update({ins["op1"]: 0})
    for key in instructions[0]:
        instructions[0][key] = int(instructions[0][key])
    registers.update(instructions[0])
    return registers


def findLabels(instructions):
    labels = {}
    for index, ins in enumerate(instructions):
        insKeys = list(ins.keys())
        if "label" in insKeys:
            labels.update({ins["label"].upper(): index})
    return labels


def main():
    if (len(sys.argv) < 2):
        print("No file passed. Please enter a file after RAM.py.")
        return
    else:
        if (sys.argv[1] == "-d"):
            executeFile(sys.argv[2], True)
        else:
            executeFile(sys.argv[1])


if __name__ == "__main__":
    main()