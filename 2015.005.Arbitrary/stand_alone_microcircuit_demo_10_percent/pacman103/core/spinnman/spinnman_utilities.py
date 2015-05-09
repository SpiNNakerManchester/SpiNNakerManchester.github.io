__author__ = 'stokesa6'
import os

class SpinnmanUtilities(object):

    def __init__(self, dao=None, input_file=None):
        self.runtime = None
        self.total_processors = None
        self.app_loads = list()
        self.mem_writes_from_file = list()
        self.mem_writes = list()
        if dao is not None:
            directory = dao.get_reports_directory("transceiver_commands")
            self.output_file = os.path.join(directory, "transceiver_commands")
            self.output = open(self.output_file, "wb")
            self.output_data = list()
        if input_file is not None:
            self.read_in_file(input_file)

    def write_extra_data(self, runtime, total_processors):
        self.output_data.insert(0, "TOTAL_PROCESSORS:{}:".format(total_processors))
        self.output_data.insert(0, "RUNTIME:{}:".format(runtime))


    # different types of writes
    def write_app_load_command(self, filename, region, core_part_of_region, app_id):
        self.output_data.append("APPLOAD:{}:{}:{}:{}:".format(filename, region,
                                                             core_part_of_region,
                                                             app_id))

    def write_selects(self, x, y, p):
        self.output_data.append("SELECT:{}:{}:{}:".format(x, y, p))

    def write_mem_from_file(self, address, type_word, filename):
        self.output_data.append("WRITE_MEM_FROM_FILE:{}:{}:{}:".
                                format(address, int(type_word), filename))

    def write_mem(self, address, type_word, structure):
        self.output_data.append("WRITE_MEM:{}:{}:{}:".
                                format(address, int(type_word), structure))

    def close(self):
        for line in self.output_data:
            self.output.write(line + "\n")
        self.output.flush()
        self.output.close()

    def get_run_time(self):
        return self.runtime

    def get_total_processors(self):
        return self.total_processors

    def get_app_loads(self):
        return self.app_loads

    def get_mem_writes(self):
        return self.mem_writes

    def get_mem_writes_from_file(self):
        return self.mem_writes_from_file

    def read_in_file(self, input_file):
        inputfile = open(input_file, "r")
        content = inputfile.readlines()
        self.runtime = content[0].split(":")[1]
        self.total_processors = content[1].split(":")[1]
        self.app_loads = list()
        data = None
        line = 0
        for line in range(2, len(content)):
            bits = content[line].split(":")
            if bits[0] == "APPLOAD":
                data = dict()
                data['filename'] = bits[1]
                data['region'] = bits[2]
                data['core_part_of_region'] = bits[3]
                data['app_id'] = bits[4]
                self.app_loads.append(data)
            elif bits[0] == "SELECT":
                data = dict()
                data['x'] = bits[1]
                data['y'] = bits[2]
                data['p'] = bits[3]
            elif bits[0] == "WRITE_MEM":
                self.mem_writes.append(data)
                data = dict()
                data['address'] = bits[1]
                data['type_word'] = bits[2]
                data['structure'] = bits[3]
                self.mem_writes.append(data)
            elif bits[0] == "WRITE_MEM_FROM_FILE":
                self.mem_writes_from_file.append(data)
                data = dict()
                data['address'] = bits[1]
                data['type_word'] = bits[2]
                data['filename'] = bits[3]
                self.mem_writes_from_file.append(data)


