import networkx as nx


class SocialNetwork:
    def __init__(self):
        self.G = nx.Graph()
        self.members = []
        self.social_NW = {}

    def read_data(self):
        while True:
            filename = input("Please enter the file name or type 'n' to exit: ")
            if filename == 'n':
                break
            try:
                with open(filename, 'r') as f:
                    n = int(f.readline())
                    for line in f:
                        line = line.strip()
                        if line != "":
                            try:
                                parts = line.split()
                                if len(parts) == 1:
                                    continue
                                u, v = parts
                                self.add_edge(u, v)
                            except ValueError:
                                print(f'Line "{line}" in file {filename} has an incorrect format')
                break
            except FileNotFoundError:
                print(f"File not found. Please try again.")

    def add_edge(self, u, v):
        self.G.add_edge(u, v)
        if u not in self.members:
            self.members.append(u)
            self.social_NW[u] = [v]
        else:
            self.social_NW[u].append(v)
        if v not in self.members:
            self.members.append(v)
            self.social_NW[v] = [u]
        else:
            self.social_NW[v].append(u)

    def add_member(self, member):
        self.members[member] = set()

    def add_friend(self, member1, member2):
        self.members[member1].add(member2)
        self.members[member2].add(member1)

    def remove_edge(self, u, v):
        self.G.remove_edge(u, v)
        self.social_NW[u].remove(v)
        self.social_NW[v].remove(u)

    def display_network(self):
        while True:
            display = input("Do you want to display the social network? (y/n)")
            if display.lower() == "y":
                for member, friends in self.social_NW.items():
                    print(f"{member} -> ", end="")
                    for friend in friends:
                        print(f"{friend}, ", end="")
                    print()
                break
            elif display.lower() == "n":
                break
            else:
                print("Please try again (PRESS Y TO VIEW SOCIAL NETWORK OR N)")

    def recommend_friends(self):
        recommendations = {}
        for member in self.members:
            friends = {}
            for neighbor in self.G.neighbors(member):
                friends[neighbor] = len(list(nx.common_neighbors(self.G, member, neighbor)))
            recommendations[member] = max(friends, key=friends.get)
        for member, friend in recommendations.items():
            print(f"{member}'s recommended friend is {friend}")

    def common_friends(self):
        common_friends = {}
        for member1 in self.members:
            common_friends[member1] = []
            for member2 in self.members:
                if member1 == member2:
                    common_friends[member1].append(0)
                else:
                    common_friends[member1].append(len(list(nx.common_neighbors(self.G, member1, member2))))
        return common_friends

    def display_num_friends(self):
        member = input("Enter a member name to check their number of friends: ")
        if member not in self.members:
            print(f"Error: {member} is not a member of the social network.")
        else:
            num_friends = len(self.social_NW[member])
            print(f"{member} has {num_friends} friends.")

    def display_least_friends(self):
        user_input = input("Would you like to display the members with the least friends? (y/n)")
        if user_input != "y":
            return
        if not self.members:
            print("No members in the network.")
            return
        if not any(self.social_NW.values()):
            print("No friends in the network.")
            return
        least_friends = sorted([(member, len(friends)) for member, friends in self.social_NW.items()],
                               key=lambda x: x[1])
        print("Members with least friends:")
        for member, num_friends in least_friends[:3]:
            print(f"{member} has {num_friends} friends.")


if __name__ == '__main__':
    sn = SocialNetwork()
    sn.read_data()
    sn.display_network()
    display_common_friends = input("Would you like to display common friends? (y/n)")
    if display_common_friends.lower() == "y":
        common_friends = sn.common_friends()
        for member, counts in common_friends.items():
            print(f"{member} -> {counts}")
    display_recommend_friends = input("Would you like to display recommended friends? (y/n)")
    if display_recommend_friends.lower() == "y":
        friends = sn.recommend_friends()
    sn.display_num_friends()
    sn.display_least_friends()
    sn = SocialNetwork()
