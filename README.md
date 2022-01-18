#Problem Decription

The capacitated vehicle routing problem (CVRP or simply VRP) is one of the 
most studied combinatorial optimization problems in the literature of operations 
research. The main reason for this much attention is the abundance of its real-life 
applications in distribution logistics and transportation. 

In this project we focus on the single-depot capacitated VRP with profits and time deadlines (VRPPTD).VRPP-TD is a generalization of the VRP where visiting each customer incurs a fixed revenue, and it is not necessary to visit all customers. The objective is to find the number and routes of vehicles under time deadline restrictions so as to maximize the total profit, which is equal to the total revenue collected from the visited customers less the traveling cost. 

Θεωρήστε μία κεντρική αποθήκη (Κόμβος με id: 0) και ένα σύνολο 𝑛 = 200 πελατών (Κόμβοι με id: 1,…,𝑛=200).

Όλοι οι κόμβοι βρίσκονται σε ένα τετράγωνο πλευράς 100. Θεωρήστε πως ο χρόνος μετάβασης από κόμβο σε κόμβο είναι ίσος με την Ευκλείδεια απόσταση μεταξύ των δύο κόμβων. 

Κάθε πελάτης 𝑖 έχει έναν απαιτούμενο χρόνο εξυπηρέτησης 𝑠𝑡i και ένα κέρδος 𝑝i.

Ένας στόλος 𝑘 = 5 φορτηγών αυτοκινήτων βρίσκεται στην κεντρική αποθήκη. 

Τα οχήματα ξεκινούν από την αποθήκη, εξυπηρετούν πελάτες και κατόπιν επιστρέφουν πίσω στην κεντρική αποθήκη. 

Κάθε όχημα εκτελεί μία διαδρομή.

Κάθε πελάτης μπορεί να καλυφθεί (δεν είναι αναγκαίο πως θα καλυφθεί) από μία επίσκεψη ενός και μόνο οχήματος. Στην περίπτωση αυτή, ο πελάτης αποδίδει το κέρδος του.

Ο συνολικός χρόνος κάθε διαδρομής (χρόνος μεταβάσεων και χρόνος εξυπηρέτησης πελατών) δε μπορεί να υπερβαίνει ένα χρονικό όριο 𝑇 = 150. 

Σκοπός του προβλήματος είναι ο σχεδιασμός 𝑘 διαδρομών οι οποίες θα μεγιστοποιούν το συνολικό κέρδος. 
Προφανώς, λόγω των περιορισμών του μέγιστου χρονικού ορίου δεν είναι απαραίτητο πως θα καλυφθούν όλοι 
οι πελάτες. Αντίθετα, πρέπει να επιλεγούν και να δρομολογηθούν οι επιλεγμένοι πελάτες. 

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
