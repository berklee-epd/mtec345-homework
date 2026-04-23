// Landmark indices derived from FaceLandmarker's own named connection sets:
// LEFT_EYE, RIGHT_EYE, LEFT_EYEBROW, RIGHT_EYEBROW, LEFT_IRIS, RIGHT_IRIS, LIPS, FACE_OVAL.
// 136 unique points — verified by extracting directly from @mediapipe/tasks-vision.
// These are the only indices sent as OSC messages (full 478 would exceed UDP size limit).
export const FACE_KEY_INDICES: readonly number[] = [
  // right eye (16)
  7, 33, 133, 144, 145, 153, 154, 155, 157, 158, 159, 160, 161, 163, 173, 246,
  // left eye (16)
  249, 263, 362, 373, 374, 380, 381, 382, 384, 385, 386, 387, 388, 390, 398, 466,
  // right eyebrow (10)
  46, 52, 53, 55, 63, 65, 66, 70, 105, 107,
  // left eyebrow (10)
  276, 282, 283, 285, 293, 295, 296, 300, 334, 336,
  // right iris (4)
  469, 470, 471, 472,
  // left iris (4)
  474, 475, 476, 477,
  // lips (40)
  0, 13, 14, 17, 37, 39, 40, 61, 78, 80, 81, 82, 84, 87, 88, 91, 95,
  146, 178, 181, 185, 191, 267, 269, 270, 291, 308, 310, 311, 312, 314,
  317, 318, 321, 324, 375, 402, 405, 409, 415,
  // face oval (36)
  10, 21, 54, 58, 67, 93, 103, 109, 127, 132, 136, 148, 149, 150, 152,
  162, 172, 176, 234, 251, 284, 288, 297, 323, 332, 338, 356, 361, 365,
  377, 378, 379, 389, 397, 400, 454,
];

// A Set for O(1) lookup in the drawing code
export const FACE_KEY_INDEX_SET = new Set(FACE_KEY_INDICES);
