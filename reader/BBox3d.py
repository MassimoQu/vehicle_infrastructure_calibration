from BBox import BBox

class BBox3d(BBox):
    def __init__(self, bbox_type, bbox_8_3, occluded_state = 0, truncated_state = 0):
        super().__init__(bbox_type, occluded_state, truncated_state)
        self.bbox3d_8_3 = bbox_8_3

    def get_bbox3d_8_3(self):
        return self.bbox3d_8_3
    