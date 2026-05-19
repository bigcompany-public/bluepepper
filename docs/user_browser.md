# Browser

The Browser allows you to browse files related to assets and shots. To look for files :

![browser_structure](img/browser_structure.jpg)

- Select the entity type :one:
- Select your asset/shot :two:
- File Kinds :four: are regrouped under tasks :three:
- Selecting an asset/shot document and a File Kind triggers a file search: all files matching the naming convention appear in the right hand side :five:.

    !!! warning
        This also mean that files that do not **strictly** match the naming convention will **not** appear.

        ![browser_no_match](img/browser_no_match.jpg)


## Selection

Searching for files with a single document selected will reveal **all** the files for this specific document.

![browser_selection_single](img/browser_selection_single.jpg)

On the other hand, looking for files with multiple documents selected will show the **last file** found for each.

![browser_selection_multiple](img/browser_selection_multiple.jpg)

!!! tip "Selecting Multiple Documents"

    The `Documents` and `Files` columns have an extended selection mode, so various shortcuts are available:

    - `Ctrl` + `click` -> additive selection 
    - `Shift` + `click` -> contiguous selection
    - `Ctrl` + `A` -> Select all
    - `Shift` + `up/down arrow` -> Extend selection up/down
    - `Ctrl` + `Space` -> Unselect last selected item

## Filters

The Browser comes with various filtering options to help you find your documents.

### Name Filter

The name filter looks for documents names that **contain** the search string, and is case insensitive.
For instance:

- `CAT` will return `catherine` and `blackCat`
- `er` will return `terry` and `pepper`

    ![browser_filter_name](img/browser_filter_name.jpg)

!!! tip
    Multiple search strings can be used at once, using the `;` separator:

    - `CAT;ry` will return `catherine`, `blackCat`, `terry` and `curry`

### Field Filter

Field filters are here to filter documents by other attributes than their name.
The filters are in order: from the less specific to the more specific, which helps you narrow down your query.

![browser_filter_fields](img/browser_filter_fields.jpg)

### Tag Filter

Tags is a more "freeform" way of sorting documents, as opposed to fields which are mandatory hard-written attributes of documents.

Click one or more tags to reveal documents that have any of the tags assigned to them.

![tags_example](img/tags_example.jpg)

!!! tip "Selecting Multiple Tags"
    The Tag filter has an extended selection mode, so various shortcuts are available:

    - `Ctrl` + `click` -> additive selection 
    - `Shift` + `click` -> contiguous selection
    - `Ctrl` + `A` -> Select all
    - `Shift` + `left/right arrow` -> Extend selection up/down
    - `Ctrl` + `Space` -> Unselect last selected item


## Actions

Various actions can be performed on the various elements of the Browser. BluePepper comes with a few handy actions out of the box, feel free to try them out.

![browser_action_document](img/browser_action_document.jpg) ![browser_action_file](img/browser_action_file.jpg)

When clicked, actions will run for all selected documents.

Please note that some actions (mainly the time consuming ones) will actually start a Batcher job. For more informations, see the [Batcher Documentation](./user_batcher)

## Tags

!!! question "Who should manage tags ?"
    In a project involving a team, it is advised that tags are handled by supervisors: while some tags are only used for filtering, others may be used to configure actions and tools.

### Creating and Adding Tags to Documents

Tags can be added to asset/shot documents, by right clicking on it and clicking `Add Tag`.

![add_tag_0](img/add_tag_0.jpg)

You may use existing tags or create a new one if needed.

![add_tag_1](img/add_tag_1.png)

The look of the tag is fully customizable

![add_tag_2](img/add_tag_2.png)

The `Pick Icon` button pops an Icon Browser window, where you can use the search bar, and double click on the icon you want to validate your choice.

![add_tag_3](img/add_tag_3.png)

When done, simply press `OK`, and you will be able to filter documents using the newly created tag.

![add_tag_4](img/add_tag_4.png)

### Removing a Tag From a Document

Tags can be removed from a document by right clicking on the document and clicking `Remove Tag`

![remove_tag](img/remove_tag.png)

### Editing and Deleting Tags

Tags can be edited or deleted by right clicking on them.

![edit_remove_tag](img/edit_remove_tag.png)

When deleting a tag, you will be prompted if the tag is applied to one or more documents.

![remove_tag_warning](img/remove_tag_warning.png)

### Multiple Documents, Multiple Tags

Both documents and tags are in extended selection mode: you may apply multiple tags to multiple documents in one go.

![add_tag_5](img/add_tag_5.png)

### Tag Managers

The tag manager we just mentioned can also be accessed from the Launcher.

![asset_tag_manager](img/asset_tag_manager.jpg)

## Tips And Tricks

!!! tip "Prefilled Naming Conventions"
    You need to create a file, but you are unsure about its naming convention?

    The built-in `Copy Path` and `Copy File Name` actions send prefilled names that respect the naming convention into you clipboard.

    For instance, if you do this:

    ![copy_file_name](img/copy_file_name.jpg)

    pressing `Ctrl + v` will paste this: `beerCanSixPack_mdl_v{version}_{description}.blend`



!!! tip "Reading a Document's Content"
    You can hover above documents to display the full document.

    ![browser_hover_document](img/browser_hover_document.jpg)



!!! tip "Advanced Document Search"
    If you feel like a power user, the search bar also handles mongoDB queries :muscle:

    - `{"asset": "sprite"}` will return documents where the `asset` key is **exactly** "sprite"
    - `{"asset" : {"$ne" : "spider"}}` will return all documents in which the `asset` key is **not** "spider".

--- 

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Batcher](./user_batcher.md) </div>