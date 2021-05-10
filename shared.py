import pygame

def set_origin(obj, image, pos, origin_pos, angle, rotate = False):
    #if self.angle_ == False: return self.origin
    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot        = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = ((pos[0] - origin_pos[0] + min_box[0] - pivot_move[0]), (pos[1] - origin_pos[1] - max_box[1] + pivot_move[1]))

    obj.origin = origin
    # obj.rect.center = obj.origin

    return

def rotate(obj, surf, image, angle):
    obj.sprit_copy = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    # surf.blit(self.sprit_copy, self.origin)

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*obj.origin, *obj.sprit_copy.get_size()), 2)

    return


def is_collision(rect1, rect2):

    return rect1.colliderect(rect2)
