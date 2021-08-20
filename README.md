# DynamicTriad-pytorch
This repo is pytorch version of [DynamicTriad](https://github.com/luckiezhou/DynamicTriad).

## Dataset

* academic
* academic_toy
* enron

Academic and academic_toy dataset has been obtained by running
[academic2adjlist.py](https://github.com/luckiezhou/DynamicTriad/blob/master/scripts/academic2adjlist.py)
and enron dataset preprocessing method is proposed by us.

Note: Enron dataset is too big to upload to repository so there is only preprocessing source code.
To use enron dataset download [emails.csv](https://www.kaggle.com/wcukierski/enron-email-dataset/download)
and run `python datasets/enron_preprocessor.py` to generate dataset.

## Differences between original implementation and this

| **Differences** | **Original** | **this** |
| :--- | :--- | :--- |
| python version | 2 | 3 |
| ML library | tensorflow | pytorch |
| graph representation | implemented by C++ | uses python library |
| multiprocessing for sampling | yes | no |
| batch duplication | no | yes |
| vertex label | yes | no |
| evaluation tasks | 6 | 4 |

## Usage

```shell
python src/main.py \
	--model=original \
	--dir=${DIR} \
	--dataset=${DATASET_NAME} \
	--device=${cpu/cuda} \
	--epochs=... \
	--lr=... \
	--time_length=... \
	--time_step=... \
	--time_stride=... \
	--emb_dim=... \
	--beta_triad=... \
	--beta_smooth=... \
	--batchsize=... \
	--batdup=... \
	--mode=...
```

| **Option** | **Description** | **Default** |
|:--- | :--- | :---: |
| `model` | Which model to use ( only `original` is implemented currently) | `original` |
| `dir` | Directory where dataset is located | `datasets`|
|`dataset`| Dataset to train (among `academic`, `academic_toy`, `enron`) | `academic`|
| `device` | Torch device to use (`cpu` or `cuda`) | `cpu`|
| `epochs` | Number of training epochs | 10 |
| `lr` | Learning Rate | 0.1 |
| `time_length` | time length to load from raw dataset | 36 |
| `time_step` | time step to merge from raw dataset | 4 |
| `time_stride` | time stride to jump time when merge from raw dataset | 2 |
| `emb_dim` | embedding dimension | 48 |
| `beta_triad` | hyperparameter for triad loss | 1.0 |
| `beta_smooth` | hyperparameter for smoothness loss | 1.0 |
| `batchsize` | batch size | 10000 |
| `batdup` | batch duplication, hyperparameter to reuse same sample | 1 |
| `mode` | evaluation mode: `{,change_}link_{reconstruction,prediction}` | `link_reconstruction` |

## Merge example

if time length is 16, time step is 4, time stride is 2, dataset is merged as below:

```
 0, 1, 2, 3 -> 0
 2, 3, 4, 5 -> 1
 4, 5, 6, 7 -> 2
 6, 7, 8, 9 -> 3
 8, 9,10,11 -> 4
10,11,12,13 -> 5
12,13,14,15 -> 6
```

## Batch duplication example

original training pseudocode is:
```python
for epoch in range(epochs):
	sample = gen_sample()
	for batch in gen_batch(sample):
		model.train(batch)
```

training pseudocode with batch duplication is:
```python
for epoch in range(epochs):
	sample = gen_sample()
	for _ in range(batdup):
		for batch in gen_batch(sample):
			model.train(batch)
```

You can reuse sample by using batdup hyperparameter. this is implemented due to slow sampling process.
