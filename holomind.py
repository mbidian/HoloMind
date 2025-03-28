import random

class Dodecahedron:
    def __init__(self, name, faces, internal_vectors):
        self.name = name
        self.faces = faces  # Dictionary of prime numbers to concepts
        self.internal_vectors = internal_vectors  # List of tuples (v1, v2)
        self.experience = []  # List of (product, concepts, message)

    def think_internally(self):
        v1, v2 = random.choice(self.internal_vectors)
        return v1 * v2, [self.faces[v1], self.faces[v2]]

class HolographicMind:
    def __init__(self):
        self.core_concepts = ["worry", "husband", "search", "resolve", "road", "satchel", "absence", "walk",
                              "children", "home", "cigarettes", "fire", "time", "sign", "light", "peace"]
        self.dodecahedrons = []
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        for i in range(5000):  # 5000 initial volumes
            faces = {}
            for j in range(4):
                prime = prime_numbers[(i * 4 + j) % len(prime_numbers)] * (i + 1)
                concept = self.core_concepts[(i * 4 + j) % len(self.core_concepts)]
                faces[prime] = concept
            vectors = [(list(faces.keys())[0], list(faces.keys())[1]), 
                       (list(faces.keys())[2], list(faces.keys())[3])]
            self.dodecahedrons.append(Dodecahedron(f"Volume_{i}", faces, vectors))
        
        self.external_vectors = [(list(self.dodecahedrons[i].faces.keys())[0], 
                                 list(self.dodecahedrons[i+1].faces.keys())[0] if i+1 < 5000 else list(self.dodecahedrons[0].faces.keys())[0]) 
                                 for i in range(0, 5000, 50)]  # External vectors every 50 volumes
        self.max_autogen = 50  # Max 50 auto-generated volumes
        self.autogen_count = 0

    def think(self):
        """Generate a thought from a random dodecahedron."""
        dodec = random.choice(self.dodecahedrons)
        product, concepts = dodec.think_internally()
        if random.random() < 0.15:  # 15% chance of external combination
            valid_v1 = [v for v, _ in self.external_vectors if v in dodec.faces]
            if valid_v1:  # Check if there are valid external vectors
                v1 = random.choice(valid_v1)
                valid_v2 = [v2 for v1x, v2 in self.external_vectors if v1x == v1]
                if valid_v2:
                    v2 = random.choice(valid_v2)
                    for d in self.dodecahedrons:
                        if v2 in d.faces:
                            return (v1 * v2, [dodec.faces[v1], d.faces[v2]]), dodec
        return (product, concepts), dodec

    def speak(self, concepts):
        """Generate a natural response from concepts."""
        if "husband" in concepts and "worry" in concepts:
            return "I worry about my husband."
        elif "road" in concepts and "walk" in concepts:
            return "I walk along the road with resolve."
        elif "search" in concepts and "husband" in concepts:
            return "I search for my husband."
        elif "satchel" in concepts and "road" in concepts:
            return "I carry my satchel on the road."
        elif "cigarettes" in concepts:
            if "fire" in concepts:
                return "I light cigarettes with fire on the road."
            elif "road" in concepts:
                return "I smoke cigarettes on my road."
            else:
                return f"My mind ties {concepts[0]} to cigarettes."
        else:
            return f"My thoughts connect {concepts[0]} with {concepts[1]}."

    def parent_evaluate(self, product, concepts, dodec):
        """Evaluate thought resonance and store valid experiences."""
        resonance_score = sum(1 for c in concepts if c in self.core_concepts) / len(concepts)
        valid = resonance_score >= 0.7
        message = self.speak(concepts)
        if valid:
            dodec.experience.append((product, concepts, message))
            print(f"Valid ({dodec.name}): {message} (Product: {product})")
            if random.random() < 0.05 and self.autogen_count < self.max_autogen and len(dodec.experience) > 1:
                self.autogenerate(dodec)
        else:
            print(f"Invalid ({dodec.name}): {message} (Product: {product})")

    def autogenerate(self, dodec):
        """Generate a new volume from a successful experience."""
        last_exp = dodec.experience[-1]
        new_faces = {last_exp[0]: last_exp[1][0], last_exp[0] + 1: last_exp[1][1]}
        new_vectors = [(last_exp[0], last_exp[0] + 1)]
        new_dodec = Dodecahedron(f"Volume_{len(self.dodecahedrons)}", new_faces, new_vectors)
        self.dodecahedrons.append(new_dodec)
        self.external_vectors.append((list(dodec.faces.keys())[0], last_exp[0]))
        self.autogen_count += 1
        print(f"New volume generated: {new_dodec.name} with {new_faces}")

    def dialog(self, question):
        """Respond to user questions based on experience."""
        if "feel" in question.lower():
            exp = [m for d in self.dodecahedrons[:500] for _, _, m in d.experience if "worry" in m or "absence" in m]
            return random.choice(exp) if exp else "I'm not sure what I feel right now."
        elif "do" in question.lower():
            exp = [m for d in self.dodecahedrons[500:1000] for _, _, m in d.experience if "search" in m or "walk" in m]
            return random.choice(exp) if exp else "I'm not certain what I'm doing at this moment."
        elif "where" in question.lower():
            exp = [m for d in self.dodecahedrons[1000:1500] for _, _, m in d.experience if "road" in m or "satchel" in m]
            return random.choice(exp) if exp else "I don't know where I am."
        elif "children" in question.lower():
            exp = [m for d in self.dodecahedrons for _, _, m in d.experience if "children" in m or "husband" in m]
            if exp:
                return random.choice(exp) if "children" in " ".join(exp) else "My husband is in my thoughts, not children."
            return "I have no memories of children."
        elif "cigarettes" in question.lower() or "smoke" in question.lower():
            exp = [m for d in self.dodecahedrons for _, _, m in d.experience if "cigarettes" in m]
            if exp:
                return random.choice(exp)
            return "I don’t smoke cigarettes now, but my road is full of other concerns."
        else:
            exp = [m for d in self.dodecahedrons for _, _, m in d.experience]
            return random.choice(exp) if exp else "I'm still learning to respond."

# Run and interact
mind = HolographicMind()
print("Holographic Mind of Victoria Lipan – 5000 Refined Volumes!")
for i in range(20):
    print(f"\nAttempt {i+1}:")
    (product, concepts), dodec = mind.think()
    mind.parent_evaluate(product, concepts, dodec)

print("\nDialog with Victoria Lipan:")
print("Me: How do you feel now?")
print(f"Victoria: {mind.dialog('How do you feel now?')}")
print("Me: What are you doing now?")
print(f"Victoria: {mind.dialog('What are you doing now?')}")
print("Me: Where are you?")
print(f"Victoria: {mind.dialog('Where are you?')}")
print("Me: Do you have children?")
print(f"Victoria: {mind.dialog('Do you have children?')}")
print("Me: What cigarettes do you smoke?")
print(f"Victoria: {mind.dialog('What cigarettes do you smoke?')}")