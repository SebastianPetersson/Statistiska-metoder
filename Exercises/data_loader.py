import numpy as np

class DataLoader:
    def __init__(self, doc):
        self.doc = doc
        self.data = None
        self.headers = None

    @classmethod 
    def read_file(cls, filepath=None):
        if filepath is None:
            filepath = "../Data/measurements.txt"

        return cls(filepath)
    
    def load_data(self):
        with open(self.doc, "r") as f:
            header_line = next(f).strip().lstrip("#").split()
            self.headers = [h for h in header_line if not h.startswith("(")]

            lines = [line.strip().split() for line in f if not line.startswith("#")]
            self.data = np.array(lines, dtype=float)

    def get_rows(self):
        return self.data
    
    def get_column(self, key):
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
        if self.headers is None:
            raise ValueError("Data ej laddat ännu.")
        return self.headers.index(header_name)
    
    def pretty_print(self, num_rows=5):
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
    loader = DataLoader.read_file()
    loader.load_data()
    loader.pretty_print(num_rows=10)
