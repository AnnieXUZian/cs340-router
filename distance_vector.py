from simulator.node import Node
import json

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.node_distance_path_table = {}      #table of who they can connect to, what cost
        self.neighbor_tables = {}               #table of what can be reached thru neighbors

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        link=frozenset([self.id, neighbor])
        # latency = -1 if delete a link
        seq_num=0
        if latency == -1 and neighbor in self.neighbors:    ###DELETE A LINK####
            self.neighbors.remove(neighbor)
            seq_num=self.node_distance_path_table[link]["seq_num"] + 1 #newest information available
            self.node_distance_path_table.pop(link)     #remove the link from the table- no longer available
            self.neighbor_tables.pop(neighbor)              #also remove it from the neighbor table



        elif neighbor in self.neighbors:        ###UPDATE A LINK###
            seq_num = self.node_distance_path_table[link]["seq_num"] + 1 #newest info available
            self.node_distance_path_table[link]["seq_num"]+=1              #updates the sequence num
            self.node_distance_path_table[link]['latency'] = latency       #updates latency num
            #self.neighbor_tables ------------------------------- this does not change the neighbor table?
            
                #BELLMAN FORD ALGORITHM MOMENT
            for i in self.node_distance_path_table.keys():                  #iterate thru the keys
                for node in i:
                    if node not in self.node_distance_path_table and c == 1:
                        temp.append(node)                                   # get num of vertices 
                        self.neighbor_tables[node] = 0 
                        c = 0
                    elif node not in self.node_distance_path_table:
                        temp.append(node)
                        self.neighbor_tables[node] = -1                             

            for i in range(len(temp)):             # iterate thru vertices
                for j in self.node_distance_path_table.keys():
                    src_edge, *_ = j
                    *_, end_edge = j 
                    weight = self.node_distance_path_table[j]['latency']
                    
                    if self.neighbor_tables[end_edge] != -1 and (self.neighbor_tables[src_edge] + weight) < self.neighbor_tables[end_edge]:
                        self.neighbor_tables[end_edge] = {self.neighbor_tables[src_edge] + weight}
                    elif(self.neighbor_tables[end_edge] == -1):
                        self.neighbor_tables[end_edge] = self.neighbor_tables[src_edge] + weight



        else:           ###ADD A LINK###
            for i in self.node_distance_path_table.keys():
                temp=[]
                for node in i:
                    temp.append(node)
                    
                entries = []
                keys = []
                for i in self.neighbor_tables.keys():
                    entries.append(self.neighbor_tables[i])       
                    keys.append(i)
                
                message = json.dumps(
                    {'source': temp[0], 'dest': temp[1], 'latency': self.node_distance_path_table[i]["latency"], 'seq_num': self.node_distance_path_table[i]["seq_num"], 'DV_table_keys': self.node_distance_path_table.keys()})
                self.send_to_neighbor(neighbor, message)
            self.neighbors.append(neighbor)
            seq_num = 1
            self.node_distance_path_table[link]={"latency":latency,"seq_num":1}
            
                #BELLMAN FORD ALGORITHM
            temp=[]
            # print(self.node_distance_path_table.keys())
            c=1
            for i in self.node_distance_path_table.keys():                  #iterate thru the keys
                for node in i:
                    if node not in self.node_distance_path_table.keys() and c == 1:
                        temp.append(node)                                   # get num of vertices 
                        self.neighbor_tables[node] = 0 
                        c = 0
                    elif node not in self.node_distance_path_table.keys():
                        temp.append(node)
                        self.neighbor_tables[node] = -1                             

            for i in range(len(temp)):             # iterate thru vertices
                for j in self.node_distance_path_table.keys():
                    src_edge, *_ = j
                    *_, end_edge = j 
                    weight = self.node_distance_path_table[j]['latency']

                    if self.neighbor_tables[end_edge] != -1 and (self.neighbor_tables[src_edge] + weight) < self.neighbor_tables[end_edge]:
                        self.neighbor_tables[end_edge] = {self.neighbor_tables[src_edge] + weight}
                    elif(self.neighbor_tables[end_edge] == -1):
                        self.neighbor_tables[end_edge] = self.neighbor_tables[src_edge] + weight

        print(self.node_distance_path_table)
        print(self.neighbor_tables)    

        entries = []
        keys = []
        for i in self.neighbor_tables.keys():
            entries.append(self.neighbor_tables[i])       
            keys.append(i)

        #send message to neighbors
        msg = json.dumps(
            {'source': neighbor, 'dest': self.id, 'latency': latency, 'seq_num': seq_num, 'DV_table_keys': keys, 'DV_table_entries' : entries})
        self.send_to_neighbors(msg)
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        msg=json.loads(m)
        source = msg['source']
        dest = msg['dest']
        latency = msg['latency']
        seq_num = msg['seq_num']
        incoming_table = msg['DV_table']
        link = frozenset([source, dest])

        if latency==-1 and link in self.node_distance_path_table.keys():#new message-delete
            self.node_distance_path_table.pop(link)
            self.neighbor_tables.pop(source)
            self.send_to_neighbors(m)

        elif link in self.node_distance_path_table.keys():
            if seq_num > self.node_distance_path_table[link]['seq_num']: #new message-update
                self.node_distance_path_table[link]['seq_num']=seq_num
                self.node_distance_path_table[link]['latency']=latency
                self.neighbor_tables[source] = incoming_table
                self.send_to_neighbors(m)
            elif seq_num < self.node_distance_path_table[link]['seq_num']:#old message-------------maybe it should be link and not source?
                message = json.dumps
                {'source': source, 'dest': dest, 'latency': self.node_distance_path_table[link]['latency'], 'seq_num': self.node_distance_path_table[link]['seq_num'], 'DV_table': self.neighbor_tables[source]}
                self.send_to_neighbors(message)

        elif latency != -1: #new message-add
            self.node_distance_path_table[link] = {"latency": latency, "seq_num": 1}
            self.neighbor_tables[source] = {"neighbor": source, "DV_table": incoming_table}
            self.send_to_neighbors(m)

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.neighbor_tables:
            return self.neighbor_tables[destination]
        else:
            return -1

       
