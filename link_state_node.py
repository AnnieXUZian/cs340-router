from simulator.node import Node
import json

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.lsdb = {}
    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        link=frozenset([self.id, neighbor])
        # latency = -1 if delete a link
        seq_num=0
        if latency == -1 and neighbor in self.neighbors: #delete a link
            self.neighbors.remove(neighbor)
            seq_num=self.lsdb[link]["seq_num"] + 1
            self.lsdb.pop(link)
        elif neighbor in self.neighbors: #update a link
            seq_num = self.lsdb[link]["seq_num"] + 1
            self.lsdb[link]["seq_num"]+=1
            self.lsdb[link]['latency'] = latency
        else: #add a link
            for i in self.lsdb.keys():
                temp=[]
                for node in i:
                    temp.append(node)
                message = json.dumps(
                    {'source': temp[0], 'dest': temp[1], 'latency': self.lsdb[i]["latency"], 'seq_num': self.lsdb[i]["seq_num"]})
                self.send_to_neighbor(neighbor, message)
            self.neighbors.append(neighbor)
            seq_num = 1
            self.lsdb[link]={"latency":latency,"seq_num":1}
        #send message to neighbors
        msg = json.dumps(
            {'source': neighbor, 'dest': self.id, 'latency': latency, 'seq_num': seq_num})
        self.send_to_neighbors(msg)
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        msg=json.loads(m)
        source = msg['source']
        dest = msg['dest']
        latency = msg['latency']
        seq_num = msg['seq_num']
        link = frozenset([source, dest])
        if latency==-1 and link in self.lsdb.keys():#new message-delete
            self.lsdb.pop(link)
            self.send_to_neighbors(m)
        elif link in self.lsdb.keys():
            if seq_num > self.lsdb[link]['seq_num']: #new message-update
                self.lsdb[link]['seq_num']=seq_num
                self.lsdb[link]['latency']=latency
                self.send_to_neighbors(m)
            elif seq_num < self.lsdb[link]['seq_num']:#old message
                message = json.dumps(
                {'source': source, 'dest': dest, 'latency': self.lsdb[link]['latency'], 'seq_num': self.lsdb[link]['seq_num']})
                self.send_to_neighbors(message)
        elif latency != -1: #new message-add
            self.lsdb[link] = {"latency": latency, "seq_num": 1}
            self.send_to_neighbors(m)


    # Return a neighbor, -1 if no path to destination
    def get_key(self,dict,value):
        for key in dict.keys():
            if dict[key]==value:
                return key


    def get_next_hop(self, destination):
        # get all nodes
        nodes=[]
        dist={}
        prev={}
        links=list(self.lsdb.keys())
        for link in self.lsdb.keys():
            for node in link:
                if node not in nodes:
                    nodes.append(node)
        # Dijkstra's Algorithm
        dist[destination]=0
        prev[destination]=-1
        while len(nodes) > 0:
            mdist = min(dist.values())
            mnode=self.get_key(dist, mdist)
            if mnode==self.id:
                return prev[self.id]
            #get the neighbor of mnode
            for link in links:
                if mnode in link:
                    for node in link:
                        if node != mnode:
                            alt=dist[mnode]+self.lsdb[link]['latency']
                            if node in dist.keys():
                                if alt < dist[node]:
                                    dist[node]=alt
                                    prev[node] = mnode
                            else:
                                dist[node] = alt
                                prev[node] = mnode
            nodes.remove(mnode)
            temp=[]
            for i in links:
                if mnode in i:
                    temp.append(i)
            for i in temp:
                links.remove(i)
            dist.pop(mnode)




