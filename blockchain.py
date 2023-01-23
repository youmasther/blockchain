import hashlib
import datetime
import json


class MinimalBlock():
    """
    cette class represente un block
    """
    def __init__(self, index, timestamp, date_facturation, data, previous_hash):
        """
        le constructeur de la class 
        """
        self.index = index
        self.timestamp = timestamp
        self.date_facturation = date_facturation
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()
       
    def hashing(self):
        """
        cette methode permet de crypter le block
        """
        data = self.data
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        if isinstance(data, dict):
            key.update(json.dumps(data, sort_keys= True).encode('utf-8'))
        else:
            key.update(str(data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()

    def dic_block(self):
        return {
            "index": self.index,
            'timestamp': str(self.timestamp),
            'date_facturation': str(self.date_facturation),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }

class MinimalChain():
    """
    cette class represente une chaine de block
    """
    def __init__(self):
        """
        le constructeur de la class MinimalChain
        """
        self.blocks = [self.get_genesis_block()]
        # self.nodes = set() #New

    def get_genesis_block(self):
        """
        cette methode permet de créer le block de debut
        """
        return MinimalBlock(
            0,
            datetime.datetime.utcnow(),
            '',
            'arbitraire',
            'Block de debut',
        ).dic_block()

   
    
    def add_block(self, data):
        """
        cette methode permet d'ajouter un nouveau block
        """
        self.blocks.append(MinimalBlock(
            len(self.blocks),
            datetime.datetime.utcnow(),
            '',
            data,
            self.blocks[-1]["hash"]
        ).dic_block())
    
    def get_chain_size(self):
        """
        Cette methode permet de nous donner la taille de la chaine
        """
        return len(self.blocks)

    def verify(self, verbose = True):
        """
        Cette methode permet de verifier si la chaine est valide 
        """
        flag = True
        message = "La chaine est valide "
        for i in range(1, len(self.blocks)):
            if int(self.blocks[i]["index"]) != i:
                flag = False
               
                if verbose :
                    message= f'le block {i} n\'est pas à la bonne place'
            if self.blocks[i - 1]['hash'] != self.blocks[i]['previous_hash']:
                flag = False
                if verbose :
                    message= f'Le block {i} ne suit pas la logique de la chaine'
            # block = MinimalBlock(self.blocks[i]['index'], self.blocks[i]['timestamp'], self.blocks[i]['data'], self.blocks[i]['previous_hash'])
            # if self.blocks[i]['hash'] != block.hash:
            #     flag = False
            #     if verbose:
            #         message= f'le cryptage du block {i} n\'pas correct'
            if self.blocks[i - 1]["timestamp"] >= self.blocks[i]["timestamp"]:
                flag = False
                if verbose:
                    message= f'La chaine est corrompue car un block précedent est  modifié'
        return {'flag':flag, 'message': message}

    # def fork(self, head='latest'):
    #     if head in ['latest', 'whole', 'all']:
    #         return copy.deepcopy(self)
    #     else:
    #         c = copy.deepcopy(self)
    #         c.blocks = c.blocks[0:head+1]
    #         return c
    # def get_root(self, chain_2):
    #     """
    #     docstring
    #     """
    #     min_chain_size = min(self.get_chain_size(), chain_2.get_chain_size())
    #     for i in range(1, min_chain_size + 1):
    #         if self.blocks[i] != chain_2.blocks[i]:
    #             return self.fork(i - 1)
    #     return self.fork(min_chain_size)


def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data

def read_json(path):
    try:
        return json.loads(read_file(path))
    except :
        return False

def write_json(path, data):
     return write_file(path, json.dumps(data, indent=4, sort_keys= True))

def write_file(path, data):
   file = open(path, "w")
   file.write(str(data))
   file.close()
   return data
