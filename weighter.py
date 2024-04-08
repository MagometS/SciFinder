import torch
import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util, models, losses
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModel


dmis_biobert = SentenceTransformer('dmis-lab/biobert-base-cased-v1.1')

# tokenizer = AutoTokenizer.from_pretrained("gsarti/biobert-nli")
gsarti_biobert = SentenceTransformer("gsarti/biobert-nli")




############################## At first, just using BioBert ######################################

base_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
bert = models.Transformer('bert-base-uncased')

pooler = models.Pooling(
    bert.get_word_embedding_dimension(),
    pooling_mode_mean_tokens=True
)

custom_model = SentenceTransformer(modules=[bert, pooler])

doc2vec_model = Doc2Vec.load("doc2vec_model")


'dmis-lab/biobert-base-cased-v1.1'

# Two lists of sentences
sentences1 = ['The cat sits outside',
             'A man is playing guitar',
             'The new movie is awesome']

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

absract1 = ['Ripples are brief high-frequency electrographic events with important roles in episodic memory. However, the in vivo circuit mechanisms coordinating ripple-related activity among local and distant neuronal ensembles are not well understood. Here, we define key characteristics of a long-distance projecting GABAergic cell group in the mouse hippocampus that selectively exhibits high-frequency firing during ripples while staying largely silent during theta-associated states when most other GABAergic cells are active. The high ripple-associated firing commenced before ripple onset and reached its maximum before ripple peak, with the signature theta-OFF, ripple-ON firing pattern being preserved across awake and sleep states. Controlled by septal GABAergic, cholinergic, and CA3 glutamatergic inputs, these ripple-selective cells innervate parvalbumin and cholecystokinin-expressing local interneurons while also targeting a variety of extra-hippocampal regions. These results demonstrate the existence of a hippocampal GABAergic circuit element that is uniquely positioned to coordinate ripple-related neuronal dynamics across neuronal assemblies.']
abstractlike1 = ['Sharp wave ripples (SWRs) are high-frequency synchronization events generated by hippocampal neuronal circuits during various forms of learning and reactivated during memory consolidation and recall. There is mounting evidence that SWRs are essential for storing spatial and social memories in rodents and short-term episodic memories in humans. Sharp wave ripples originate mainly from the hippocampal CA3 and subiculum, and can be transmitted to modulate neuronal activity in cortical and subcortical regions for long-term memory consolidation and behavioral guidance. Different hippocampal subregions have distinct functions in learning and memory. For instance, the dorsal CA1 is critical for spatial navigation, episodic memory, and learning, while the ventral CA1 and dorsal CA2 may work cooperatively to store and consolidate social memories. Here, we summarize recent studies demonstrating that SWRs are essential for the consolidation of spatial, episodic, and social memories in various hippocampal-cortical pathways, and review evidence that SWR dysregulation contributes to cognitive impairments in neurodegenerative and neurodevelopmental diseases']
abstractnotlike1 = ['Memories are believed to be encoded by sparse ensembles of neurons in the brain. However, it remains unclear whether there is functional heterogeneity within individual memory engrams, i.e., if separate neuronal subpopulations encode distinct aspects of the memory and drive memory expression differently. Here, we show that contextual fear memory engrams in the mouse dentate gyrus contain functionally distinct neuronal ensembles, genetically defined by the Fos- or Npas4-dependent transcriptional pathways. The Fos-dependent ensemble promotes memory generalization and receives enhanced excitatory synaptic inputs from the medial entorhinal cortex, which we find itself also mediates generalization. The Npas4-dependent ensemble promotes memory discrimination and receives enhanced inhibitory drive from local cholecystokinin-expressing interneurons, the activity of which is required for discrimination. Our study provides causal evidence for functional heterogeneity within the memory engram and reveals synaptic and circuit mechanisms used by each ensemble to regulate the memory discrimination-generalization balance.']
abstractnotatalllike1 = ['This article describes neural models of attention. Since attention is not a disembodied process, the article explains how brain processes of consciousness, learning, expectation, attention, resonance, and synchrony interact. These processes show how attention plays a critical role in dynamically stabilizing perceptual and cognitive learning throughout our lives. Classical concepts of object and spatial attention are replaced by mechanistically precise processes of prototype, boundary, and surface attention. Adaptive resonances trigger learning of bottom-up recognition categories and top-down expectations that help to classify our experiences, and focus prototype attention upon the patterns of critical features that predict behavioral success. These feature-category resonances also maintain the stability of these learned memories. Different types of resonances induce functionally distinct conscious experiences during seeing, hearing, feeling, and knowing that are described and explained, along with their different attentional and anatomical correlates within different parts of the cerebral cortex. All parts of the cerebral cortex are organized into layered circuits. Laminar computing models show how attention is embodied within a canonical laminar neocortical circuit design that integrates bottom-up filtering, horizontal grouping, and top-down attentive matching. Spatial and motor processes obey matching and learning laws that are computationally complementary to those obeyed by perceptual and cognitive processes. Their laws adapt to bodily changes throughout life, and do not support attention or conscious states.']


# Load pre-trained model tokenizer (vocabulary)
#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def weighter_k(first_keywords, second_keywords):
    # keywords_1 = df.loc[ df['pubmed_id'] == first_id, 'keywords' ].iloc[0]
    # keywords_2 = df.loc[ df['pubmed_id'] == second_id, 'keywords' ].iloc[0]

    embeddings1 = base_model.encode(first_keywords, convert_to_numpy=True, normalize_embeddings = True)
    embeddings2 = base_model.encode(second_keywords, convert_to_numpy=True, normalize_embeddings = True)

    # tokenized_doc1 = word_tokenize(first_keywords.lower())
    # tokenized_doc2 = word_tokenize(second_keywords.lower())
    # print('tokenized_doc1: ', tokenized_doc1)
 
    # doc2vec_embedding1 = doc2vec_model.infer_vector(tokenized_doc1)
    # doc2vec_embedding2 = doc2vec_model.infer_vector(tokenized_doc2)
    # print('base embedding: ', embeddings1, embeddings1.shape)
    # print('doc2vec embedding: ',doc2vec_embedding1, embeddings2.shape)

    #Compute cosine-similarits
    base_cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

    #doc2vec_cosine_scores = util.pytorch_cos_sim([doc2vec_embedding1], [doc2vec_embedding2])
    #print('cosine_score: ', base_cosine_scores)

    weight = 1/((sum(sum(base_cosine_scores.numpy()))+1))
    #print('weight: ', weight) # +1 for 0 to 2 score, and more similar articles - less weight between them
    return weight  

    # dot_scores = util.dot_score(embeddings1, embeddings2)
    # return (dot_scores)



print(weighter_k(abstractlike1, absract1))
print(weighter_k(abstractnotlike1, absract1))
print(weighter_k(abstractlike1, abstractnotlike1))
print(weighter_k(abstractlike1, abstractnotatalllike1))



def check_embeddings(words, model = base_model):
   
    if model == doc2vec_model: embeddings = model.infer_vector(words)
    embeddings = model.encode(words, convert_to_tensor=True)
    X = embeddings.cpu()

    from sklearn.decomposition import PCA
    reducer = PCA(n_components=2)
    r = reducer.fit_transform(embeddings.cpu())
    
    import time
    t0 = time.time()

    import matplotlib.pyplot as plt
    import seaborn as sns

    fig = plt.figure(figsize = (25,10));  c = 0
    n_x_subplots = 2
    #plt.suptitle(str_data_inf, fontsize = 20)       

    c+=1; fig.add_subplot(1,n_x_subplots,c)

    from sklearn.decomposition import PCA
    reducer = PCA(n_components=2)
    r = reducer.fit_transform(X)

    sns.scatterplot(x=r[:,0],y=r[:,1])
    plt.title(str(reducer))

    mask = r[:,1] > 2
    #print( np.array(words)[mask] )

    mask = r[:,1] > 2
    #print( np.array(words)[mask] )

    # c+=1; fig.add_subplot(1,n_x_subplots,c);

    # import umap.umap_ as umap
    # reducer = umap.UMAP()# 
    # r = reducer.fit_transform(X )

    # sns.scatterplot(x=r[:,0],y=r[:,1])
    # plt.title(str(reducer))


    plt.show()

    print('%.1f seconds passed'%(-t0 + time.time() ) )

#print(weighter_k(sentences1[0], sentences2[0]))


    #Output the pairs with their score
    # for i in range(len(sentences1)):
    #     print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
    #     print(keywords_1)




############################## bert training ###################################

print('\nSOMEHOW weighter is running!\n')
dataset_Name='PubMed Multi Label Text Classification Dataset Processed.csv'

df= pd.read_csv(dataset_Name)


df_train, df_test = train_test_split(df, random_state=32, test_size=0.20, shuffle=True)

cols = df.columns
cols = list(df.columns)
mesh_Heading_categories = cols[6:]
num_labels = len(mesh_Heading_categories)

df_train['one_hot_labels'] = list(df_train[mesh_Heading_categories].values)

#print(df_train[:5], '\n'*2)

positive_pairs = []


# Choosing pairs of articles with matching MESH-Labels and adding them into training dataset
for idx1,row1 in df_train[:30].iterrows():
    for idx2,row2 in df_train[:30].iterrows():
        #print(row1, row2)
        labels1 = int(''.join (map(str, row1['one_hot_labels'])), 2)
        labels2 = int(''.join (map(str, row2['one_hot_labels'])), 2)
        # print('labels: ', bin(labels1), bin(labels2))
        overlay = bin(labels1 & labels2)
        similarity = sum([int(e) for e in str(overlay)[2:]])
        #print('abstract: ', row1['abstractText'])
        if similarity >=6 : positive_pairs.append([row1['abstractText'], row2['abstractText']])
        #print('len of labels: ', len(str(bin(labels2))))
        # print('similarity: ', similarity, '\n')

labels = list(df_train.one_hot_labels.values)
Article_train = list(df_train.abstractText.values)



dataset = df

from sentence_transformers import InputExample

# Formatting our dataset of pairs for DataLoader via InputExample
train_examples = []

n_examples = len(positive_pairs)

for i in range(n_examples):
  example = positive_pairs[i]
  train_examples.append(InputExample(texts = example, label = 1))

from torch.utils.data import DataLoader

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)


from sentence_transformers import losses

#train_loss = losses.MultipleNegativesRankingLoss(model=model)

# model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=2)


###############################   WordToVec    #######################################


'''
dataset_Name='PubMed Multi Label Text Classification Dataset Processed.csv'

df= pd.read_csv(dataset_Name)

df_train, df_test = train_test_split(df, random_state=32, test_size=0.20, shuffle=True)

cols = df.columns
cols = list(df.columns)
mesh_Heading_categories = cols[6:]
num_labels = len(mesh_Heading_categories)

df_train['one_hot_labels'] = list(df_train[mesh_Heading_categories].values)

#Labels = list(df_train.one_hot_labels.values)
Article_train = list(df_train.abstractText.values)

import pickle
import nltk
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#nltk.download()

#nltk.download('punkt')


#Use Doc2Vec to vectorise the contents of abstractText
# Tokenize the documents
tokenized_documents = [word_tokenize(document.lower()) for document in Article_train]

#Create TaggedDocument objects
# tagged_data = [TaggedDocument(words=doc, tags=[str(i)]) for i, doc in enumerate(tokenized_documents)]

# #Train Doc2Vec model
# model = Doc2Vec(vector_size=100, window=5, min_count=1, workers=8, epochs=50)
# model.build_vocab(tagged_data)

# print('Training started')
# model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
# model.save("doc2vec_model")

model = Doc2Vec.load("doc2vec_model")

vector_representation = model.infer_vector(tokenized_documents[0])
print(vector_representation)
'''