"""
Lab 5: Symbolic Music Generation
Algorithm: Maze Generation + DFS Pathfinding + Bubble Sort + Sleep Sort
"""

import random
from symusic import Note, Score, Tempo, Track

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
SEED        = 2025
BPM         = 100
COLS        = 10
ROWS        = 8
SCALE       = [0, 2, 4, 7, 9]           # pentatonic intervals
ROOT_MIDI   = 60                         # Middle C
OCTAVE_SPAN = 2                          # how many octaves the grid maps to

random.seed(SEED)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def scale_pitch(value, lo, hi):
    """Map a value in [lo, hi] to a MIDI pitch in C major, 2 octaves."""
    if hi == lo:
        return ROOT_MIDI
    t = (value - lo) / (hi - lo)
    total_notes = len(SCALE) * OCTAVE_SPAN
    idx = int(t * (total_notes - 1))
    octave = idx // len(SCALE)
    degree = idx % len(SCALE)
    return ROOT_MIDI + octave * 12 + SCALE[degree]


def coord_pitch(r, c):
    """Convert maze (row, col) to a MIDI pitch."""
    combined = r * COLS + c
    return scale_pitch(combined, 0, ROWS * COLS - 1)


def make_note(beat, duration, pitch, velocity):
    return Note(beat, duration, pitch, velocity, "quarter")


# ─────────────────────────────────────────
# CHAPTER 1: MAZE GENERATION (Prim's)
# ─────────────────────────────────────────

def generate_maze():
    """
    Prim's algorithm: start from (0,0), grow maze by randomly
    picking a frontier cell and connecting it to a visited neighbour.
    Returns list of (row, col) tuples in the order walls were broken.
    """
    visited  = [[False] * COLS for _ in range(ROWS)]
    frontier = []   # list of (r, c) not yet visited but adjacent to visited
    order    = []   # the sequence of cells we "open"

    def add_frontier(r, c):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc]:
                if (nr, nc) not in frontier:
                    frontier.append((nr, nc))

    visited[0][0] = True
    add_frontier(0, 0)
    order.append((0, 0))

    while frontier:
        idx = random.randrange(len(frontier))
        r, c = frontier.pop(idx)
        # find a visited neighbour to connect to
        neighbours = [
            (r+dr, c+dc)
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
            if 0 <= r+dr < ROWS and 0 <= c+dc < COLS and visited[r+dr][c+dc]
        ]
        if neighbours:
            visited[r][c] = True
            order.append((r, c))
            add_frontier(r, c)

    return order


def chapter1_notes(maze_order, start_beat=0.0):
    """
    Each cell added to the maze = one note.
    Pitch  ← column position (x axis of maze)
    Duration ← random short value (exploration feel)
    Velocity ← row position mapped to 40–90 (deeper = louder)
    """
    notes = []
    beat  = start_beat + 1.0
    for r, c in maze_order:
        pitch    = coord_pitch(r, c)
        duration = random.choice([0.25, 0.5, 0.5, 0.75])
        velocity = int(40 + (r / (ROWS - 1)) * 50)
        notes.append(make_note(beat, duration, pitch, velocity))
        beat += duration
    return notes, beat


# ─────────────────────────────────────────
# CHAPTER 2: DFS PATHFINDING
# ─────────────────────────────────────────

def build_adjacency(maze_order):
    """
    Reconstruct which cells are connected based on Prim's visit order.
    We treat any two orthogonally adjacent visited cells as connected.
    """
    visited_set = set(maze_order)
    adj = {}
    for r, c in maze_order:
        adj[(r,c)] = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if (nr, nc) in visited_set:
                adj[(r,c)].append((nr, nc))
    return adj


def dfs_path(adj):
    """
    DFS from (0,0) to (ROWS-1, COLS-1).
    Returns the full sequence of (r,c) visited including backtracking steps.
    """
    goal    = (ROWS-1, COLS-1)
    visited = set()
    path    = []   # full walk including backtracks

    def dfs(node):
        if node == goal:
            path.append(node)
            return True
        visited.add(node)
        path.append(node)
        neighbours = adj.get(node, [])
        random.shuffle(neighbours)
        for nb in neighbours:
            if nb not in visited:
                if dfs(nb):
                    return True
        # backtrack: re-append current node to signal retreat
        path.append(node)
        return False

    dfs((0, 0))
    return path


def chapter2_notes(dfs_walk, ch1_end_beat):
    """
    Each step in the DFS walk = one note.
    Forward step  → normal velocity
    Backtrack step → softer velocity, slightly lower pitch
    """
    notes   = []
    beat    = ch1_end_beat + 1.0   # 1-beat rest between chapters
    seen    = {}                    # node → first beat it appeared

    for i, (r, c) in enumerate(dfs_walk):
        node = (r, c)
        pitch    = coord_pitch(r, c)
        duration = 0.5

        if node in seen:
            # backtracking: quieter, slightly flatten pitch
            velocity = 35
            pitch    = max(ROOT_MIDI, pitch - 2)
        else:
            seen[node] = beat
            velocity = int(55 + (c / (COLS - 1)) * 35)  # further right = louder

        notes.append(make_note(beat, duration, pitch, velocity))
        beat += duration

    return notes, beat


# ─────────────────────────────────────────
# CHAPTER 3A: BUBBLE SORT
# ─────────────────────────────────────────

def bubble_sort_events(arr):
    """
    Run bubble sort and record each comparison/swap as an event.
    Returns list of (type, index_a, index_b, array_snapshot)
    type = 'compare' or 'swap'
    """
    a      = arr[:]
    events = []
    n      = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            events.append(('compare', j, j+1, a[:]))
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                events.append(('swap', j, j+1, a[:]))
    return events


def chapter3a_notes(dfs_walk, ch2_end_beat):
    """
    Take the last 16 DFS path columns as the array to sort.
    Each bubble sort event = one note.
    Compare → soft note at average pitch of the two elements
    Swap    → louder note, higher pitch
    """
    raw_vals = [c for r, c in dfs_walk[-16:]]
    if len(raw_vals) < 2:
        raw_vals = list(range(8))

    events = bubble_sort_events(raw_vals)
    notes  = []
    beat   = ch2_end_beat + 1.0
    lo, hi = min(raw_vals), max(raw_vals)

    for evt_type, ia, ib, snapshot in events:
        va, vb = snapshot[ia], snapshot[ib]
        pitch    = scale_pitch(int((va + vb) / 2), lo, hi)
        duration = 0.25

        if evt_type == 'swap':
            pitch    = scale_pitch(max(va, vb), lo, hi)
            velocity = 90
        else:
            velocity = 45

        notes.append(make_note(beat, duration, pitch, velocity))
        beat += duration

    return notes, beat


# ─────────────────────────────────────────
# CHAPTER 3B: SLEEP SORT (coda)
# ─────────────────────────────────────────

def sleep_sort_schedule(arr):
    """
    Sleep Sort: each element 'sleeps' for its value in time units,
    then fires. Returns list of (fire_time, value) sorted by fire_time.
    """
    scale_factor = 0.15   # seconds per unit value
    return sorted([(v * scale_factor, v) for v in arr], key=lambda x: x[0])


def chapter3b_notes(dfs_walk, ch3a_end_beat):
    """
    Use the same array as bubble sort but schedule with Sleep Sort.
    Each element wakes up at its own time → note fires then.
    Creates a sparse, ascending coda.
    """
    raw_vals = [c for r, c in dfs_walk[-16:]]
    if len(raw_vals) < 2:
        raw_vals = list(range(8))

    schedule = sleep_sort_schedule(raw_vals)
    notes    = []
    lo, hi   = min(raw_vals), max(raw_vals)
    base     = ch3a_end_beat + 2.0   # 2-beat gap between 3A and 3B

    for fire_time, val in schedule:
        pitch    = scale_pitch(val, lo, hi)
        duration = 0.75
        velocity = int(50 + (val / (hi if hi else 1)) * 50)
        beat     = base + fire_time
        notes.append(make_note(beat, duration, pitch, velocity))

    # 收束和弦：最后一个音结束后加C大三和弦
    last_beat = max(n.time for n in notes) + 2.0
    for chord_pitch in [ROOT_MIDI, ROOT_MIDI + 4, ROOT_MIDI + 7]:
        notes.append(make_note(last_beat, 3.0, chord_pitch, 70))

    return notes


# ─────────────────────────────────────────
# ASSEMBLE SCORE
# ─────────────────────────────────────────

def build_score():
    score = Score(960, ttype="quarter")
    score.tempos.append(Tempo(0, BPM, ttype="quarter"))
    track = Track(ttype="quarter")

    maze_order = generate_maze()
    adj        = build_adjacency(maze_order)
    dfs_walk   = dfs_path(adj)

    ch2, ch2_end = chapter2_notes(dfs_walk, 0)
    print(f"Chapter 2: {len(ch2)} notes  (ends at beat {ch2_end:.2f})")

    ch1, ch1_end = chapter1_notes(maze_order, ch2_end)
    print(f"Chapter 1: {len(ch1)} notes  (ends at beat {ch1_end:.2f})")

    ch3a, ch3a_end = chapter3a_notes(dfs_walk, ch1_end)
    print(f"Chapter 3A (bubble): {len(ch3a)} notes  (ends at beat {ch3a_end:.2f})")

    ch3b = chapter3b_notes(dfs_walk, ch3a_end)
    print(f"Chapter 3B (sleep):  {len(ch3b)} notes")

    all_notes = ch2 + ch1 + ch3a + ch3b
    for n in all_notes:
        track.notes.append(n)

    score.tracks.append(track)
    return score


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    score = build_score()
    score.dump_midi("composition.mid")
    print("\nSaved: composition.mid")
    print("Import into Logic Pro, assign a piano/synth sound, and export as WAV.")