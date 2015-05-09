import logging
import math
import os
import subprocess

from pacman103.core import exceptions
logger = logging.getLogger(__name__)


def send_ybug_command(hostname, command_string):
    """Create an instance of `ybug` and use it to execute the given command
    string.
    """
    p = subprocess.Popen(
        ["ybug", hostname],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (out, err) = p.communicate(command_string + "\nquit")

    if "error" in out:
        raise Exception("STDOUT=\n%s\n\nSTDERR=\n%s" % (out, err))


class Utility(object):

    def __init__(self):
        logger.debug("initlising a utility object for scp")


    def parse_region(self, region, chip_x, chip_y):
        '''
        takes a region and checks its in the correct format and converts if needed
        '''
        # if no region defined, return 0
        if region is None:
            raise exceptions.SpinnManException("no region was defined")

        # if current region
        if region == "." or str(region).partition(",")[1] == ",":
            # if no x and y corrds defined, return 0
            if chip_x is None and chip_y is None:
                raise exceptions.SpinnManException("no chip coords were "
                                                   "supplied for parsing region")
            else:
                # return some number (no idea what this actually computes)
                m = (chip_y & 3) * 4 + (chip_x & 3)
                return ((chip_x & 252) << 24) + ((chip_y & 252) << 16) + \
                       (3 << 16) + (1 << m)

        # if a region defined as a coord
        if str(region).partition(",")[1] == ",":
            bits = str(region).partition(",")
            x = [0]
            y = [2]
            m = (x & 3) * 4 + (y & 3)
            return ((x & 252) << 24) + ((y & 252) << 16) + (3 << 16) + (1 << m)

        # if all is defined, change to 0-15
        if region.lower() == "all":
            region = "0-15"

        #check that the region is in the correct format
        region_bits = region.split(".")
        number_of_levels = len(region_bits) - 1
        if number_of_levels < 0 or number_of_levels > 3:
            raise exceptions.SpinnManException("the region given did"
                                               " not have enough levels")

        x, y = 0, 0
        for level in range(number_of_levels):
            d = int(region_bits[level])
            if d > 15 and d < 0:
                raise exceptions.SpinnManException("the region requested does "
                                                   "not exist. out of bounds")

            shift = 6 -2 * level

            x += (d & 3) << shift
            y += (d >> 2) << shift

        mask = self.parse_bits(region_bits[-1], 0, 15)

        if mask is None:
            raise exceptions.SpinnManException("no mask was supplied "
                                               "for parsing a region")

        return (x << 24) + (y << 16) + (number_of_levels << 16) + mask

    def parse_apps(self, app_id, app_range):
        if app_range is None:
            return 255
        elif app_range < 1:
            raise exceptions.SpinnManException("range is less than 1, "
                                    "a app region must be positive")
        elif app_id % app_range != 0:
            raise exceptions.SpinnManException("range % app_id must equal 0")
        elif app_id + app_range > 255:
            raise exceptions.SpinnManException("range + app_id must not go above 255")

        return 255 & ~(app_range - 1)



    def parse_bits(self, mask, min_core_id, max_core_id):
        '''
        parses the bits or converts if required
        '''
        if mask is None:
            raise exceptions.SpinnManException("no mask was supplied "
                                               "for parsing a region")
        if mask.lower() == "all":
            mask = "{}-{}".format(min_core_id, max_core_id)

        node_range = mask.split(",")
        mask = 0
        for sub in node_range:
            if sub.isdigit():
                if int(sub) < min_core_id or int(sub) > max_core_id:
                    return 0
                else:
                    mask |= 1 << int(sub)
            else:
                bits = sub.split("-")
                if len(bits) == 2:
                    l, h = bits[0], bits[1]
                    if int(l) > int(h) or int(l) < min_core_id or int(h) > max_core_id:
                        return 0
                    else:
                        for i in range(int(l), int(h)+1):
                            mask |= 1 << i
                else:
                    return 0
        return mask

    def parse_cores(self, cores):
        '''
        parses cores by bit
        '''
        return self.parse_bits(cores, 1, 17)



    def read_file(self, file_name, max_length=65536):
        '''
        reads a binary file to convert to memory for the scp messages
        '''
        statinfo = os.stat(file_name)
        if statinfo.st_size >= 65536:
            raise exceptions.SpinnManException("file too big to "
                                               "be written to a core")

        try:
            file = open(file_name, 'rb')
            buf = file.read(statinfo.st_size)
            file.close()
            return buf
        except Exception as e:
            print "failed to read the file at {}".format(file_name)


    @staticmethod
    def calculate_region_id(x, y):
        level_0 = 4 * (math.floor(y / 64))
        level_0 += math.floor(x / 64)
        x_offset = x - (64 * math.floor(x / 64))
        y_offset = y - (64 * math.floor(y / 64))
        level_1 = 4 * (math.floor(y_offset / 16))
        level_1 += math.floor(x_offset / 16)
        x_offset -= 16 * math.floor(x_offset / 16)
        y_offset -= 16 * math.floor(y_offset / 16)
        level_2 = 4 * (math.floor(y_offset / 4))
        level_2 += math.floor(x_offset / 4)
        x_offset -= 4 * math.floor(x_offset / 4)
        y_offset -= 4 * math.floor(y_offset / 4)
        level_3 = 4 * (math.floor(y_offset / 1))
        level_3 += math.floor(x_offset / 1)
        x_offset -= 1 * math.floor(x_offset / 1)
        y_offset -= 1 * math.floor(y_offset / 1)
        return "{}.{}.{}.{}".format(int(level_0), int(level_1),
                                    int(level_2), int(level_3))









