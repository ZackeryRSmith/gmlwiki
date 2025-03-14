---
description: Learn how to setup Godot Mod Loader for your game.
---

# Godot Project Setup
If you don't have your project set up yet, see [Decompiling Games](../modding/tools/decompile_games.md) and [GodotSteam](../modding/tools/godot_steam.md).

## Installing The Mod Loader

!!! info
    Download links for GitHub and the Godot Asset Lib can be found on the [Home Page](../../index.md). If you use the asset
    lib download you can skip step 1.

1. After downloading, create a new `/addons` folder, and add the *mod_loader* and *JSON_Schema_Validator* folder to it.
2. Add `mod_loader.gd` and `mod_loader_store.gd` to your project's Autoload settings:
	- Project > Project Settings > Global (Autoload in previous versions)
	- At the top left, click the folder icon next to Path. Browse to *res://addons/mod_loader/mod_loader.gd* and select it.
	- At the top right, `ModLoader` will be shown in the "Node Name" field. Click Add.
	- Repeat the above steps for *mod_loader_store.gd*
3. Reorder the autoloads so that `ModLoaderStore` is at the top and `ModLoader` is in the second spot.

    ???+ note 
    
        The ModLoader autoloads must be placed at the top of the autoload list to ensure they can affect other autoloads/singletons. In certain cases, you may want to make modding of an autoload more difficult, such as for cheat detection. In such cases, you can use the `allow_modloader_autoloads_anywhere` setting. Read more about it on the [Mod Loader Options](mod_loader_options.md) page.

4. Click Close, and save your project.
	- Scene > Save All Scenes

!!! tip
    The Mod Loader can be customized further by changing the [Options](mod_loader_options.md)

![](_media/autoload_settings.png)
/// caption
*Adding `ModLoaderStore` and `ModLoader` to the Autoload/Global settings of the game [Brotato](https://store.steampowered.com/app/1942280/Brotato/)*
///

## Related Examples
- [GodotModding-UserProfileUI](https://github.com/GodotModding/GodotModding-UserProfileUI) - A mod that adds an interface to manage mod user profiles, to handle enabling and disabling of mods.
- [GodotModding-ModConfigEditor](https://github.com/GodotModding/GodotModding-ModConfigEditor) - A mod that adds an interface to edit mod configs, the user settings that mod developers can add for users to customise their experience.

## Related Pages
- [Decompiling Games](../modding/tools/decompile_games.md) - Instructions for decompiling a game, for editing in Godot.
- [GodotSteam](../modding/tools/godot_steam.md) - Most games require you to use GodotSteam, instead of vanilla Godot.
