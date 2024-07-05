import pygame 

from object import Object


class Segment(Object):
    def __init__(self, x, y, w, h, texture_path):
        super().__init__(x, y, w, h, texture_path)
        self.w = w
        self.h = h
    
    def update(self, target_pos, segment_dis, speed):
        direction = [target_pos[0] - self.object_hitbox.x, target_pos[1] - self.object_hitbox.y]
        vector_len = (direction[0]**2 + direction[1]**2)**(1/2)
        if vector_len < segment_dis:
            return
        direction[0] /= vector_len
        direction[1] /= vector_len

        self.object_hitbox.x += direction[0] * speed
        self.object_hitbox.y += direction[1] * speed