import re
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict


class RAGRetriever:
    def __init__(
        self,
        index_file: str = "data/faiss/faiss_index.bin",
        chunks_file: str = "data/faiss/chunks.pkl",
        embedding_model_name: str = "multi-qa-MiniLM-L6-cos-v1"  # FIX 1: wrong model before
    ):
        self.index = faiss.read_index(index_file)

        with open(chunks_file, "rb") as f:
            self.chunked_sections = pickle.load(f)

        self.model = SentenceTransformer(embedding_model_name)

    # ----------------------------------------
    # Core query — use for direct keyword queries
    # e.g. "punishment for murder", "theft definition"
    # ----------------------------------------
    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        query_vec = self.model.encode([query_text]).astype("float32")
        faiss.normalize_L2(query_vec)           # FIX 2: was missing normalization
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(distances[0], indices[0]):
            chunk = self.chunked_sections[idx].copy()
            chunk["score"] = round(float(score), 4)  # FIX 3: score was missing
            results.append(chunk)
        return results

    # ----------------------------------------
    # Query expansion — use for hypothetical/story queries
    # e.g. "Ram stabbed Shyam and he died"
    # ----------------------------------------
    def query_with_expansion(self, story: str, top_k: int = 5) -> List[Dict]:
        sub_queries = self._extract_legal_keywords(story)

        # Query each sub-query, keep best score per section
        all_results = {}
        for sq in sub_queries:
            results = self.query(sq, top_k=top_k)
            for r in results:
                sec = r["section_number"]
                if sec not in all_results or r["score"] > all_results[sec]["score"]:
                    all_results[sec] = r

        return sorted(
            all_results.values(),
            key=lambda x: x["score"],
            reverse=True
        )[:top_k]

    # ----------------------------------------
    # Smart query — auto detects if story or keyword
    # Use this as your single entry point in FastAPI
    # ----------------------------------------
    def smart_query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        # If query is long (>12 words) treat as story → use expansion
        # If short → direct keyword query
        word_count = len(query_text.split())
        if word_count > 12:
            return self.query_with_expansion(query_text, top_k=top_k)
        else:
            return self.query(query_text, top_k=top_k)

    # ----------------------------------------
    # Internal: extract legal sub-queries from story
    # ----------------------------------------
    def _extract_legal_keywords(self, story: str) -> List[str]:
        sub_queries = []
        story_lower = story.lower()

        rules = [
            (r'\bdied\b|\bdead\b|\bdeath\b|\bkilled\b|\bmurder\b|\bstab\b|\bshot\b',
             "murder intentional killing death punishment"),

            (r'knows.*likely.*death|likely to cause death|not intend.*kill|survived.*blow',
             "culpable homicide not amounting to murder"),

            (r'injur|wound|hurt|rod|weapon|permanent.*loss|fracture|grievous',
             "grievous hurt bodily injury weapon punishment"),

            (r'\bstole\b|\btheft\b|\bsteal\b|\btook.*property\b|\bgold\b|\bjewel\b|\belectronics\b',
             "theft stolen property dishonestly taking"),

            (r'broke.*window|broke.*door|break.*in|enter.*house|trespass|warehouse.*night|locked.*building',
             "house breaking trespass theft dwelling night"),

            (r'\brob\b|\bsnatch\b|force.*take.*property|extort',
             "robbery extortion snatching force"),

            (r'fake|pretend|impersonat|deceiv|false.*officer|cheat|fake.*document|false.*identity|uniform|disguise|false.*name',
            "cheating fraud impersonation deceiving dishonestly"),

            (r'collected.*money|took.*money|money.*disappeared|paid.*money|gave.*money|cash.*collected|promised.*service|never.*delivered|vanished.*money',
            "cheating inducing delivery property dishonestly punishment Section 318"),

            (r'government.*officer|revenue.*officer|civil.*servant|police.*impersonat|official.*uniform|pretended.*official|false.*government',
            "impersonation public servant cheating fraud deceiving"),

            (r'kidnap|abduct|took.*child|taken.*away.*child|forcefully took',
             "kidnapping abduction child lawful guardianship"),

            (r'ransom|demanded.*money|threaten.*harm.*person',
             "kidnapping ransom extortion threat"),

            (r'\bchild\b|\bminor\b|\byear.*old\b|\bschool\b',
             "kidnapping child minor abduction"),

            (r'\brape\b|raped|sexual assault|sexually assault',
            "rape definition punishment Section 63 64 65"),

            (r'forced.*will|against.*will|without.*consent|grabbed.*woman|dragged.*woman|isolated.*woman|attacked.*woman',
            "rape woman forced against will without consent punishment"),

            (r'knife.*woman|weapon.*woman|threatened.*woman|threat.*rape|knife.*rape|armed.*rape',
            "rape aggravated circumstances weapon threat punishment Section 64 65"),

            (r'medical.*examination|cctv|evidence.*assault|confirmed.*assault|identified.*accused',
            "rape evidence punishment rigorous imprisonment"),

            (r'outrage|modesty|groped|touched.*without.*consent',
             "outrage modesty woman assault criminal force"),

            (r'self.defence|fought back|defend.*himself|protect.*himself|attacked.*him|surrounded.*him|attacked.*with|men.*attacked|to escape|stabbed.*escape|grabbed.*knife|snatched.*weapon',
            "right of private defence body property"),

            (r'attacked.*knife|knife.*attack|rob.*attack|surrounded.*rob|assailant|attacker|aggressor|mob.*knife|men.*knife|four.*men|group.*attacked', "right of private defence causing hurt death attacker"),

            (r'rob.*him|tried.*rob|attempt.*rob|robbers|dacoits|snatched.*from.*him|demanded.*purse|demanded.*wallet',"robbery victim private defence right resist"),

            (r'attempt|tried to|try to|survived|did not die|not succeed',
             "attempt to commit offence punishment"),

            (r'group.*men|mob|gang|five.*more.*person|assembly',
             "unlawful assembly rioting group offence"),
    
             (r'broke.*stole|entered.*took|trespass.*stole|house.*robbery|night.*stole|midnight.*took',
              "robbery theft house breaking dwelling night punishment"),
        ]

        for pattern, legal_query in rules:
            if re.search(pattern, story_lower):
                sub_queries.append(legal_query)

        # Add trimmed story as fallback
        short_story = " ".join(story.split()[:60])
        sub_queries.append(short_story)

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for q in sub_queries:
            if q not in seen:
                seen.add(q)
                unique.append(q)

        return unique