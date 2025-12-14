import os

class RLECompressor:
    def __init__(self, user_input):
        self.args = user_input.strip().split(" ", 1)

    # ---------- TEXT RLE ----------
    def compress_text(self, text):
        if not text:
            return ""

        result = ""
        count = 1

        for i in range(1, len(text)):
            if text[i] == text[i - 1] and count < 255:
                count += 1
            else:
                result += f"{text[i - 1]}:{count};"
                count = 1

        result += f"{text[-1]}:{count};"
        return result

    def decompress_text(self, text):
        result = ""
        i = 0

        while i < len(text):
            char = text[i]
            i += 2  # skip "char:"
            count = ""

            while text[i] != ";":
                count += text[i]
                i += 1

            result += char * int(count)
            i += 1

        return result

    # ---------- BINARY RLE ----------
    def compress_binary(self, data):
        compressed = bytearray()
        count = 1

        for i in range(1, len(data)):
            if data[i] == data[i - 1] and count < 255:
                count += 1
            else:
                compressed.append(count)
                compressed.append(data[i - 1])
                count = 1

        compressed.append(count)
        compressed.append(data[-1])
        return compressed

    def decompress_binary(self, data):
        decompressed = bytearray()

        for i in range(0, len(data), 2):
            count = data[i]
            byte = data[i + 1]
            decompressed.extend([byte] * count)

        return decompressed

    # ---------- FILE TYPE DETECTION ----------
    def is_text_file(self, filename):
        try:
            with open(filename, "rb") as f:
                f.read().decode("utf-8")
            return True
        except:
            return False

    # ---------- FILE HANDLING ----------
    def compress_file(self, filename):
        if not os.path.exists(filename):
            return "File not found"

        if self.is_text_file(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()

            compressed = self.compress_text(content)
            out_file = filename + ".rle"

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(compressed)

        else:
            with open(filename, "rb") as f:
                content = f.read()

            compressed = self.compress_binary(content)
            out_file = filename + ".rle"

            with open(out_file, "wb") as f:
                f.write(compressed)

        return self.report(filename, out_file)

    def decompress_file(self, filename):
        if not os.path.exists(filename):
            return "File not found"

        # Detect text or binary compressed file
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()

            decompressed = self.decompress_text(content)
            out_file = filename.replace(".rle", ".decoded")

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(decompressed)

        except:
            with open(filename, "rb") as f:
                content = f.read()

            decompressed = self.decompress_binary(content)
            out_file = filename.replace(".rle", ".decoded")

            with open(out_file, "wb") as f:
                f.write(decompressed)

        return f"Decompressed → {out_file}"

    # ---------- STATS ----------
    def report(self, original, compressed):
        orig_size = os.path.getsize(original)
        comp_size = os.path.getsize(compressed)

        ratio = (1 - comp_size / orig_size) * 100 if orig_size else 0

        return (
            f"Compressed → {compressed}\n"
            f"Original size: {orig_size} bytes\n"
            f"Compressed size: {comp_size} bytes\n"
            f"Compression ratio: {ratio:.2f}%"
        )

    # ---------- COMMAND HANDLER ----------
    def run(self):
        if len(self.args) != 2:
            return (
                "Commands:\n"
                "  compress <text>\n"
                "  decompress <text>\n"
                "  compressfile <filename>\n"
                "  decompressfile <filename>"
            )

        command, data = self.args

        if command == "compress":
            return self.compress_text(data)

        elif command == "decompress":
            return self.decompress_text(data)

        elif command == "compressfile":
            return self.compress_file(data)

        elif command == "decompressfile":
            return self.decompress_file(data)

        else:
            return "Unknown command"


# -------- Main --------
user_input = input("RLEc~$ ")
tool = RLECompressor(user_input)
print(tool.run())
