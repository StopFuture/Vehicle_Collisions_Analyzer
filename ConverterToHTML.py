class ConverterToHTML:
    def __init__(self, name):
        self.source = name[:-4]
        self.status = 0

    def set_source(self, name):
        self.source = name
        return self.source

    def create_html(self, data, name):
        self.source = name
        res = data.to_html()
        text_file = open(name + ".html", "w")
        text_file.write(res)
        text_file.close()

    def modify(self, updated):
        try:
            cnt = 0
            text_file = open(self.source + ".html", "r")
            info = text_file.read()
            for char1, char2 in zip(info, updated):
                if char1 != char2:
                    cnt += 1

            if 2 * cnt > len(info):
                new_file = open(self.source + ".html", "w")
                new_file.write(updated)
                new_file.close()
                self.status = 1
        finally:
            return self.status
