import networkx as nx
import pandas
import pylab as plt  #import Matplotlib plotting interface

def create_adjlist():
    f = open('myfile.adjlist', 'w')
    for i in range(0,20):
        #write row country in same line
        row = df.index[i]
        f.write(row)
        for j in range(0,20):
            if df.iloc[i,j] == 1:
                #write column country in same line
                col = df.columns[j]
                f.write(" "+col)
        #new line
        if(i != 19):
            f.write("\n")
    f.close()

def draw_graph():
    graph_pos = nx.spring_layout(G)
    # draw nodes, edges and labels
    nx.draw_networkx_nodes(G, graph_pos, node_size=250  , node_color='blue', alpha=0.15)
    nx.draw_networkx_edges(G, graph_pos, edge_color='red')
    nx.draw_networkx_labels(G, graph_pos, font_size=10, font_family='sans-serif', font_color='black')
    #plt.savefig("graph.png")
    # show graph
    plt.show()

def calculate_power():
    bet_cen = nx.betweenness_centrality(G)
    clo_cen = nx.closeness_centrality(G)
    eig_cen = nx.eigenvector_centrality(G)
    max_bet_cen = highest_centrality(bet_cen)
    max_clo_cen = highest_centrality(clo_cen)
    max_eig_cen = highest_centrality(eig_cen)
    return (max_bet_cen,max_clo_cen,max_eig_cen)

def highest_centrality(cent_dict):
    cent_items=[(b,a) for (a,b) in cent_dict.items()]
    cent_items.sort()
    cent_items.reverse()
    return tuple(reversed(cent_items[0]))

def link_prediction():
    india = 6
    leng = 20
    for col in range(0,leng):
        if col == india:
            continue
        if df.iloc[india,col]==1:
            continue
        else:
            df.iloc[india,col]=1
            df.iloc[col,india]=1
            find_new_powers(india,col)
            df.iloc[india,col]=0
            df.iloc[col,india]=0

def find_new_powers(india, col):
    global G,max_cen,country
    create_adjlist()
    fh=open("myfile.adjlist", 'rb')
    G=nx.read_adjlist(fh)
    fh.close()
    #draw_graph()
    powers = calculate_power()
    #print("\nPowers if India forms a link with: "+df.columns[col])
    #print(str(powers[0])+"\n"+str(powers[1])+"\n"+str(powers[2])+"\n")
    ind_cen = indian_power()
    avg_cen = (ind_cen[0]+ind_cen[1]+ind_cen[2])/3
    if avg_cen > max_cen:
        max_cen = avg_cen
        country = col
        a["new_max_centralities"] = powers
        a["new_indian_centralities"] = ind_cen

def indian_power():
    bet_cen = nx.betweenness_centrality(G)['India']
    clo_cen = nx.closeness_centrality(G)['India']
    eig_cen = nx.eigenvector_centrality(G)['India']
    #print("New centralities of India:")
    #print('bet_cen: '+str(bet_cen)+'\t\tchange: '+str(bet_cen-a[0]))
    #print('clo_cen: '+str(clo_cen)+'\t\tchange: '+str(clo_cen-a[1]))
    #print('eig_cen: '+str(eig_cen)+'\t\tchange: '+str(eig_cen-a[2]))
    return (bet_cen, clo_cen, eig_cen)

def print_link():
    print("\nOriginal_max_centralities:\n"+str(a["original_max_centralities"]))
    print("\nOriginal_indian_centralities:\n"+str(a["original_indian_centralities"]))

    if country == -1:
        print("\n
        No such country found!")
    else:
        a["link"] = df.columns[country]
        print("\nThe country with whom, India would get maximum increase in its centrality is: "+a["link"])
        print("\nNew Indian centralities:\n"+str(a["new_indian_centralities"]))
        print("\nNew_max_centralities:\n"+str(a["new_max_centralities"]))


################################################################################################################
##############################               MAIN            ###################################################
################################################################################################################
a = {
    "original_max_centralities":"",
    "original_indian_centralities":"",
    "link":"",
    "new_indian_cetralities":""
}

df = pandas.read_csv("sin_dataset.csv")
df = df.set_index("Countries")
create_adjlist()
fh=open("myfile.adjlist", 'rb')
G=nx.read_adjlist(fh)
fh.close()
powers = calculate_power()
a["original_max_centralities"] = powers
#print("\nCurrent Powers:\n"+str(powers[0])+"\n"+str(powers[1])+"\n"+str(powers[2])+"\n")
a["original_indian_centralities"] = (nx.betweenness_centrality(G)['India'], nx.closeness_centrality(G)['India'], nx.eigenvector_centrality(G)['India'])
max_cen = (a["original_indian_centralities"][0]+a["original_indian_centralities"][1]+a["original_indian_centralities"][2])/3
country = -1
link_prediction()
print_link()