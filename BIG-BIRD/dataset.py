import torch
from torch.utils import data
import numpy as np
import json
from tqdm import tqdm_notebook as tqdm
#from tqdm import tqdm

class Dataset(data.Dataset):    
    def __init__(self, data_name, INPUT_MAX, OUTPUT_MAX, pad_idx, cutoff=None):
        print("loading json")
        data = json.load(open(data_name, 'r'))
        print("load json done.")
        sum_list = data['summary']
        data_list = data['document']
        
        if cutoff is not None:
            sum_list = sum_list[:cutoff]
            data_list = data_list[:cutoff]
        # idata -> list
        self.size = len(sum_list)
        self.sum_len = 0
        
        self.documents = np.full((self.size, INPUT_MAX), pad_idx, dtype=np.int64)
        self.summaries = np.full((self.size, OUTPUT_MAX), pad_idx, dtype=np.int64)
        
        for i in tqdm(range(self.size)):
            src = data_list[i]
            tgt = sum_list[i]
            cp_src = min(len(src), INPUT_MAX)
            cp_tgt = min(len(tgt), OUTPUT_MAX)
            
            self.documents[i,:cp_src] = src[:cp_src]
            self.summaries[i,:cp_tgt] = tgt[:cp_tgt]
        
     
    def __len__(self):
        return self.size
    def __getitem__(self, index):
        return torch.from_numpy(self.documents[index]), torch.from_numpy(self.summaries[index])
    
def make_data_generator(data_name, in_max, out_max, padding_idx, batch_size, cutoff=None, shuffle=True, num_workers=4):    
    data_set = Dataset(data_name, in_max, out_max, padding_idx, cutoff)
    params = {'batch_size':batch_size,
         'shuffle': shuffle,
         'num_workers': num_workers}
    generator = data.DataLoader(data_set, **params)
    return data_set, generator