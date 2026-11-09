# GitHub Links:
- MAIN: https://github.com/macf2/bloonz/tree/main
- REFACTOR: https://github.com/macf2/bloonz/tree/refactor

# Isaac Young:
- I have started to implement the map editor. This can be found on the refactor branch of our project. Pull the refactor branch run map_editor.py and an image of a map will appear you can place the spline down by clicking on the map. Select and move exisiting nodes by clicking on them and dragging, and delete nodes by selecting them and clicking backspace on your keyboard. Once you've placed you path down you can hit the save button in the top left of the window. If you go into blooz/assets/maps/map_1 and select the track.json file you can see the file update with the coordinates of the spline when you hit save. More user firendly UI will be implemented later also ability to pick a custom image. I didn't do round mechanics because we are still building out core functionality so it didn't really end up making sense for this leg of the project.

# Nico Lippiatt-Cook

- I implemented 4 new towers and 5 new bloons as well as the different projectile behaviors of the towers. This is all merged into main, if you pull the main branch and run main.py and start a new save you can experiment with the new towers. First create the track by pressing T to spawn nodes. Then you can place the towers. Freeze tower shoots an orb that freezes bloons, bombtower shoots a bomb that does splash damage, tack shooter shoots tacks from 8 directions, and supermonkey is like the dart monkey but it has very little reload time and a lot of range. The new bloons spawn randomly, red is the basic, blue is a little faster and when you pop it a red one spawns, green is even faster and when popped a blue one spawns, yellow is very fast and spawns a green on pop, the black bloon is immune to bomb explosions and spawns two yellows on pop, white bloon is immune to freeze and spawns two yellow bloons on pop. 


# Mac 

- I refactored the way that entities (monkeys, projectiles, and bloons) are handled. Before we had enum types for the different type of entities (MonkeyType, BloonType, ProjectileType). now we have base itnerface classes (IBloon, IMonkey, IProjectile) that each type inherits from. ALso, rather than the world having functions to update the entities, they now have their own update methods. For example,instead of doing world.update_monkeys() you do world.monkeys.update().
- I made a dropdown menu in the title screen to select maps.
