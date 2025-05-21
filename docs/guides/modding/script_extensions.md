---
description: Script extensions are the preferred way to change, extend and replace behavior of an existing vanilla script.
status: new
---

# Script Extensions

Script extensions are the preferred way to change, extend and replace behavior of an existing vanilla script.

It works by registering an entire file of new script functions as a child script of a vanilla script. Not all methods 
from the original script need to be in the extension script.

Extensions are based on [inheritance](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#inheritance), 
which is a concept from object-oriented programming. It is recommended that you know a bit about [classes](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#classes) 
and [inheritance](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#inheritance) before delving deeper. 
Note that we won't be making much use of custom named classes, we'll mostly be using inheritance to extend a functions
logic and then let the mod loader replace the vanilla script with our custom one. 

!!! abstract "See also" 
    [API Reference: `#!gd ModLoaderMod.install_script_extension()`](../../api/mod_loader_mod.md#method-install_script_extension)

## Features

**Multiple mods can mod the same functions** and their changes will accumulate rather than replacing each other (depending on load order).

Extensions can **change vanilla methods before and after** they are called, which allows them to 
**manipulate both the input parameters and the output value of a function**. They can also **completely replace** 
vanilla functions, but be aware that that may reduce compatibility, especially with other mods that change 
the same function.

Since we are working with standard inheritance, we can also **add new member variables and functions** to the classes that 
we extend. 

Script extensions **can also be applied to [Autoloads](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html)**, 
if the ModLoader autoload is higher in the load order. You can check the autoload order by setting the mod loader 
[log level](testing_debugging.md#logging-and-other-handy-options) to DEBUG and checking the log. 


This example script extension changes the path that save files are loaded from in the game Brotato.  
The path of this script extension would be, by convention, in the `/extensions` folder and then mirroring the 
vanilla file structure: `res://mods-unpacked/Author-ModName/extensions/singletons/progress_data.gd`

=== "Godot 4"

    ```geedee
    # Our base script is the original game script.
    extends "res://singletons/progress_data.gd"
    
    # This overrides the method with the same name, changing the value of its argument:
    func load_game_file(path: String = SAVE_PATH) -> void:
        var modded_path = path + "--modded.json"
    
        # Calling the base method will call the original game method:
        super(modded_path)
    
        # Note that if the vanilla script returned something, we would do this instead:
        #return super(modded_path)
    ```

=== "Godot 3"

    ```gdscript
    # Our base script is the original game script.
    extends "res://singletons/progress_data.gd"
    
    # This overrides the method with the same name, changing the value of its argument:
    func load_game_file(path: String = SAVE_PATH) -> void:
        var modded_path = path + "--modded.json"
    
        # Calling the base method will call the original game method:
        .load_game_file(modded_path)
    
        # Note that if the vanilla script returned something, we would do this instead:
        #return .load_game_file(modded_path)
    ```

The above example showed how to call the base method by using `#!gd super()` or the `.` prefix in Godot 3. 

It changes the input values for the base function before calling it. Similarly, it is also possible to manipulate the 
output value by calling the base method first, changing something and then returning that new value, as shown below:

=== "Godot 4"

    ```gdscript
    func get_playtime_days() -> int:
        var days = super()
        return days + 2
    ```

=== "Godot 3"

    ```gdscript
    func get_playtime_days() -> int:
        var days = .get_playtime_days()
        return days + 2
    ```

Since we are extending the vanilla base class, not calling the base method would completely replace the method. 
But, because all methods from each mod in the load order extend each other in a chain, 
doing this would break the chain and usually cause conflicts between mods.

To install it, call [`#!gd ModLoaderMod.install_script_extension()`](../../api/mod_loader_mod.md#method-install_script_extension) 
from your mod's `mod_main.gd`, in `#!gd _init()` or in any function that gets called 
by `#!gd _init()`, like the `#!gd install_script_extensions()` functions we usually use by convention.

```gdscript
extends Node

func _init():
	install_script_extensions()

func install_script_extensions() -> void:
    ModLoaderMod.install_script_extension('res://mods-unpacked/Author-ModName/extensions/singletons/progress_data.gd')
```


## Limitations

Script Extensions **will not be applied to scripts that are 
[`preload()`ed](https://docs.godotengine.org/en/stable/classes/class_%40gdscript.html#class-gdscript-method-preload "preload() is a GDScript feature")** 
in any way. This affects both scripts which are preloaded directly - `#!gd preload("res://player.gd")` - and scripts which are
indirectly preloaded by being used in preloaded scenes - `#!gd preload("res://player.tscn")`.   
This is a Godot limitation we have yet to find a complete workaround for.  
For scenes there can be a way to circumvent this limitation by extending the scene that instantiates it. For example,
the pause menu in dome keeper was preloaded and instantiated from another scene. The other scene was extended, which 
allowed accessing the nodes within the pause menu after it was created, as well as adding new nodes to it.

=== "Godot 4"

    **Extending global classes (scripts with `class_name` at the top) is not possible**. 
    To work around this issue, we've created [Script Hooks](script_hooks.md), use them instead of 
    extensions when necessary.

    !!! bug "Related Godot Issue"
        [#83542](https://github.com/godotengine/godot/issues/83542)

=== "Godot 3"

    It is **not possible to replace [virtual functions](https://docs.godotengine.org/en/3.5/tutorials/scripting/overridable_functions.html)** 
    with a script extension, since the function from the base class will always be called by Godot.
    Because of this, using `._ready()` - the `_ready()` function of the base class - in a script extension will result 
    in that function being called twice.

    ???+ info
        Virtual functions, like `_ready()` or `_init()`, are used to execute code when specific "events", also called 
        "notifications", occur. You can learn more about them in the 
        [Godot Documentation](https://docs.godotengine.org/en/3.5/tutorials/scripting/overridable_functions.html).

    !!! bug "Related Godot Issue"
        [#33620](https://github.com/godotengine/godot/issues/33620#issuecomment-553912225)


You **can't redefine or overwrite member variables** in inheriting scripts. That's simply due to how inheritance works in Godot.  
This can usually be worked around by using a function like _ready or _init to change their value ahead of time, or by
extending the function that uses the variable and changing the value before calling the base method.

There is currently **no way to insert code into the middle of a function**. In the best case scenario, functions are kept 
small, or you can ask the developer to split the function into smaller parts for the next update. If that fails, you can
copy the vanilla method in its entirety and insert your code in the middle. This is the same as replacing a function 
completely though, so your mod will be less compatible with other mods. Additionally, if the game developer changes that
function in an update, you will have to update your function to that new code too, or you risk the game breaking or 
reintroducing old bugs.

**Constants** do what they should, so they **can't be changed or overwritten**. Unless the constant holds an Array, in which 
case the variable can't be reassigned, but the values within can change without problem. 
Dictionaries are in a similar situation, where the dict values can change freely, but the keys are fixed. 


## Technical Details

### Script Inheritance
!!! info 
     This info comes from the docs for the [Delta-V mod loader](https://gitlab.com/Delta-V-Modding/Mods/-/blob/main/MODDING.md) for a full write-up check this [blog post](https://blog.cy.md/2022/05/27/modding-for-godot/).

In order to allow modifying game functions without copying the contents of the functions or entire scripts in mod code, 
this system makes use of inheritance for hooking. We exploit the fact that all Godot scripts are also classes and may 
extend other scripts in the same way how a class may extend another class; this allows mods to include script extensions, 
which extend some standard game script and selectively override some methods.

### Inheritance chaining
By using `install_script_extension`, the Mod Loader builds a chain of scripts which are applied one by one. 
The order of the chain is determined by the [`manifest.json`](mod_files.md#manifestjson) fields 
`dependencies`, `optional_dependencies` and `load_before`. 

If these fields are set correctly, multiple mods should "just work" together without any additional work.
