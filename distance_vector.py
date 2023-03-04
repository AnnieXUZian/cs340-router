from simulator.node import Node
import json
# SOMETHING WRONG WITH SEQ NUM?
class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.node_distance_path_table = {}      #table of who they can connect to, what cost
        self.neighbor_tables = {}               #table of what can be reached thru neighbors
        self.c = 20

            # IMPLEMENTATION TOOLS:

        # node_distance_path_table:     {end_vertex, {latency, seq_num}}
        # neighbor_table:               {neighbor, [tuple]}
        # tuple =   (end_vertex, latency)

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"
    
    def bellman_ford(self, seq_num):
        for neighbor in self.neighbor_tables.keys():                             #iterate thru the neighbors (vertices)
            print('neighbors: ' + str(self.neighbors))
            for tuple in self.neighbor_tables[neighbor]:            #iterate thru the edges for each neighbor
                if tuple[0] not in self.node_distance_path_table.keys() and self.id != neighbor:                   #if there is no length already, set len to whatever is in the neighbor's DV
                    self.node_distance_path_table[frozenset([self.id, tuple[0]])] = {'latency': self.node_distance_path_table[frozenset([self.id, neighbor])]['latency'] + tuple[1], "seq_num": seq_num}    # tuple0latency->end point cost set to: cost src to neighbor+cost neigbor to end point
                elif self.id != tuple[0] and self.id != neighbor:
                    if self.node_distance_path_table[frozenset([self.id, tuple[0]])]['latency'] > self.node_distance_path_table[frozenset([self.id, neighbor])]['latency'] + tuple[1]:    # if current distance larger than distance to neighbor+distance neighbor->end point,
                        self.node_distance_path_table[frozenset([self.id, tuple[0]])]['latency'] = self.node_distance_path_table[frozenset([self.id, neighbor])]['latency'] + tuple[1]      # set new distance to       distance to neighbor+distance neighbor->end point.
                    self.node_distance_path_table[frozenset([self.id, tuple[0]])]['seq_num'] = seq_num    
        return

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        link=frozenset([self.id, neighbor])
        # latency = -1 if delete a link
        seq_num=0


        if latency == -1 and neighbor in self.neighbors:    ###DELETE A LINK####
            self.neighbors.remove(neighbor)
            seq_num=self.node_distance_path_table[link]["seq_num"] + 1 #newest information available
            self.node_distance_path_table
            print("deleting "+str(link))


            # HOW TO DO DELETE?


        elif neighbor in self.neighbors:        ###UPDATE A LINK###
            seq_num = self.node_distance_path_table[link]["seq_num"] + 1 #newest info available
            self.node_distance_path_table[link]["seq_num"]+=1              #updates the sequence num
            self.node_distance_path_table[link]['latency'] = latency       #updates latency num
            print("updating "+ str(link))

        else: #add a link                   ------------------------ HAVE TO TAKE INTO ACCOUNT THE FIRST NODE
            
            self.neighbors.append(neighbor)
            seq_num = 1
            self.node_distance_path_table[link]={"latency":latency,"seq_num": seq_num} 
            x, *_ = link
            *_, y = link
            print(x,y)
            if x in self.neighbor_tables:
                previous_entries = self.neighbor_tables[x]
                print("Previous entries: "+str(previous_entries))
                self.neighbor_tables[x] = previous_entries.append((y, latency))
            else:
                self.neighbor_tables[x] = [(y, latency)]
            print("Before algorithm " +str(self.node_distance_path_table))
            print(self.neighbor_tables)

         #BELLMAN FORD ALGORITHM MOMENT
        self.bellman_ford(seq_num)                           


        #send message to neighbors ----------------------- HOW TO SEND DV TABLE?----------------------------------------
        print("After Algorithm: "+ str(self.node_distance_path_table))
        print(self.neighbor_tables)
        end_vertices = []
        costs = []
        for i in self.node_distance_path_table.keys():
            for node in i:
                if node not in end_vertices:
                    end_vertices.append(node)
                    costs.append(self.node_distance_path_table[i]['latency'])

        msg = json.dumps(
            {'source': neighbor, 'dest': self.id, 'latency': latency, 'seq_num': seq_num, 'DV_endpoints': end_vertices, 'DV_costs': costs})
        self.send_to_neighbors(msg)
        print("sent message")
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        self.c = self.c-1
        print('received message')
        
        msg=json.loads(m)
        source = msg['source']
        dest = msg['dest']
        latency = msg['latency']
        seq_num = msg['seq_num']
        DV_endpoints = msg['DV_endpoints']
        DV_costs = msg['DV_costs']
        link = frozenset([source, dest])


        print('RECEIVED MESSAGE DV STUFF')
        print(DV_endpoints, DV_costs)

        entry_list = []
        for i in range(len(DV_endpoints)):
            if DV_endpoints[i] not in entry_list:
                entry_list.append((DV_endpoints[i], DV_costs[i]))
        # self.neighbor_tables[source] = entry_list

        if latency==-1 and link in self.node_distance_path_table.keys():#new message-delete
            self.node_distance_path_table.pop(link)
            self.neighbor_tables.pop(dest)                  # COULD ACTUALLY BE THE SOURCE INSTEAD? TO DO 
            # self.send_to_neighbors(m)

        elif link in self.node_distance_path_table.keys():
            if self.c > 0:
                
                if seq_num > self.node_distance_path_table[link]['seq_num']: #new message-update
                    self.node_distance_path_table[link]['seq_num']=seq_num
                    self.node_distance_path_table[link]['latency']=latency
                    self.neighbor_tables[source] = entry_list
                    # self.send_to_neighbors(m)
            # elif seq_num < self.node_distance_path_table[link]['seq_num']:#old message----IF AN OLD SEQ NUM, CONTINUE TO SEND TO NEIGHBORS (SEND SPECIFICALLY BACK TO THAT ONE)
            #     message = json.dumps
            #     {'source': source, 'dest': dest, 'latency': self.node_distance_path_table[link]['latency'], 'seq_num': self.node_distance_path_table[link]['seq_num'], 'DV_table': self.neighbor_tables[source]}
                

        elif latency != -1: #new message-add
            if seq_num > self.node_distance_path_table[link]['seq_num']: #new message-update
                self.lsdb[link]['seq_num']=seq_num
                self.lsdb[link]['latency']=latency
                self.send_to_neighbors(m)
            elif seq_num < self.lsdb[link]['seq_num']:#old message
                message = json.dumps(
                {'source': source, 'dest': dest, 'latency': self.lsdb[link]['latency'], 'seq_num': self.lsdb[link]['seq_num']})
                self.send_to_neighbors(message)
            self.node_distance_path_table[link] = {"latency": latency, "seq_num": 1}
            self.neighbor_tables[source] = entry_list
            # self.send_to_neighbors(m)

       
        if seq_num > self.node_distance_path_table[link]['seq_num']:#new message- update ------------maybe it should be link and not source?
            self.bellman_ford(seq_num)

            end_vertices = []
            costs = []
            for i in self.node_distance_path_table.keys():
                for node in i:
                    if node not in end_vertices:
                        end_vertices.append(node)
                        costs.append(self.node_distance_path_table[i]['latency']) 

            message = json.dumps(
                {'source': neighbor, 'dest': self.id, 'latency': latency, 'seq_num': seq_num, 'DV_endpoints': end_vertices, 'DV_costs': costs}
            )


        else:  # if seq_num > self.node_distance_path_table[link]['seq_num']: #new message-update  
            end_vertices = []
            costs = []
            for i in self.node_distance_path_table.keys():
                for node in i:
                    if node not in end_vertices:
                        end_vertices.append(node)
                        costs.append(self.node_distance_path_table[i]['latency'])

            message = json.dumps(
            {'source': source, 'dest': dest, 'latency': self.node_distance_path_table[link]['latency'], 'seq_num': self.node_distance_path_table[link]['seq_num'], 'DV_endpoints': end_vertices, 'DV_costs': costs})
                
            self.send_to_neighbors(message)



    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        end_point_reached = None
        hop_list = []
        while end_point_reached != destination:

            print('getting next hop')
            if destination in self.neighbor_tables:
                return self.neighbor_tables[destination]
        else:
            return -1

       
