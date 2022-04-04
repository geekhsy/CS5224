import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import json
import sys


def tokenize(text_feature:list)->dict:
    # tokenized sentences
    tokens = {'input_ids': [], 'attention_mask': []}

    for sentence in text_feature:
    # tokenize sentence and append to dictionary lists
        new_tokens = tokenizer.encode_plus(sentence, max_length=128, truncation=True, padding='max_length', return_tensors='pt')
        tokens['input_ids'].append(new_tokens['input_ids'][0])
        tokens['attention_mask'].append(new_tokens['attention_mask'][0])

    # to single tensor
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
    return tokens

def get_embeddings(tokens,NUM_BATCH):
    # Get the embeddings of sentences above
    mean_pooleds = None

    BATCH = 1
    pool = np.array(0)
    for num_batch in range(NUM_BATCH):
        perc = int(float(num_batch)/NUM_BATCH*100)
        # print('\r'+'▇'*(perc//2)+str(perc)+'%', end='')

        token = {'input_ids': [], 'attention_mask': []}
        token['input_ids'] = tokens['input_ids'][num_batch*BATCH:(num_batch+1)*BATCH]
        token['attention_mask'] = tokens['attention_mask'][num_batch*BATCH:(num_batch+1)*BATCH]

        outputs = model(**token)
        embeddings = outputs.last_hidden_state
        # print('embeddings',embeddings.shape)
        del outputs

        attention_mask = token['attention_mask']
        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        masked_embeddings = embeddings * mask
        # print(masked_embeddings.shape)
        
        summed = torch.sum(masked_embeddings, 1)
        summed_mask = torch.clamp(mask.sum(1), min=1e-9)
        mean_pooled = summed / summed_mask
        mean_pooled = mean_pooled.detach().numpy()
        # print(mean_pooled.shape)
        # save val
        if mean_pooleds is not None:
            mean_pooleds = np.concatenate((mean_pooleds, mean_pooled), axis=0)
        else:
            mean_pooleds = mean_pooled
    return mean_pooleds

def preprocess_data(data):
    # data -> dataframe
    # w -> weights
    data = data.copy()
    values = ["manufactured", "reg_date", "curb_weight", "power", "engine_cap", "no_of_owners",\
              "depreciation", "coe", "road_tax", "dereg_value", "mileage", "omv", "arf"] 
    
    # Dorp useless data
    data = data[values]
    # print("original data", data)
    # print("---------------------------------------------------------")

    # Fill NA
    data.fillna(0, inplace=True)
    # print("data",data)
    # for c in values: 
        # data[c].fillna(data[c].mode()[0], inplace=True)
        # print("datacccc",data[c].mode()[0])
    
    import time
    data['reg_date'] = pd.to_datetime(data['reg_date'])
    data['reg_date'] = data['reg_date'].view('int64')//1e9

    # Using Z-score norm
    if data.shape[0]!=1:
        data = (data - data.mean()) / (data.std())
    # print("data",data)

    # For traditional methods
    W = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    data = data.to_numpy()
    data = W * data

    return data

def get_traditional_scores(data_test, data_train):  
    # print(data_test)
    x_test = preprocess_data(data_test)
    x_train = preprocess_data(data_train)
    
    # print("x-test", x_test)
    sim = cosine_similarity(x_test, x_train)
    # print(sim,sim.shape)
    return sim

def get_top_recommendations(data_test,acc_embedding,des_embedding, **kwargs) -> list:
    
    # Return the top k recommendations
    k = None
    
    # Extract all **kwargs input parameters
    # and set the used paramaters (here: k)
    for key, value in kwargs.items():
        if key == 'k':
            k = value

    # cosine_similarity for BERT
    d_sim = cosine_similarity(des_embedding, d)
    a_sim = cosine_similarity(acc_embedding, a)
    # print('d_sim',d_sim.shape)
    # print()

    # Norm
    d_sim = (d_sim - np.mean(d_sim)) / np.std(d_sim)
    a_sim = (a_sim - np.mean(a_sim)) / np.std(a_sim)

    bert = np.concatenate((a_sim, d_sim),axis=0)
    # print('bert',bert.shape[0])

    # traditional_scores
    trad = get_traditional_scores(data_test, d_train)
    # print('trad',trad.shape[0])

    # W for BERT and Traditional methods
    coefficient=[]
    for i in range(bert.shape[0]+trad.shape[0]):
        if i < bert.shape[0]:
            coefficient.append(1)
        else:
            coefficient.append(3)

    # Cal scores
    scores = np.concatenate((bert, trad), axis=0)
    # print('score',scores.shape)
    scores = scores.T*coefficient
    # print('score',scores.shape)

    scores = cosine_similarity([scores[1]], scores)
    
    scores = scores.flatten()
    ind = np.argpartition(scores, -(k+1))[-(k+1):-1]
    ind = ind[np.argsort(scores[ind])]

    # Return the dataset with the k recommendations
    return ind


def recommend(x_str,k):
    # get test data
    # x_re = sys.argv[1]
    # d_test = pd.read_csv('./test.csv')
    x_ori = json.loads(x_str)
    d_test = pd.DataFrame([x_ori])
    acc_test = d_test['accessories'].tolist()
    des_test = d_test['description'].tolist()
    d_test['description'].fillna(value = '', inplace=True)
    d_test['accessories'].fillna(value = '', inplace=True)
    # x_test = d_test.iloc[0:1]
    # print(x_test)
    # acc_test = d_test['accessories'][0:1].tolist()
    # des_test = d_test['description'][0:1].tolist()

    num_batch = len(acc_test)
    acc_token = tokenize(acc_test)
    des_token = tokenize(des_test)
    # print('token',acc_token['input_ids'].shape[0])
    acc_embedding = get_embeddings(acc_token,num_batch)
    des_embedding = get_embeddings(des_token,num_batch)
    # print('acc_embedding',acc_embedding.shape)

    # k=5
    recommendations = get_top_recommendations(d_test,acc_embedding,des_embedding, k=k)

    # Get the row from the dataframe (an valid row ids will throw an error)
    result = d_train.iloc[recommendations]

    # Just for printing it nicely, we create a new dataframe from this single row
    # print(result.head())
    # result.info\
    return result

if __name__ == '__main__':
    # print('ourput',sys.argv[1])
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
    model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
    
    # read training data
    d_train = pd.read_csv('./train.csv')
    d_train['description'].fillna(value = '', inplace=True)
    d_train['accessories'].fillna(value = '', inplace=True)
    d = np.load("d_embeddings.npy")
    a = np.load("a_embeddings.npy")

    
    recommend_result = recommend(sys.argv[1],int(sys.argv[2]))
    # print("The result is:\n", recommend_result)
    result_json = recommend_result.to_json(orient="records")
    print(result_json)
    # sys.exit(recommend_result)