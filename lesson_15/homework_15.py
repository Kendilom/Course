from pathlib import Path
import logging
import json
import xml.etree.ElementTree as ET

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filename='json_Rafalsky.log',
    filemode='w'
)
logger = logging.getLogger('admin')


work_dir = Path.cwd().parent
def task1():
    files = []
    path = Path(r'C:\Users\25032\PycharmProjects\Course\ideas_for_test\ideas_for_test\work_with_csv')
    files = list(path.glob("*.csv"))
    for file in files:
        duplicate = False

        for unique in files:
            if file.read_bytes() == unique.read_bytes():
                duplicate = True
                break

        if not duplicate:
            files.append(file)

    with open("result_Rafalsky.csv", "w+") as result:
        for file in files:
            result.write(f"{file.name}\n")

task1()

def task2():
    path = Path(r'C:\Users\25032\PycharmProjects\Course\ideas_for_test\ideas_for_test\work_with_json')
    for file in path.iterdir():
        if file.suffix == '.json':
            try:
                with file.open('r', encoding='utf-8') as f:
                    json.load(f)
                logger.info(f'File {file.name} is valid')
            except json.JSONDecodeError:
                logger.error(f'File {file.name} is invalid')
task2()


def task3(group_number):
    path = Path(r'C:\Users\25032\PycharmProjects\Course\ideas_for_test\ideas_for_test\work_with_xml\groups.xml')
    root = ET.parse(path).getroot()

    for group in root.findall('group'):
        number = group.find('number')
        incoming = group.find('timingExbytes/incoming')

        if number is not None and incoming is not None:
            logger.info(f'Group {number.text}: Incoming = {incoming.text}')

    return None

task3(2)






