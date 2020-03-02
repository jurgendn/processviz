# THƯ VIỆN PROCESSVIZ - PROCESS VISUALIZATION

> Thư viện này được viết ra cho môn `Các mô hình ngẫu nhiên và ứng dụng`, sử dụng để mô tả Markov chain

## Dependencies

1. [networkx](https://networkx.github.io/)
2. [numpy](https://matplotlib.org/)
3. [matplotlib](https://numpy.org/)
4. [pandas](https://pandas.pydata.org/)

## Usage

Simple usage:

```python
import processviz as pvz

g = pvz.MarkovChain()
g.from_stdin(state=[1,2], data=[[0.8,0.2],[0.3,0.7]])
g.generate_graph()
```

This will generate a graph below:

### Instruction

To import library, use:

```python
import processviz as pvz
```

#### Table of Attribute

| attribute name       | use                                     | syntax                                                                                      |
| -------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------- |
| MarkovChain          | generate a empty Markov chain           | processviz.MarkovChain()                                                                    |
| from_stdin           | import data to Markov chain manually    | processviz.from_stdin(state = [(default None)], data = [default None], pi = [default None]) |
| from_file            | import data to Markov chain from file   | processviz.from_file(path = 'matrix_input.csv')                                             |
| \_generate_struct    | generate graph structure                |                                                                                             |
| generate_state_graph | visualize state graph through time      | processviz.generate_state_graph(n = 1)                                                      |
| generate_graph       | generate process matrix at special step | processviz.generate_graph(n = 1)                                                            |
