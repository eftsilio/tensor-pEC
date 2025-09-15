# Tensor-pEC: A Tensor-Based Probabilistic Event Calculus

Tensor-pEC is an open-source tensor formalization of a probabilistic [Event Calculus](https://en.wikipedia.org/wiki/Event_calculus) (EC), optimized for data stream reasoning.

# License

Tensor-pEC comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions; see the [GNU Lesser General Public License v3 for more details](http://www.gnu.org/licenses/lgpl-3.0.html).

# File Description

[Prob-EC](https://cer.iit.demokritos.gr/publications/papers/2015/artikis-TPLP.pdf) is the symbolical implementation of probabilistic EC, which is based on [ProbLog](https://arxiv.org/pdf/1304.6810) and written in Python.

Tensor-pEC is implemented in Python and is tested under Python 3.12.2, NumPy 1.26.4 and SciPy 1.13.1.

The probabilistic CER process involves the computation and caching of the instantaneous probabilities of fluent-value pairs, expressing CEs, to hold.
We provide two datasets:

- [CAVIAR](https://groups.inf.ed.ac.uk/vision/DATASETS/CAVIAR/CAVIARDATA1/), a benchmark human activity recognition dataset.
- Brest, a publicly available dataset from the maritime domain, concerning vessels sailing in the Atlantic Ocean around the port of Brest, France.

All the datasets are provided as csv files. Regarding the maritime application, we provide a subset of the public dataset of Brest, due to its size. To run the source code of each method, you have to enter the corresponding directory, that is, "./Prob-EC" for Prob-EC and "./Tensor-pEC" for the tensor method. Then, open a terminal and type the following command:

```python
$ python3 run-exps.py <app>
```
where <app\> corresponds to one of the following:

- m, for the Brest dataset.
- c, for the CAVIAR dataset.

For example, assume you want to execute the source code of tensor-pEC for the maritime monitoring application. Then, you will type in the command line the following:

```python
$ python3 run−exps.py m
```

When the probabilistic CER process terminates, the results are saved in the folder of the executed method. Assume, for example, you have performed probabilistic CER with tensor-pEC in the CAVIAR dataset. The results will be saved in the directory "./examples/caviar/results/Tensor-pEC/".


# Documentation

- Tsilionis E., Artikis A. and Paliouras G., [A Tensor-Based Probabilistic Event Calculus](). In International Conference on Principles of Knowledge Representation and Reasoning (KR), 2025.

# Related Software
- [Tensor-EC](https://github.com/eftsilio/Tensor-EC): Tensor-EC is tensor-based (non-porbabilistic) formalization of the Event Calculus.<br /> Tsilionis E., Artikis A., Paliouras G., [A Tensor-Based Formalization of the Event Calculus](https://cer.iit.demokritos.gr/publications/papers/2024/tensor-EC.pdf). In the International Joint Conference on Artificial Intelligence (IJCAI), 2024.

- [RTEC](https://github.com/aartikis/RTEC): RTEC is an Event Calculus implementation optimised for stream reasoning.
