import os


def extract_files_content(root_dir, output_file, target_files):
    """
    提取指定目录及其子目录中目标文件的内容，并保存到txt文件中。

    :param root_dir: 要搜索的根目录
    :param output_file: 输出的txt文件路径
    :param target_files: 目标文件名列表
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for file in filenames:
                if file in target_files:
                    file_path = os.path.join(dirpath, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                        outfile.write(f"### {file_path}\n\n")
                        outfile.write(content + "\n\n")
                    except Exception as e:
                        print(f"无法读取文件 {file_path}: {e}")


if __name__ == "__main__":
    # 根目录
    root_directory = "./order/"  # 替换为你的目标目录
    # 输出文件路径
    output_txt_file = "extracted_files_content.txt"
    # 目标文件名列表
    target_file_names = ["serializers.py", "views.py", "urls.py"]

    extract_files_content(root_directory, output_txt_file, target_file_names)
    print(f"文件内容已提取到 {output_txt_file}")
