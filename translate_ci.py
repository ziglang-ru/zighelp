from re import template
import jinja2
import os
import sys
import pathlib
from os import path
import tomllib as toml
import argparse
from colorama import Fore

TRANSLATION_DIR = "./docs"
SNIPPET_DIR = "./docs/snippets/"
# files to be ignored when traversing the TRANSLATION_DIR
IGNORE_FILES = ["CNAME", "assets", "stylesheets", "snippets"]

# type aliases
# dict[language][chapter][snippet_name]
# dict["no_translation"] includes all chapters with no translations provided
SnippetsDict = dict[str, dict[str, dict[str, str]]]
# dict[chapter][template_path]
TemplateDict = dict[str, dict[str, list[str]]]


def main() -> None:
    parser = argparse.ArgumentParser(
            prog="translate_ci",
            description="expands markdown templates into their respective translations",)
    parser.add_argument('-y', '--assumeyes', help="runs script without confirmation", action="store_true")
    args = parser.parse_args()
    if not args.assumeyes:
        print(Fore.RED + f"WARNING: All translations in {TRANSLATION_DIR} will be expanded and overwritten")
        if input(Fore.RESET + "Do you want to proceed? [Yes, I want to proceed!, N] ") != "Yes, I want to proceed!":
            return

    template_dict: TemplateDict = get_template_dict()
    snippets_dict: SnippetsDict = get_rendered_snippets_dict(template_dict)

    # render files with no translations
    for language in os.listdir(TRANSLATION_DIR):
        if language in IGNORE_FILES: continue
        language_dir = path.join(TRANSLATION_DIR, language)
        for markdown in os.listdir(language_dir):
            markdown = path.join(language_dir, markdown)
            chapter = pathlib.Path(markdown).stem
            if chapter not in snippets_dict["no_translation"]: continue
            render_and_write_translation(snippets_dict, markdown, "no_translation", chapter)

    # render files with translations
    for language, chapters in snippets_dict.items():
        for chapter in chapters:
            if language == "no_translation": continue

            for chapter in chapters:
                try:
                    language_dir = path.join(TRANSLATION_DIR, language)
                    for markdown in os.listdir(language_dir):
                        markdown = path.join(language_dir, markdown)
                        render_and_write_translation(snippets_dict, markdown, language, chapter)

                except FileNotFoundError:
                    print(
                        f"Error: No snippets have been provided for {language}", file=sys.stderr)

def render_and_write_translation(snippets_dict: SnippetsDict,
                                 markdown_path: str, language: str, chapter: str) -> None:
    with open(markdown_path, "r+") as md_file:
        md_templ = jinja2.Template(md_file.read())
        md_expanded = md_templ.render(
            snippets_dict[language][chapter])
        md_file.seek(0)
        md_file.write(md_expanded)


# renders snippets and inserts them into a dictionary with the following structure
# structure of the returned dictionary: dict[language][chapter][snippet_name]
def get_rendered_snippets_dict(template_dict: TemplateDict) -> SnippetsDict:
    snippets_dict: dict[str, dict[str, dict[str, str]]] = dict()
    # all files that do not provide translation tomls are put here
    snippets_dict["no_translation"] = dict()

    for chapter, templates in template_dict.items():
        snippets_dict["no_translation"][chapter] = dict()

        for template, translations in templates.items():
            snippet_name = pathlib.Path(template).parent.stem

            with open(template, "r") as template_file:
                if len(translations) == 0:
                    snippets_dict["no_translation"][chapter][snippet_name] = template_file.read()
                    continue

                templ = jinja2.Template(template_file.read())
                for translation in translations:
                    with open(translation, "r") as translation_toml:
                        data = toml.loads(translation_toml.read())
                        language = pathlib.Path(translation).stem
                        if language not in snippets_dict:
                            snippets_dict[language] = dict()
                            snippets_dict[language][chapter] = dict()
                        snippets_dict[language][chapter][snippet_name] = templ.render(data)
    return snippets_dict


def get_template_dict() -> TemplateDict:
    translation_dict: dict[str, dict[str, list[str]]] = dict()
    for chapter in os.listdir(SNIPPET_DIR):
        chapter_path = path.join(SNIPPET_DIR, chapter)
        translation_dict[chapter] = dict()

        for section in os.listdir(chapter_path):
            section_path = path.join(chapter_path, section)
            section_files = os.listdir(section_path)

            # figure out which file is the snippet template
            template_file = ""
            for snippet in section_files:
                if snippet.endswith(".zig"):
                    template_file = path.join(section_path, snippet)
                    break

            translation_dict[chapter][template_file] = []
            # initializes dictionary with values such that
            # key: is the path for the corresponding template file (the snippet)
            # value: is a list of paths for the translation TOMLs
            for translation in section_files:
                translation_path = path.join(section_path, translation)
                if translation.endswith(".zig") or not translation.endswith(".toml"):
                    continue
                translation_dict[chapter][template_file].append(translation_path)
    return translation_dict


if __name__ == "__main__":
    main()
