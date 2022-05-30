import csv


class BufferedWriter (object):
    def __init__ (self, f, buffer_size=100, csv_dialect="excel-tab"):
        self._buffer = []
        self._buffer_size = buffer_size
        self._writer = csv.writer(f, csv_dialect)
    
    def __del__ (self):
        self.flush()

    def flush (self):
        self._writer.writerows(self._buffer)
        self._buffer = []
        
    def writerow (self, row):
        self._buffer.append(row)
        
        if len(self._buffer) > self._buffer_size:
            self.flush()
            
    def writerows (self, rows):
        for row in rows:
            self.writerow(row)
        self.flush()


class DictWriter (object):
    
    def __init__ (self, f, columns, encoding="utf-8", **kwds):
        self._encoding = encoding
        self._writer = csv.DictWriter(f, columns, **kwds)
    
    def writeheader (self):
        self._writer.writeheader()
    
    def writerow (self, row):
        if row != None:
            encoded_row = {}
            for key, value in row.items():
                encoded_row[key] = value
            self._writer.writerow(encoded_row)

    def writerows (self, rows):
        for row in rows:
            self.writerow(row)


class DictReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, encoding="utf-8", **kwds):
        self._encoding = encoding
        self._reader = csv.DictReader(f, **kwds)

    @property
    def fieldnames (self):
        fields = self._reader.fieldnames
        if fields != None:
            return [field.decode(self._encoding) for field in fields]
        return []

    def next(self):
        row = {}
        for key, value in self._reader.next().items():
            decoded_key = key.decode(self._encoding)
            if not value is None:
                row[decoded_key] = value.decode(self._encoding)
            else:
                row[decoded_key] = None
            
        return row

    def __iter__(self):
        return self


class Reader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, encoding="utf-8", **kwds):
        self._encoding = encoding
        self._reader = csv.reader(f, **kwds)

    @property
    def fieldnames (self):
        header_row = self.next()
        return header_row

    def next(self):
        row = []
        for value in self._reader.next():
            if not value is None:
                row.append(value.decode(self._encoding))
            else:
                row.append(None)
            
        return row

    def __iter__(self):
        return self
