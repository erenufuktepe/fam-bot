class CLIParser:
    def __init__(self, mapping: dict[str, str], cls: type):
        self.mapping = mapping
        self.cls = cls

    def parse(self, tokens: str):
        data = {}

        i = 0
        while i < len(tokens):
            if tokens[i] in self.mapping:
                key = self.mapping[tokens[i]]
                value_parts = []

                j = i + 1
                while j < len(tokens) and not tokens[j].startswith("-"):
                    value_parts.append(tokens[j])
                    j += 1

                data[key] = " ".join(value_parts)
                i = j
            else:
                i += 1

        # 🟢 Burada class'ı çağırıyoruz → spesific object return
        return self.cls(**data)
