from insightface.app import FaceAnalysis

class FaceEmbedder:
    def __init__(self):
        self.app = FaceAnalysis(providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=0)

    def get_embedding(self, frame):
        faces = self.app.get(frame)
        return faces[0].embedding if faces else None
