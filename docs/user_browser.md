# Browser

The Browser allows you to browse files related to assets and shots. To look for files :

![browser_structure](img/browser_structure.jpg)

- Select the entity type (`1`)
- Select your asset/shot (`2`)
- File Kinds (`4`) are regrouped under tasks (`3`)
- Selecting an asset/shot document and a File Kind triggers a file search: all files matching the naming convention appear in the right hand side (`5`).

:warning:**Warning:** This also mean that files that do not **strictly** match the naming convention will **not** appear.

![browser_no_match](img/browser_no_match.jpg)

## Selection

Searching for files with a single document selected will reveal **all** the files for this specific document.

![browser_selection_single](img/browser_selection_single.jpg)

On the other hand, looking for files with multiple documents selected will show the **last file** found for each.

![browser_selection_multiple](img/browser_selection_multiple.jpg)

The `Documents` and `Files` columns have an extended selection mode, so various shortcuts are available:
- `Ctrl` + `click` -> additive selection 
- `Shift` + `click` -> contiguous selection
- `Ctrl` + `A` -> Select all
- `Shift` + `up/down arrow` -> Extend selection up/down
- `Ctrl` + `Space` -> Unselect last selected item

## Filters

The Browser comes with various filtering options to help you find your documents.

### Name Filter

The name filter looks for documents names that *contain* the search string, and is case insensitive.\
For instance:

- `CAT` will return `catherine` and `blackCat`
- `er` will return `terry` and `pepper`

![browser_filter_name](img/browser_filter_name.jpg)

Multiple search strings can be used at once, using the `;` separator:

- `CAT;ry` will return `catherine`, `blackCat`, `terry` and `curry`

### Field Filter

Field filters are here to filter documents by other attributes than their name.
The filters are in order: from the less specific to the more specific, which helps you narrow down your query.

![browser_filter_fields](img/browser_filter_fields.jpg)

### Tag Filter

*(Coming soon. the Tag feature has not been released yet.)*

## Actions

Various actions can be performed on the various elements of the Browser. BluePepper comes with a few handy actions out of the box, feel free to try them out.

![browser_action_document](img/browser_action_document.jpg) ![browser_action_file](img/browser_action_file.jpg)

## Tips And Tricks

:bulb:You can hover above documents to display the full document.

![browser_hover_document](img/browser_hover_document.jpg)

:bulb:This option is more advanced, but if you know what you are doing, you can write a MondoDB query as a filter:
- `{"asset" : "cat"}` will return `cat` but **not** `blackCat`
