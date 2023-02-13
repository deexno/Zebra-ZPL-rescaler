import inquirer
from inquirer.themes import GreenPassion

# pip install inquirer

scalable_cmds = [
    "A0",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "B3",
    "B7",
    "BC",
    "BQ",
    "BY",
    "FB",
    "FO",
    "FT",
    "GB",
    "LH",
    "LH",
    "LL",
    "LS",
    "LT",
    "PW",
]
available_zpl_resolutions = [152, 203, 300, 600]


def rescale_zpl_file(
    src_file_path,
    dst_file_path,
    current_resolution,
    desired_resolution,
):
    zpl_file = open(src_file_path, "r")
    new_zpl_file = open(dst_file_path, "w")

    for line in zpl_file.readlines():
        scaled_sections = []

        for section in line.split("^"):
            scaled_sections.append(
                scale_section(section, desired_resolution / current_resolution)
            )

        new_zpl_file.write("^".join([str(elem) for elem in scaled_sections]))

    new_zpl_file.close()


def scale_section(section_value, scale_factor):
    if any(section in section_value for section in scalable_cmds):
        cmd = section_value[:2]
        section_parts = section_value[2:].split(",")

        for section_part in section_parts:
            if section_part.isnumeric():
                rescaled_part = int(round(float(section_part) * scale_factor))
                cmd = f"{cmd}{rescaled_part},"
            else:
                cmd = f"{cmd}{section_part},"

        return cmd[:-1]
    else:
        return section_value


questions = [
    inquirer.List(
        "current_resolution",
        message="What is the resolution of the current ZPL file?",
        choices=available_zpl_resolutions,
        default=203,
    ),
    inquirer.List(
        "desired_resolution",
        message="What is your desired new ZPL file resolution?",
        choices=available_zpl_resolutions,
        default=300,
    ),
    inquirer.Path(
        "source_file_path",
        message="What is the current file path of the ZPL file?",
        exists=True,
        path_type=inquirer.Path.FILE,
    ),
    inquirer.Path(
        "destination_file_path",
        message="What is the destination file path of the ZPL file?",
        exists=False,
        path_type=inquirer.Path.FILE,
    ),
]
answers = inquirer.prompt(questions, theme=GreenPassion())

rescale_zpl_file(
    answers["source_file_path"],
    answers["destination_file_path"],
    int(answers["current_resolution"]),
    int(answers["desired_resolution"]),
)
