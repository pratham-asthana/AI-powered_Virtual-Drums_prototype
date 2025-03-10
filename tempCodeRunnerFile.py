import cv2
from hand_tracker import HandTracker
from drum_kit import DrumKit
from sound_player import SoundPlayer

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize components
    hand_tracker = HandTracker()
    drum_kit = DrumKit(frame_width, frame_height)
    sound_player = SoundPlayer()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Track hands
        results = hand_tracker.track_hands(frame)

        # Draw drum pads
        drum_kit.draw_pads(frame)

        # Detect drum hits and play sounds
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                hand_tracker.draw_landmarks(frame, hand_landmarks)

                # Check for drum hits
                hits = drum_kit.is_hit(hand_landmarks.landmark[hand_tracker.mp_hands.HandLandmark.INDEX_FINGER_TIP], frame_width, frame_height)
                for drum_name in hits:
                    sound_player.play_sound(drum_name)

        # Display the frame
        cv2.imshow('Virtual Drum Kit', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()