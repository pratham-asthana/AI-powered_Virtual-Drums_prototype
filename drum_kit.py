import math
import cv2

class DrumKit:
    def __init__(self, frame_width, frame_height):
        self.drum_pads = {
            "snare": {"center": (int(frame_width * 0.25), int(frame_height * 0.5)), "radius": 50, "active_hands": set()},
            "kick": {"center": (int(frame_width * 0.5), int(frame_height * 0.7)), "radius": 50, "active_hands": set()},
            "hi-hat": {"center": (int(frame_width * 0.75), int(frame_height * 0.5)), "radius": 50, "active_hands": set()},
        }

    def is_hit(self, hand_id, hand_landmark, frame_width, frame_height):
        hits = []
        x, y = hand_landmark.x * frame_width, hand_landmark.y * frame_height
        for drum_name, drum_pad in self.drum_pads.items():
            pad_center, pad_radius = drum_pad["center"], drum_pad["radius"]
            distance = math.sqrt((x - pad_center[0]) ** 2 + (y - pad_center[1]) ** 2)
            if distance <= pad_radius:
                if hand_id not in drum_pad["active_hands"]:
                    hits.append(drum_name)
                    drum_pad["active_hands"].add(hand_id)  # Mark this hand as active on the pad
            else:
                if hand_id in drum_pad["active_hands"]:
                    drum_pad["active_hands"].remove(hand_id)  # Remove this hand if it leaves the pad
        return hits

    def draw_pads(self, frame):
        for drum_name, drum_pad in self.drum_pads.items():
            center, radius = drum_pad["center"], drum_pad["radius"]
            color = (0, 255, 0) if not drum_pad["active_hands"] else (0, 0, 255)  # Green if inactive, red if active
            cv2.circle(frame, center, radius, color, 2)
            cv2.putText(frame, drum_name.upper(), (center[0] - 30, center[1] - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)