# GestureChord Feature Requirements

## MVP Goal

GestureChord should let a user select and play chords from a chord wheel using hand gestures tracked through a webcam.

The first version should be simple, reliable, and demo-ready.

---

## Must-Have Features

### 1. Webcam Feed

The app must open the default webcam and display the live camera feed in a window.

Requirements:

- Start webcam when the app launches.
- Show live video frames.
- Exit cleanly when the user presses a quit key.
- Handle webcam failure with a clear error message.

---

### 2. Hand Tracking

The app must detect one hand using MediaPipe.

Requirements:

- Detect hand landmarks in real time.
- Track the index fingertip.
- Track the thumb fingertip.
- Continue running when no hand is detected.
- Draw a small visual marker on the index fingertip.

---

### 3. Chord Wheel

The app must display a 7-segment chord wheel.

Requirements:

- Each segment represents one chord.
- The wheel should display the diatonic chords for the selected key.
- The currently selected segment should be highlighted.
- Chord labels should be visible.
- The wheel should update in real time.

---

### 4. Key Selection

The app must support selecting a musical key.

MVP supported keys:

- C Major
- D Major
- G Major
- A Major
- F Major

Requirements:

- The current key should be visible on screen.
- The app should display the correct 7 diatonic chords for the selected key.
- Minor keys are not required for the MVP.

---

### 5. Finger-To-Segment Detection

The app must determine which chord the user is pointing at.

Requirements:

- Use the index fingertip position.
- Compare the fingertip position to the center of the chord wheel.
- Convert the fingertip position into an angle.
- Map the angle to one of the 7 chord wheel segments.
- Ignore the fingertip if it is too close to the center.
- Ignore the fingertip if it is outside the wheel.

---

### 6. Chord Playback

The app must play the selected chord.

Requirements:

- Use `pygame-ce` for audio playback.
- Import it in Python as `pygame`.
- Play the chord when the user confirms the selection.
- Playback should not freeze the webcam feed.
- Generated tones are acceptable for the MVP.

---

### 7. Confirmation Input

The app must provide a way to confirm and play a chord.

MVP requirement:

- Pressing Spacebar plays the selected chord.

Nice-to-have requirement:

- Pinch gesture between thumb and index finger plays the selected chord.

Pinch requirements:

- Calculate distance between index fingertip and thumb fingertip.
- Trigger playback when the distance is below a threshold.
- Use debounce logic so one pinch does not trigger repeatedly.

---

### 8. Basic UI Display

The app must show enough information for the user to understand what is happening.

Requirements:

- Show current key.
- Show selected chord.
- Show chord wheel.
- Show fingertip marker.
- Show simple quit/play instructions.
- Optional: show FPS counter.

---

## Nice-To-Have Features

Only add these after the MVP works:

- Pinch confirmation gesture
- Chord progression recording
- MIDI export
- FPS counter
- Latency tracking
- Gesture smoothing
- Minor key support
- Better chord sounds
- Demo GIF or video

---

## Out Of Scope For MVP

Do not build these in the first version:

- AI chord prediction
- User accounts
- Databases
- Cloud deployment
- Mobile version
- Large-scale machine learning
- Complex GUI framework
- Full music production tools

---

## Completion Criteria

The MVP is complete when:

- The webcam opens successfully.
- A hand can be tracked.
- The chord wheel is visible.
- Pointing at different wheel segments changes the selected chord.
- Pressing Spacebar plays the selected chord.
- The app does not crash when no hand is visible.
- The project has a clear README.
- The code is organized into separate modules.