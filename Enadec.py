class Enadec:
    def __init__(self, user_input):
        self.letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        self.numbers = [str(i) for i in range(10)]
        self.args = user_input.strip().split(" ", 1)

    def encode(self, text):
        text = text.lower()
        encoded = []

        for char in text:
            if char in self.letters:
                encoded.append(format(self.letters.index(char) + 1, "05b"))
            elif char in self.numbers:
                encoded.append(format(int(char), "04b"))
            elif char == " ":
                encoded.append("/")
            elif char == ".":
                encoded.append("|")
            else:
                encoded.append("?")

        return " ".join(encoded)

    def decode(self, binary_text):
        decoded = ""
        parts = binary_text.split()

        for part in parts:
            if part == "/":
                decoded += " "
            elif part == "|":
                decoded += "."
            elif part.isdigit() and len(part) == 5:
                decoded += self.letters[int(part, 2) - 1]
            elif part.isdigit() and len(part) == 4:
                decoded += str(int(part, 2))
            else:
                decoded += "?"

        return decoded

    def run(self):
        if len(self.args) != 2:
            return "Invalid input. Use: encode <text> or decode <binary>"

        command, data = self.args

        if command == "encode":
            return self.encode(data)
        elif command == "decode":
            return self.decode(data)
        else:
            print("Unknown command. Use 'encode' or 'decode'")


while True:
  user_input = input("Enadec~$ ")
  if user_input == "cd defthon":
    break
  elif user_input == "help":
    print("Usage: encode <words> to encode, decode <binary> to decode")
  else:
    encoder = Enadec(user_input)
    print(encoder.run())
    
