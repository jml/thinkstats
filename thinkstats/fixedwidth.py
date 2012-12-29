import gzip


def open_file(path):
    """Open file at 'path', decompressing if needed."""
    if path.endswith('.gz'):
        return gzip.open(path)
    else:
        return open(path)


def parse_line(fields, line):
    parsed = {}
    for (name, start, end, parser) in fields:
        value = None
        field = line[start - 1:end].strip()
        if field:
            try:
                value = parser(field)
            except ValueError:
                raise ValueError("Could not parse field %r: %r" % (name, field))
        parsed[name] = value
    return parsed


def parse_file(file_obj, fields):
    for line in file_obj:
        yield parse_line(fields, line)


def fixed_width_to_csv(in_file, fields, out_file):
    w = out_file.write
    columns = [f[0] for f in fields]
    w(','.join(columns))
    w('\n')
    for parsed in parse_file(in_file, fields):
        w(','.join(str(parsed[col]) for col in columns))
        w('\n')
