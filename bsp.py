import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Room:
    WALL_THICKNESS = 0.1
    BROWN_SHADES = ['#808080']
    DOOR_CLEARANCE = 20
    MAX_PLACEMENT_ATTEMPTS = 100

    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.doors, self.objects = [], []

    def add_door(self):
        door_positions = [
            (random.uniform(self.x + self.WALL_THICKNESS, self.x + self.width - self.WALL_THICKNESS - 5),
             random.choice([self.y, self.y + self.height - self.WALL_THICKNESS]), 'H'),
            (random.choice([self.x, self.x + self.width - self.WALL_THICKNESS]),
             random.uniform(self.y + self.WALL_THICKNESS, self.y + self.height - self.WALL_THICKNESS - 5), 'V')
        ]
        self.doors.extend(door_positions)

    def add_objects(self):
        for _ in range(random.randint(1, 5)):
            attempts = 0
            while attempts < self.MAX_PLACEMENT_ATTEMPTS:
                obj_width, obj_height = random.uniform(1.0, self.width / 5), random.uniform(1.0, self.height / 5)
                if max(obj_width / obj_height, obj_height / obj_width) < 3:
                    obj_x, obj_y = random.uniform(self.x + obj_width / 2, self.x + self.width - obj_width / 2), random.uniform(self.y + obj_height / 2, self.y + self.height - obj_height / 2)

                    if not self.is_near_door(obj_x, obj_y, obj_width, obj_height):
                        #self.objects.append((obj_x - obj_width / 2, obj_y - obj_height / 2, obj_width, obj_height, random.choice(self.BROWN_SHADES)))
                        break
                attempts += 1

    def is_near_door(self, obj_x, obj_y, obj_width, obj_height):
        for door_x, door_y, orientation in self.doors:
            if orientation == 'H':
                if (door_y >= obj_y and door_y - obj_y < self.DOOR_CLEARANCE) or \
                   (door_y < obj_y and obj_y - door_y < self.DOOR_CLEARANCE):
                    if (obj_x + obj_width > door_x - self.DOOR_CLEARANCE) and (obj_x < door_x + self.DOOR_CLEARANCE):
                        return True
            else:
                if (door_x >= obj_x and door_x - obj_x < self.DOOR_CLEARANCE) or \
                   (door_x < obj_x and obj_x - door_x < self.DOOR_CLEARANCE):
                    if (obj_y + obj_height > door_y - self.DOOR_CLEARANCE) and (obj_y < door_y + self.DOOR_CLEARANCE):
                        return True
        return False

    def draw(self, ax):
        for obj in self.objects:
            ax.add_patch(Rectangle((obj[0], obj[1]), obj[2], obj[3], color=obj[4]))
        ax.add_patch(Rectangle((self.x, self.y), self.width, self.height, fill=None, edgecolor='black'))


def draw_doors(rooms, ax):
    door_width, door_thickness = 5, 5
    for room in rooms:
        for door_x, door_y, orientation in room.doors:
            if orientation == 'H':
                ax.add_patch(Rectangle((door_x - door_width / 2, door_y - door_thickness / 2), door_width, door_thickness, color='w'))
            else:
                ax.add_patch(Rectangle((door_x - door_thickness / 2, door_y - door_width / 2), door_thickness, door_width, color='w'))


def split_room(room, min_size, min_aspect_ratio=1.0 / 3):
    vertical_split = room.width >= room.height
    if vertical_split:
        if room.width - min_size <= min_size or room.width / room.height < min_aspect_ratio:
            return None
        split_pos = random.randint(min_size, room.width - min_size)
        room1, room2 = Room(room.x, room.y, split_pos, room.height), Room(room.x + split_pos, room.y, room.width - split_pos, room.height)
    else:
        if room.height - min_size <= min_size or room.height / room.width < min_aspect_ratio:
            return None
        split_pos = random.randint(min_size, room.height - min_size)
        room1, room2 = Room(room.x, room.y, room.width, split_pos), Room(room.x, room.y + split_pos, room.width, room.height - split_pos)

    return room1, room2


def generate_environment(width, height, min_size, max_splits, min_aspect_ratio=1.0 / 3):
    rooms = [Room(0, 0, width, height)]
    for _ in range(max_splits):
        new_rooms = []
        for room in rooms:
            if room.width > min_size * 2 and room.height > min_size * 2:
                split_result = split_room(room, min_size, min_aspect_ratio)
                if split_result:
                    new_rooms.extend(split_result)
                else:
                    new_rooms.append(room)
            else:
                new_rooms.append(room)
        rooms = new_rooms

    for room in rooms:
        room.add_door()
        room.add_objects()

    return rooms


def main():
    overall_width, overall_height, minimum_room_size, max_room_splits, min_aspect_ratio = 1111, 1111, 10, 100, 1.0 / 3
    environment_rooms = generate_environment(overall_width, overall_height, minimum_room_size, max_room_splits, min_aspect_ratio)
    fig, ax = plt.subplots()
    for room in environment_rooms:
        room.draw(ax)
    draw_doors(environment_rooms, ax)
    ax.set_xlim(0, overall_width)
    ax.set_ylim(0, overall_height)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == "__main__":
    main()
