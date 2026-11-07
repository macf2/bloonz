## Mac:

Tasks:
    &emsp;- Refactor to make each monkey use different classes, with a base monkey class
    &emsp;- premade maps with a main menu for map selection

Refactor Results:
        I made the entities in the game (Monkeys, bloons, projectiles) more OOP style. Before, the code was more procedural, were we had 3 structs (Monkey, Projectile, Bloon) each with a enum variant (MonkeyType, BloonType, ProjectileType). We had the World class have a update_monkeys, update_projectiles, and update_bloons methods, that ran through the arrays and updated them acordingly. Now, we have 3 base classes (IMonkey, IBloon, IProjectile) that have a general interface for each entitiy. Rather than having enums for the type of entity, we now just inherit from the base interface and override the init, update, etc methods that dictate the behavior of the entity. For example, rather than calling  world.update_bloons() you do world.bloons.update() and each bloon update itself.
        You can't really see the results of this in game, but it made it easier to the team to add new towers and bloons.

Map selection menu results:
    
