# VRP with profits and time deadlines

The capacitated vehicle routing problem (CVRP or simply VRP) is one of the most studied combinatorial optimization problems in the literature of operations research. The main reason for this much attention is the abundance of its real-life applications in distribution logistics and transportation. 

In this project we focus on the single-depot capacitated VRP with profits and time deadlines (VRPP-TD).VRPP-TD is a generalization of the VRP where visiting each customer incurs a fixed revenue, and it is not necessary to visit all customers. The objective is to find the number and routes of vehicles under time deadline restrictions so as to maximize the total profit, which is equal to the total revenue collected from the visited customers less the traveling cost. 

# Problem Description
Consider a central repository (Node with id: 0) and a set of 𝑛 = 200 customers (Nodes with id: 1,…, 𝑛 = 200).
All nodes are on a square side 100. Assume that the transition time from node to node is equal to the Euclidean distance between the two nodes.
Every customer 𝑖 has a required service time 𝑠𝑡i and a profit 𝑝i.
A fleet of 𝑘 = 5 trucks is located in the central warehouse.
The vehicles start at the warehouse, serve customers and return to the main warehouse.
Each car performs one route.
Each customer can be covered (not necessarily as it will be covered) by a single vehicle visit. In this case, the customer returns his profit.
The time of each route (time of transitions and time of customer service) can not exceed a period of time 𝑇 = 150.

The purpose of the problem is to design 𝑘 routes that will maximize overall profit. Obviously, due to the limitations of the maximum time limit, it is not necessary that everyone will be covered customers. Instead, the selected customers must be selected and routed. 

Α. Γράψτε σε python τις κλάσεις, πίνακες και γενικότερα την απαιτούμενη υποδομή για αναπαρασταθεί το 
πρόβλημα (3).
Οι κόμβοι αποθήκη και πελάτες να δημιουργούνται και να φυλάσσονται όπως φαίνεται στον παρακάτω 
κώδικα:

all_nodes = [] 

d = Node(0, 50, 50, 0, 0) 

all_nodes.append(d) 

birthday = 3112000 

random.seed(birthday)

for i in range(0, 200): 

 xx = random.randint(0, 100) 
 
 yy = random.randint(0, 100) 
 
 service_time = random.randint(5, 10)
 
 profit = random.randint(5, 20) 
 
 cust = Node(i+1, xx, yy, service_time, profit) 
 
 all_nodes.append(cust)
 
 όπου birthday η ημέρα γενεθλίων του αρχηγού της ομάδας. 

Β. Φτιάξτε έναν κατασκευαστικό αλγόριθμο ο οποίος θα σχηματίζει μία ολοκληρωμένη λύση (3). 

Γ. Γράψτε σε Python τέσσερεις τελεστές τοπικής έρευνας (3) 
  1. Relocate: Επανατοποθέτηση κάθε καλυπτόμενου πελάτη σε οποιοδήποτε διαφορετικό σημείο 
  της λύσης. 
  2. Swap: Αντιμετάθεση των θέσεων εξυπηρέτησης οποιουδήποτε ζεύγους καλυπτόμενων 
  πελατών. 
  3. Insertion: Εισαγωγή ενός οποιουδήποτε μη καλυπτόμενου πελάτη σε οποιοδήποτε σημείο της 
  λύσης. 
  4. Profitable Swap: Αντικατάσταση οποιουδήποτε καλυπτόμενου πελάτη με οποιονδήποτε μη 
  καλυπτόμενο πελάτη. 
  
Δ. Γράψτε σε Python μία VND μέθοδο η οποία θα χρησιμοποιεί τους τελεστές του ερωτήματος (Γ) και θα 
βελτιώνει τη λύση του ερωτήματος (Β). Ποια είναι η τελική λύση. Ποιο το κόστος της και μετά από πόσες 
επαναλήψεις του αλγορίθμου δημιουργήθηκε (1);
