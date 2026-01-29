import numpy as np

class DataLoader:
    def __init__(self, doc=r"../Data/measurements.txt"):
        self.doc = doc
        self.data = None
        self.headers = None
        self._loaded = False

    def _load_data(self):
        if not self._loaded:
            print(">> Laddar filen nu (lazy load)...")
            with open(self.doc, "r") as f:
                header_line = next(f).strip().lstrip("#").split()
                headers = []
                skip_next=False
                for i, h in enumerate(header_line):
                    if skip_next:
                        skip_next = False
                        continue
                    if i + 1 < len(header_line) and header_line[i+1].startswith("("):
                        headers.append(h + header_line[i+1])
                        skip_next = True
                    else:
                        headers.append(h)
                self.headers = headers
                
                lines = [line.strip().split() for line in f if not line.startswith("#")]
                self.data = np.array(lines, dtype= float)
                self._loaded = True

    def get_rows(self):
        self._load_data()
        return self.data
    
    def get_column(self, key):
        self._load_data()
        if isinstance(key, int):
            return self.data[:, key]
        elif isinstance(key, str):
            if key in self.headers:
                idx = self.headers.index(key)
                return self.data[:, idx]
            else:
                raise ValueError(f"Header '{key}' finns inte.")
        else:
            raise TypeError("Key måste vara int (index) eller str (header-namn).")
    
    def get_header_index(self, header_name):
        self._load_data()
        if self.headers is None:
            raise ValueError("Data ej laddat ännu.")
        return self.headers.index(header_name)
    
    def pretty_print(self, num_rows=5):
        self._load_data()
        if self.headers is None or self.data is None:
            raise ValueError("Data ej laddat ännu")
        
        col_width = 12
        header_line = " | ".join(f"{h:>{col_width}}" for h in self.headers)
        print(header_line)
        print("-" * len(header_line))
        
        for row in self.data[:num_rows]:
            row_line = " | ".join(f"{val:{col_width}.3f}" for val in row)
            print(row_line)

    
if __name__ == "__main__":
    loader = DataLoader()
    print(loader._loaded)
    loader.pretty_print(num_rows=10)
    print(loader._loaded)
