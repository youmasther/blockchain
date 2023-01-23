from blockchain import *
import datetime


blockchain = MinimalChain()

json_path = 'data.json'
save_path = '.save_data.json'
json_data = read_json(json_path)
save_data = read_json(save_path)

if json_data:
    blockchain.blocks = sorted(json_data, key=lambda block: block['index'], reverse=False)

# if save_path:
#     nodes_list = sorted(nodes_data, key=lambda node: node['index'], reverse=False)

message = """
		1. Taper 1 pour ajouter un achat
		2. Taper 2 pour lister les achats précédents
		3. Taper 3 pour quitter .
		--------------------------------------------------
"""

choix = int(input(f"{message}"))

while choix != 1 and choix != 2 and choix != 3:
	choix = int(input(f"{message}"))

if choix == 1:
	prenom = input("Donner le prenom du client: ")
	nom = input("Donner le nom du client: ")
	produit = input("Donner le nom du produit: ")
	prix = input("Donner le prix du produit: ")

	data = {
		"prenom": prenom,
		"nom": nom,
		"produit": produit,
		"prix": prix,
		# "date_facturation": str(datetime.datetime.utcnow()).encode('utf-8')
	}

	blockchain.add_block(data)
	blockchain.blocks[-1]["date_facturation"] = blockchain.blocks[-1]["timestamp"]
	flag, message = blockchain.verify()
	print(message)
	if flag:
		write_json(json_path, blockchain.blocks)
		write_json(save_path, blockchain.blocks)
	else:
		blockchain.blocks = sorted(save_data, key=lambda block: block['index'], reverse=False)
		write_json(json_path, blockchain.blocks)
		
elif choix == 2:
	for i in range(1, blockchain.get_chain_size()):
		facture= f"""
				Date de facturation : {blockchain.blocks[i]["date_facturation"]}
				Prenom et nom du client : {blockchain.blocks[i]["data"]["prenom"]} {blockchain.blocks[i]["data"]["nom"]}
				Nom du produit: {blockchain.blocks[i]["data"]["produit"]}
				Prix du produit: {blockchain.blocks[i]["data"]["prix"]}
				{100 * "-"}
		"""
		print(facture)
elif choix == 3:
	print("bye bye à la prochaine")