from simulator.node import Node
import json

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.node_distance_path_table = {}      #table of who they can connect to, what cost
        self.neighbor_tables = {}               #table of what can be reached thru neighbors

            # IMPLEMENTATION TOOLS:

        # node_distance_path_table:     {end_vertex, {latency, seq_num}}
        # neighbor_table:               {neighbor, [tuple]}
        # tuple =   (end_vertex, latency)

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
            self.node_distance_path_table


            # HOW TO DO DELETE?


        elif neighbor in self.neighbors:        ###UPDATE A LINK###
            seq_num = self.node_distance_path_table[link]["seq_num"] + 1 #newest info available
            self.node_distance_path_table[link]["seq_num"]+=1              #updates the sequence num
            self.node_distance_path_table[link]['latency'] = latency       #updates latency num


        else: #add a link                   ------------------------ HAVE TO TAKE INTO ACCOUNT THE FIRST NODE
#-------------------------------COMMENTED OUT FOR CLARITY-------------------------------------------#

            # for i in self.lsdb.keys():
            #     temp=[]
            #     for node in i:
            #         temp.append(node)
            #     message = json.dumps(
            #         {'source': temp[0], 'dest': temp[1], 'latency': self.node_distance_path_table[i]["latency"], 'seq_num': self.node_distance_path_table[i]["seq_num"]})
            #     self.send_to_neighbor(neighbor, message)
                
            self.neighbors.append(neighbor)
            seq_num = 1
            self.node_distance_path_table[link]={"latency":latency,"seq_num":1}
            self.neighbor_tables[neighbor] = [(neighbor, latency)]
            

         #BELLMAN FORD ALGORITHM MOMENT
        for neighbor in self.neighbors:                             #iterate thru the neighbors (vertices)
            for tuple in self.neighbor_tables[neighbor]:            #iterate thru the edges for each neighbor
                if tuple not in self.node_distance_path_table.keys():                   #if there is no length already, set len to whatever is in the neighbor's DV
                    self.node_distance_path_table[tuple[0]]['latency'] = self.node_distance_path_table[neighbor]['latency'] + tuple[1]    # tuple0latency->end point cost set to: cost src to neighbor+cost neigbor to end point
                elif self.node_distance_path_table[tuple[0]]['latency'] > self.node_distance_path_table[neighbor]['latency'] + tuple[1]:    # if current distance larger than distance to neighbor+distance neighbor->end point,
                    self.node_distance_path_table[tuple[0]]['latency'] = self.node_distance_path_table[neighbor]['latency'] + tuple[1]      # set new distance to       distance to neighbor+distance neighbor->end point.
                self.node_distance_path_table[tuple[0]]['seq_num'] = seq_num                            

        entries = []
        keys = []
        for i in self.neighbor_tables.keys():
            entries.append(self.neighbor_tables[i])       
            keys.append(i)

        #send message to neighbors
        msg = json.dumps(
            {'source': neighbor, 'dest': self.id, 'latency': latency, 'seq_num': seq_num, 'DV_table': self.neighbor_tables})
        self.send_to_neighbors(msg)
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        msg=json.loads(m)
        source = msg['source']
        dest = msg['dest']
        latency = msg['latency']
        seq_num = msg['seq_num']
        incoming_keys = msg['DV_table_keys']
        incoming_entries = msg['DV_table_entries']
        link = frozenset([source, dest])

        if latency==-1 and link in self.node_distance_path_table.keys():#new message-delete
            self.node_distance_path_table.pop(link)
            self.neighbor_tables.pop(source)
            self.send_to_neighbors(m)

            #NEED TO REFIND THE WAYS TO PLACES

        elif link in self.node_distance_path_table.keys():
            if seq_num > self.node_distance_path_table[link]['seq_num']: #new message-update
                self.node_distance_path_table[link]['seq_num']=seq_num
                self.node_distance_path_table[link]['latency']=latency
                # for i in incoming_keys:
                    #self.neighbor_tables[i] = 
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

       

    
