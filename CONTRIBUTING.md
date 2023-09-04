# How to contribute to ZigHelp
### Adding translations
Translations are located in a directory in `docs/`. Say `docs/en/` for English.
The language directory should contain all translations matching the files found in [docs/en/](https://github.com/zighelp/zighelp/tree/master/docs/en) (the reference documentation).

Translations include templates for snippets in the form `{{ some_snippet }}`, this is to make sure that all snippets are tested and can be updated once and be reflected everywhere as Zig itself evolves. All snippets go into `docs/snippets`.

The `docs/snippets` directory follows the following structure.
```
section
└── my_snippet
    ├── my_snippet.zig
    ├── ru.toml
    ├── pt.toml
    └── en.toml
```
Where `section` would be the `docs/en/section.md` file's snippets and the `my_snippet` would be the name of that snippet.
The `my_snippet.zig` is a regular file that can contain templates and the TOML files contain the templates for each language.

Source file example:
```
// {{ my_comment }}
pub fn do_something() void {}
```
In the TOML file this would be:
```toml
my_comment = "This is my comment"
```
