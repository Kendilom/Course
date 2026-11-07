import logging
from datetime import datetime


KEY = "TSTFEED0300|7E3E|0400"

logging.basicConfig(
        filename="hb_test.log",
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s: %(message)s",
        filemode="w"
)


def heartbeat_log(input_file):
    filtered_log = []
    with open(input_file, "r") as file:
        for line in file:
            if KEY in line:
                filtered_log.append(line.strip())

    timestamps = []

    for line in filtered_log:
        pos = line.find("Timestamp ")
        time = line[pos + len("Timestamp "):pos + len("Timestamp ") + 8]
        timestamp = datetime.strptime(time, "%H:%M:%S")
        timestamps.append((timestamp, time))

    for i in range(len(timestamps) - 1):
        current_time, current_string = timestamps[i]
        next_time, next_string = timestamps[i + 1]

        interval = (current_time - next_time).total_seconds()

        if 31 < interval < 33:
            logging.warning(f'Thread {KEY}: Interval: {interval:.0f} seconds; timestamps: {current_string} -> {next_string} ')
        elif interval >= 33:
            logging.error(f'Thread {KEY}: Interval: {interval} seconds; timestamps: {current_string} -> {next_string} ')

    return "hb_test.log"


if __name__ == "__main__":
    result = heartbeat_log("hblog.txt")


